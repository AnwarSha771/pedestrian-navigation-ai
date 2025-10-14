/**
 * SensorUploadService.kt
 * 
 * Background service for collecting sensor data and GPS location
 * Sends data to Python backend for pedestrian navigation processing
 * 
 * Features:
 * - Real-time GPS tracking
 * - Accelerometer data collection
 * - Battery-optimized sampling
 * - Offline data caching
 * - Automatic reconnection
 */

package com.pedestriannav.wearable

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.BatteryManager
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import androidx.core.app.NotificationCompat
import kotlinx.coroutines.*
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.util.concurrent.TimeUnit
import kotlin.math.sqrt

class SensorUploadService : Service(), SensorEventListener, LocationListener {
    
    // Managers
    private lateinit var sensorManager: SensorManager
    private lateinit var locationManager: LocationManager
    private lateinit var powerManager: PowerManager
    private lateinit var batteryManager: BatteryManager
    
    // Sensors
    private var accelerometer: Sensor? = null
    private var gyroscope: Sensor? = null
    private var magnetometer: Sensor? = null
    
    // Data
    private var lastAccel = FloatArray(3)
    private var lastGyro = FloatArray(3)
    private var lastMagnet = FloatArray(3)
    private var currentLocation: Location? = null
    
    // Network
    private val client = OkHttpClient.Builder()
        .callTimeout(10, TimeUnit.SECONDS)
        .connectTimeout(5, TimeUnit.SECONDS)
        .retryOnConnectionFailure(true)
        .build()
    
    // Coroutines
    private val serviceScope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    
    // Configuration
    private var serverUrl = "http://192.168.1.100:5000" // Default, should be configurable
    private var samplingRate = SensorManager.SENSOR_DELAY_NORMAL
    private var batchSize = 10
    private var locationUpdateInterval = 1000L // 1 second
    private var locationUpdateDistance = 1f // 1 meter
    
    // Data buffer
    private val dataBuffer = mutableListOf<JSONObject>()
    private val maxBufferSize = 100
    
    // Statistics
    private var eventsCollected = 0
    private var eventsSent = 0
    private var eventsFailed = 0
    
    companion object {
        private const val NOTIFICATION_ID = 1001
        private const val CHANNEL_ID = "pedestrian_nav_service"
        private const val TAG = "SensorUploadService"
    }
    
    override fun onCreate() {
        super.onCreate()
        
        // Initialize managers
        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        locationManager = getSystemService(LOCATION_SERVICE) as LocationManager
        powerManager = getSystemService(POWER_SERVICE) as PowerManager
        batteryManager = getSystemService(BATTERY_SERVICE) as BatteryManager
        
        // Get sensors
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION)
            ?: sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
        magnetometer = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD)
        
        // Register sensor listeners
        accelerometer?.let { 
            sensorManager.registerListener(this, it, samplingRate)
        }
        gyroscope?.let {
            sensorManager.registerListener(this, it, samplingRate)
        }
        magnetometer?.let {
            sensorManager.registerListener(this, it, samplingRate)
        }
        
        // Start location updates (with permission check in calling activity)
        try {
            locationManager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                locationUpdateInterval,
                locationUpdateDistance,
                this
            )
            
            // Also use network provider as backup
            locationManager.requestLocationUpdates(
                LocationManager.NETWORK_PROVIDER,
                locationUpdateInterval * 2, // Less frequent
                locationUpdateDistance * 2,
                this
            )
        } catch (e: SecurityException) {
            android.util.Log.e(TAG, "Location permission not granted", e)
        }
        
        // Load configuration
        loadConfiguration()
        
        // Start foreground service
        startForeground(NOTIFICATION_ID, createNotification())
        
        // Start periodic upload
        startPeriodicUpload()
        
        android.util.Log.i(TAG, "SensorUploadService started")
    }
    
    private fun createNotification(): Notification {
        // Create notification channel for Android O+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Pedestrian Navigation",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Collecting sensor data for navigation"
            }
            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }
        
        return NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Pedestrian Navigation Active")
            .setContentText("Collecting sensor and GPS data")
            .setSmallIcon(android.R.drawable.ic_dialog_map) // Use your own icon
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()
    }
    
    override fun onSensorChanged(event: SensorEvent) {
        when (event.sensor.type) {
            Sensor.TYPE_LINEAR_ACCELERATION, Sensor.TYPE_ACCELEROMETER -> {
                lastAccel = event.values.clone()
                
                // Calculate magnitude for motion detection
                val magnitude = sqrt(
                    lastAccel[0] * lastAccel[0] +
                    lastAccel[1] * lastAccel[1] +
                    lastAccel[2] * lastAccel[2]
                )
                
                // Only record if significant motion (save battery)
                if (magnitude > 0.5f || dataBuffer.isEmpty()) {
                    recordSensorData()
                }
            }
            
            Sensor.TYPE_GYROSCOPE -> {
                lastGyro = event.values.clone()
            }
            
            Sensor.TYPE_MAGNETIC_FIELD -> {
                lastMagnet = event.values.clone()
            }
        }
    }
    
    private fun recordSensorData() {
        currentLocation?.let { loc ->
            try {
                val payload = JSONObject().apply {
                    // Location data
                    put("lat", loc.latitude)
                    put("lon", loc.longitude)
                    put("altitude", loc.altitude)
                    put("speed", loc.speed)
                    put("bearing", loc.bearing)
                    put("accuracy", loc.accuracy)
                    
                    // Accelerometer data
                    put("ax", lastAccel[0])
                    put("ay", lastAccel[1])
                    put("az", lastAccel[2])
                    
                    // Gyroscope data
                    put("gx", lastGyro[0])
                    put("gy", lastGyro[1])
                    put("gz", lastGyro[2])
                    
                    // Magnetometer data
                    put("mx", lastMagnet[0])
                    put("my", lastMagnet[1])
                    put("mz", lastMagnet[2])
                    
                    // Metadata
                    put("timestamp", System.currentTimeMillis())
                    put("battery", getBatteryLevel())
                    put("device_id", getDeviceId())
                }
                
                // Add to buffer
                synchronized(dataBuffer) {
                    dataBuffer.add(payload)
                    eventsCollected++
                    
                    // Limit buffer size
                    if (dataBuffer.size > maxBufferSize) {
                        dataBuffer.removeAt(0)
                    }
                    
                    // Send batch if buffer full
                    if (dataBuffer.size >= batchSize) {
                        serviceScope.launch {
                            sendBatch()
                        }
                    }
                }
            } catch (e: Exception) {
                android.util.Log.e(TAG, "Error recording sensor data", e)
            }
        }
    }
    
    private fun startPeriodicUpload() {
        serviceScope.launch {
            while (isActive) {
                delay(5000) // Upload every 5 seconds
                
                synchronized(dataBuffer) {
                    if (dataBuffer.isNotEmpty()) {
                        sendBatch()
                    }
                }
            }
        }
    }
    
    private suspend fun sendBatch() {
        val batch: List<JSONObject>
        
        synchronized(dataBuffer) {
            if (dataBuffer.isEmpty()) return
            
            batch = dataBuffer.toList()
            dataBuffer.clear()
        }
        
        try {
            val jsonArray = JSONArray()
            batch.forEach { jsonArray.put(it) }
            
            val requestBody = JSONObject().apply {
                put("events", jsonArray)
                put("batch_size", batch.size)
                put("device_type", "android")
            }
            
            postEvents(requestBody.toString())
            
            eventsSent += batch.size
            android.util.Log.d(TAG, "Sent batch of ${batch.size} events. Total: $eventsSent")
            
        } catch (e: Exception) {
            android.util.Log.e(TAG, "Error sending batch", e)
            eventsFailed += batch.size
            
            // Re-add to buffer for retry
            synchronized(dataBuffer) {
                dataBuffer.addAll(0, batch)
            }
            
            // Save to disk for offline mode
            saveToCache(batch)
        }
    }
    
    private fun postEvents(json: String) {
        val mediaType = "application/json; charset=utf-8".toMediaType()
        val requestBody = json.toRequestBody(mediaType)
        
        val request = Request.Builder()
            .url("$serverUrl/report")
            .post(requestBody)
            .addHeader("Content-Type", "application/json")
            .addHeader("X-Device-Type", "android")
            .addHeader("X-App-Version", "1.0.0")
            .build()
        
        try {
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) {
                    throw Exception("Server returned ${response.code}")
                }
                
                val responseBody = response.body?.string()
                android.util.Log.d(TAG, "Server response: $responseBody")
            }
        } catch (e: Exception) {
            android.util.Log.e(TAG, "Network error", e)
            throw e
        }
    }
    
    private fun saveToCache(batch: List<JSONObject>) {
        try {
            val cacheDir = File(cacheDir, "sensor_data")
            if (!cacheDir.exists()) {
                cacheDir.mkdirs()
            }
            
            val cacheFile = File(cacheDir, "cache_${System.currentTimeMillis()}.json")
            val jsonArray = JSONArray()
            batch.forEach { jsonArray.put(it) }
            
            cacheFile.writeText(jsonArray.toString())
            android.util.Log.d(TAG, "Cached ${batch.size} events to ${cacheFile.name}")
        } catch (e: Exception) {
            android.util.Log.e(TAG, "Error caching data", e)
        }
    }
    
    override fun onLocationChanged(location: Location) {
        currentLocation = location
        android.util.Log.d(TAG, "Location updated: ${location.latitude}, ${location.longitude}")
        
        // Update notification with location info
        updateNotification("Lat: %.4f, Lon: %.4f".format(location.latitude, location.longitude))
    }
    
    private fun updateNotification(text: String) {
        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Pedestrian Navigation Active")
            .setContentText(text)
            .setSmallIcon(android.R.drawable.ic_dialog_map)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()
        
        val notificationManager = getSystemService(NotificationManager::class.java)
        notificationManager.notify(NOTIFICATION_ID, notification)
    }
    
    private fun getBatteryLevel(): Int {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
        } else {
            -1
        }
    }
    
    private fun getDeviceId(): String {
        // Use a persistent UUID stored in SharedPreferences
        val prefs = getSharedPreferences("pedestrian_nav", Context.MODE_PRIVATE)
        var deviceId = prefs.getString("device_id", null)
        
        if (deviceId == null) {
            deviceId = java.util.UUID.randomUUID().toString()
            prefs.edit().putString("device_id", deviceId).apply()
        }
        
        return deviceId
    }
    
    private fun loadConfiguration() {
        val prefs = getSharedPreferences("pedestrian_nav", Context.MODE_PRIVATE)
        serverUrl = prefs.getString("server_url", serverUrl) ?: serverUrl
        batchSize = prefs.getInt("batch_size", batchSize)
        samplingRate = prefs.getInt("sampling_rate", samplingRate)
        
        android.util.Log.d(TAG, "Configuration loaded: serverUrl=$serverUrl, batchSize=$batchSize")
    }
    
    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        android.util.Log.d(TAG, "Sensor accuracy changed: ${sensor?.name}, accuracy=$accuracy")
    }
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onDestroy() {
        android.util.Log.i(TAG, "SensorUploadService stopping")
        
        // Unregister sensors
        sensorManager.unregisterListener(this)
        
        // Stop location updates
        try {
            locationManager.removeUpdates(this)
        } catch (e: SecurityException) {
            android.util.Log.e(TAG, "Error removing location updates", e)
        }
        
        // Cancel coroutines
        serviceScope.cancel()
        
        // Log statistics
        android.util.Log.i(TAG, "Statistics: Collected=$eventsCollected, Sent=$eventsSent, Failed=$eventsFailed")
        
        super.onDestroy()
    }
}

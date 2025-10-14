/**
 * MainActivity.kt
 * 
 * Main activity for Pedestrian Navigation Android App
 * Handles permissions, service lifecycle, and UI
 */

package com.pedestriannav.wearable

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {
    
    private lateinit var btnStartService: Button
    private lateinit var btnStopService: Button
    private lateinit var etServerUrl: EditText
    private lateinit var tvStatus: TextView
    
    private var isServiceRunning = false
    
    companion object {
        private const val PERMISSION_REQUEST_CODE = 100
        private val REQUIRED_PERMISSIONS = mutableListOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.INTERNET,
            Manifest.permission.FOREGROUND_SERVICE,
            Manifest.permission.VIBRATE
        ).apply {
            // Add Android 10+ background location permission
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                add(Manifest.permission.ACCESS_BACKGROUND_LOCATION)
            }
            // Add Android 9+ activity recognition permission
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                add(Manifest.permission.ACTIVITY_RECOGNITION)
            }
            // Add Android 12+ Bluetooth permissions
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                add(Manifest.permission.BLUETOOTH_CONNECT)
            }
        }.toTypedArray()
    }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Initialize views
        btnStartService = findViewById(R.id.btnStartService)
        btnStopService = findViewById(R.id.btnStopService)
        etServerUrl = findViewById(R.id.etServerUrl)
        tvStatus = findViewById(R.id.tvStatus)
        
        // Load saved server URL
        val prefs = getSharedPreferences("pedestrian_nav", MODE_PRIVATE)
        etServerUrl.setText(prefs.getString("server_url", "http://192.168.1.100:5000"))
        
        // Set up button listeners
        btnStartService.setOnClickListener {
            if (checkPermissions()) {
                startSensorService()
            } else {
                requestPermissions()
            }
        }
        
        btnStopService.setOnClickListener {
            stopSensorService()
        }
        
        // Update UI
        updateUI()
    }
    
    private fun checkPermissions(): Boolean {
        return REQUIRED_PERMISSIONS.all {
            ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED
        }
    }
    
    private fun requestPermissions() {
        ActivityCompat.requestPermissions(
            this,
            REQUIRED_PERMISSIONS,
            PERMISSION_REQUEST_CODE
        )
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            if (grantResults.all { it == PackageManager.PERMISSION_GRANTED }) {
                Toast.makeText(this, "Permissions granted", Toast.LENGTH_SHORT).show()
                startSensorService()
            } else {
                Toast.makeText(
                    this,
                    "Permissions required for sensor data collection",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }
    
    private fun startSensorService() {
        // Save server URL
        val serverUrl = etServerUrl.text.toString()
        val prefs = getSharedPreferences("pedestrian_nav", MODE_PRIVATE)
        prefs.edit().putString("server_url", serverUrl).apply()
        
        // Start service
        val intent = Intent(this, SensorUploadService::class.java)
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        
        isServiceRunning = true
        updateUI()
        
        Toast.makeText(this, "Sensor service started", Toast.LENGTH_SHORT).show()
    }
    
    private fun stopSensorService() {
        val intent = Intent(this, SensorUploadService::class.java)
        stopService(intent)
        
        isServiceRunning = false
        updateUI()
        
        Toast.makeText(this, "Sensor service stopped", Toast.LENGTH_SHORT).show()
    }
    
    private fun updateUI() {
        if (isServiceRunning) {
            btnStartService.isEnabled = false
            btnStopService.isEnabled = true
            tvStatus.text = "Status: Running ✅"
            tvStatus.setTextColor(getColor(android.R.color.holo_green_dark))
        } else {
            btnStartService.isEnabled = true
            btnStopService.isEnabled = false
            tvStatus.text = "Status: Stopped ⏸️"
            tvStatus.setTextColor(getColor(android.R.color.holo_red_dark))
        }
    }
}

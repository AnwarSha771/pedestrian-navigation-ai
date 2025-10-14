#!/data/data/com.termux/files/usr/bin/bash
#
# Quick camera test for Termux
# Tests if termux-camera-photo command works
#

echo "📷 Testing Termux Camera Access..."
echo ""

# Check if termux-api is installed
if ! command -v termux-camera-photo &> /dev/null; then
    echo "❌ termux-camera-photo not found!"
    echo ""
    echo "Install Termux:API:"
    echo "1. Install app from F-Droid: https://f-droid.org/packages/com.termux.api/"
    echo "2. Run: pkg install termux-api"
    exit 1
fi

# Check camera info
echo "🔍 Checking available cameras..."
termux-camera-info 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  Could not get camera info"
    echo "Make sure Termux:API app has camera permission"
fi

echo ""
echo "📸 Taking test photo..."

# Take photo with back camera
termux-camera-photo -c 0 test_photo.jpg 2>/dev/null

# Check if photo was created
if [ -f "test_photo.jpg" ]; then
    echo "✅ Camera works!"
    echo ""
    echo "Photo details:"
    ls -lh test_photo.jpg
    
    # Show where it's saved
    echo ""
    echo "Photo saved at: $(pwd)/test_photo.jpg"
    
    # Ask if user wants to delete
    echo ""
    echo "Delete test photo? (y/n)"
    read -r answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        rm test_photo.jpg
        echo "🗑️  Test photo deleted"
    fi
else
    echo "❌ Camera test failed!"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check Termux:API app is installed"
    echo "2. Grant camera permission: Android Settings → Apps → Termux:API → Permissions → Camera"
    echo "3. Restart Termux"
    exit 1
fi

echo ""
echo "✅ Camera ready for navigation system!"

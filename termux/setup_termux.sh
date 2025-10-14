#!/data/data/com.termux/files/usr/bin/bash
#
# Termux Setup Script for Pedestrian Navigation AI
# Tested on OnePlus 11R with Termux
#
# Usage: bash setup_termux.sh
#

echo "=========================================="
echo "🚀 Termux Setup - Pedestrian Navigation AI"
echo "=========================================="
echo ""

# Update packages
echo "📦 Updating Termux packages..."
pkg update -y && pkg upgrade -y

# Install required packages
echo "📦 Installing system dependencies..."
pkg install -y \
    python \
    python-pip \
    clang \
    cmake \
    ninja \
    pkg-config \
    libjpeg-turbo \
    libpng \
    wget \
    git \
    termux-api \
    ffmpeg \
    libopenblas

echo ""
echo "✅ System packages installed"
echo ""

# Install Python packages
echo "🐍 Installing Python dependencies..."
echo "This may take 10-15 minutes on mobile..."
echo ""

# Upgrade pip
pip install --upgrade pip

# Install core ML libraries
echo "Installing NumPy..."
pip install numpy

echo "Installing OpenCV (lightweight)..."
pip install opencv-python-headless

echo "Installing PyTorch (CPU only for mobile)..."
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

echo "Installing YOLOv8..."
pip install ultralytics

echo "Installing audio libraries..."
pip install pyttsx3 || echo "⚠️ pyttsx3 may not work on Termux, audio will be disabled"

echo "Installing utilities..."
pip install pillow requests

echo ""
echo "✅ Python packages installed"
echo ""

# Create project directory
echo "📁 Setting up project structure..."
cd ~
if [ ! -d "pedestrian-navigation-ai" ]; then
    mkdir -p pedestrian-navigation-ai
fi

cd pedestrian-navigation-ai

# Download YOLOv8 model
echo "📥 Downloading YOLOv8 Nano model..."
if [ ! -f "yolov8n.pt" ]; then
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
fi

echo ""
echo "✅ Model downloaded"
echo ""

# Check Termux:API installation
echo "🔍 Checking Termux:API..."
if command -v termux-camera-photo &> /dev/null; then
    echo "✅ Termux:API found"
else
    echo "⚠️  Termux:API not found!"
    echo ""
    echo "Please install Termux:API from F-Droid:"
    echo "https://f-droid.org/en/packages/com.termux.api/"
    echo ""
fi

# Create test script
echo "📝 Creating test script..."
cat > test_camera.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
echo "Testing camera access..."
termux-camera-photo test_photo.jpg
if [ -f "test_photo.jpg" ]; then
    echo "✅ Camera works! Photo saved as test_photo.jpg"
    ls -lh test_photo.jpg
else
    echo "❌ Camera test failed"
fi
EOF
chmod +x test_camera.sh

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📍 Project location: ~/pedestrian-navigation-ai"
echo ""
echo "Next steps:"
echo "1. Install Termux:API app from F-Droid"
echo "2. Clone project: git clone https://github.com/AnwarSha771/pedestrian-navigation-ai.git"
echo "3. Run: python termux_main.py"
echo ""
echo "Test camera: ./test_camera.sh"
echo ""

Check if connected to Pi 5
```python
lsusb
```
You should see an Intel device with USB vendor ID 8086

Check connection speed
```python
lsusb -t
```
Ideally, the camera should appear at 5000M

reference for the following: https://github.com/dannyh147/Pi5-realsense
## Prerequisites
Install system dependencies:
```python
sudo apt update && sudo apt install -y \
  git cmake build-essential libssl-dev libusb-1.0-0-dev libudev-dev pkg-config \
  libgtk-3-dev libglfw3-dev libgl1-mesa-dev python3-pybind11 pybind11-dev \
  ffmpeg wget
```

## Build and Install librealsense
librealsense is necessary with working with any Intel Real Sense camera

1. Clone the SDK and create a build directory:
```python
cd ~
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
mkdir build && cd build
```

2. Configure with UVC (RSUSB) backend and Python bindings enabled:
```python
cmake ../ \
  -DFORCE_RSUSB_BACKEND=ON \
  -DBUILD_PYTHON_BINDINGS=ON \
  -DPYTHON_EXECUTABLE=$(which python3.11) \
  -DCMAKE_BUILD_TYPE=Release
```

3. Compile and install:
```python
make -j$(nproc)
sudo make install
sudo ldconfig
```

## Generate and Install Python Bindings

1. Generate (needed by setup.py)
```python
cd ~/librealsense
python3.11 wrappers/python/find_librs_version.py \
  "$(pwd)" "$(pwd)/wrappers/python/pyrealsense2"
```

2. Copy the compiled into the Python package:
```python
cp build/Release/pyrealsense2.cpython-311-aarch64-linux-gnu.so \
  wrappers/python/pyrealsense2/pyrealsense2.so
```

3. Install into system site-packages
```python
cd wrappers/python
sudo python3.11 setup.py install
```

## Verify Python Wrapper
Run:
```python
python3.11 - <<EOF
import pyrealsense2 as rs
print("pipeline available?", "pipeline" in dir(rs))
p = rs.pipeline()
print("Pipeline created:", p)
EOF
```
Should print True and show a pipeline object without errors

## Install RTSP Server (MediaMTX)
1. Download and install the ARM64 server:
```python

```
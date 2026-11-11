#!/usr/bin/env python3.11
"""
Dual RealSense IR → RTSP
"""
import pyrealsense2 as rs
import numpy as np
import subprocess, signal, sys

# RTSP mountpoints
RTSP1 = 'rtsp://localhost:8554/ir1'
RTSP2 = 'rtsp://localhost:8554/ir2'
# RealSense params
W, H, FPS = 1280, 720, 30

def start_ffmpeg(url):
    cmd = [
        'ffmpeg','-re','-f','rawvideo','-pix_fmt','gray8',
        '-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','ultrafast','-tune','zerolatency',
        '-f','rtsp','-rtsp_transport','tcp',url
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

# Setup
ff1 = start_ffmpeg(RTSP1)
ff2 = start_ffmpeg(RTSP2)
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.infrared, 1, W, H, rs.format.y8, FPS)
cfg.enable_stream(rs.stream.infrared, 2, W, H, rs.format.y8, FPS)
pipe.start(cfg)
print("Streaming IR1 → /ir1 and IR2 → /ir2")

# Graceful shutdown
 def shutdown(*_):
    for ff in (ff1, ff2): ff.stdin.close(); ff.wait()
    pipe.stop(); sys.exit(0)
for sig in (signal.SIGINT, signal.SIGTERM): signal.signal(sig, shutdown)

# Main loop
while True:
    frames = pipe.wait_for_frames()
    ir1 = np.asanyarray(frames.get_infrared_frame(1).get_data())
    ir2 = np.asanyarray(frames.get_infrared_frame(2).get_data())
    ff1.stdin.write(ir1.tobytes())
    ff2.stdin.write(ir2.tobytes())
import os
import ctypes
from ctypes import wintypes
import time
import math
from consmath.crackcailonmemay import *

mouse_dll = ctypes.CDLL("consmath/svchost.dll")

DriverAuth = mouse_dll.DriverAuth
DriverAuth.argtypes = [wintypes.HANDLE]
DriverAuth.restype = ctypes.c_bool

MoveMouse = mouse_dll.MoveMouse
MoveMouse.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_int]
MoveMouse.restype = ctypes.c_bool

driver_handle = None

def init():
    global driver_handle
    if driver_handle is not None:
        ctypes.windll.kernel32.CloseHandle(driver_handle)
    
    driver_handle = ctypes.windll.kernel32.CreateFileW(
        "\\\\.\\JustWokeUp",
        0xC0000000,  # GENERIC_READ | GENERIC_WRITE
        0x00000003,  # FILE_SHARE_READ | FILE_SHARE_WRITE
        None,
        3,           # OPEN_EXISTING
        0,
        None
    )
    if driver_handle == -1:  # INVALID_HANDLE_VALUE
        print("\033[1;39m[\033[0;31mvn.dev\033[1;39m] Không thể mở driver chuột.")
        time.sleep(5)
        return False
    
    if not DriverAuth(driver_handle):
        print("\033[1;39m[\033[0;31mvn.dev\033[1;39m] Xác thực driver thất bại.")
        ctypes.windll.kernel32.CloseHandle(driver_handle)
        return False
    return True

def ease_in_out(t):
    return -0.5 * (math.cos(math.pi * t) - 1)

def mouse_move(x, y):
    global driver_handle, smoothness
    if driver_handle is None or driver_handle == -1:
        if not init():
            return
    
    steps = max(1, int(smoothness))
    if steps <= 0:
        print("\033[1;39m[\033[0;31mvn.dev\033[1;39m] Giá trị độ mượt không hợp lệ.")
        return
    
    start_x, start_y = 0, 0
    previous_x, previous_y = start_x, start_y
    overflow_x, overflow_y = 0.0, 0.0
    
    for i in range(1, steps + 1):
        t = i / steps
        progress = ease_in_out(t)
        
        current_x = start_x + (x - start_x) * progress
        current_y = start_y + (y - start_y) * progress
        
        raw_delta_x = current_x - previous_x
        raw_delta_y = current_y - previous_y
        
        delta_x_total = raw_delta_x + overflow_x
        delta_y_total = raw_delta_y + overflow_y
        
        move_x = int(delta_x_total)
        move_y = int(delta_y_total)
        overflow_x = delta_x_total - move_x
        overflow_y = delta_y_total - move_y
        
        if move_x != 0 or move_y != 0:
            if not MoveMouse(driver_handle, move_x, move_y):
                print("\033[1;39m[\033[0;31mvn.dev\033[1;39m] Di chuyển chuột thất bại.")
                init()
                return
        
        previous_x = current_x
        previous_y = current_y
        
        time.sleep(0.002 / steps)
    
def get_screen_resolution():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize
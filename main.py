import mss
from PIL import Image
import ctypes
import time
import numpy as np
from consmath.logitech import *
import keyboard
from consmath.crackcailonmemay import *
import colorama
import pystyle
import os
import shutil
import subprocess
from time import sleep
import sys
import math
from flask import Flask, render_template, request, redirect, url_for
import logging
import threading

# Flask app initialization
app = Flask(__name__)

# Valid options for configuration
VALID_KEYS = [
    'x1', 'alt', 'ctrl', 'shift', 'chuot_trai', 'chuot_phai', 'x2', 
    'f1', 'f2', 'space'
]
VALID_COLORS = ['purple', 'yellow', 'red']

def read_config(file_path="config.txt"):
    config = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        config = {
            "Phim kich hoat": "x1",
            "Do nhay mau": "120",
            "FOV quet ngang": "65",
            "FOV quet doc": "30",
            "Mau dich": "purple",
            "Do muot (Cang cao cang muot)": "12",
            "offset Y": "4",
            "offset X": "0"
        }
    return config

def write_config(config, file_path="config.txt"):
    with open(file_path, "w", encoding="utf-8") as file:
        for key, value in config.items():
            file.write(f"{key}: {value}\n")

@app.route('/')
def index():
    config = read_config()
    return render_template('index.html', config=config, valid_keys=VALID_KEYS, valid_colors=VALID_COLORS)

@app.route('/save', methods=['POST'])
def save_config():
    config = read_config()
    
    # Update config with form data
    config["Phim kich hoat"] = request.form.get("Phim kich hoat", config["Phim kich hoat"])
    config["Do nhay mau"] = request.form.get("Do nhay mau", config["Do nhay mau"])
    config["FOV quet ngang"] = request.form.get("FOV quet ngang", config["FOV quet ngang"])
    config["FOV quet doc"] = request.form.get("FOV quet doc", config["FOV quet doc"])
    config["Mau dich"] = request.form.get("Mau dich", config["Mau dich"])
    config["Do muot (Cang cao cang muot)"] = request.form.get("Do muot (Cang cao cang muot)", config["Do muot (Cang cao cang muot)"])
    config["offset Y"] = request.form.get("offset Y", config["offset Y"])
    config["offset X"] = request.form.get("offset X", config["offset X"])
    
    # Validation
    try:
        do_nhay_mau = int(config["Do nhay mau"])
        if not (0 <= do_nhay_mau <= 255):
            return "Độ nhạy màu phải từ 0 đến 255", 400
        
        fov_ngang = int(config["FOV quet ngang"])
        fov_doc = int(config["FOV quet doc"])
        if fov_ngang <= 0 or fov_doc <= 0:
            return "FOV quét phải lớn hơn 0", 400
            
        do_muot = int(config["Do muot (Cang cao cang muot)"])
        if do_muot <= 0:
            return "Độ mượt phải lớn hơn 0", 400
            
        if config["Phim kich hoat"] not in VALID_KEYS:
            return "Phím kích hoạt không hợp lệ", 400
            
        if config["Mau dich"] not in VALID_COLORS:
            return "Màu đích không hợp lệ", 400
            
        offset_y = int(config["offset Y"])
        offset_x = int(config["offset X"])
        
    except ValueError:
        return "Giá trị số không hợp lệ", 400

    write_config(config)

    # Reload cấu hình và cập nhật banner ngay sau khi lưu
    try:
        supanigaplusplusplusfrvuapproved()
        print_banner()
    except Exception:
        pass

    # Nếu là AJAX (fetch) thì trả 200 để không reload trang
    requested_with = request.headers.get('X-Requested-With', '')
    if requested_with.lower() in ("xmlhttprequest", "fetch"):
        return ("OK", 200)
    # Ngược lại vẫn redirect như cũ
    return redirect(url_for('index', saved=1))

def run_flask():
    # Tắt log của werkzeug để console chỉ hiển thị banner
    try:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        log.disabled = True
        app.logger.disabled = True
        # Ẩn banner khởi động của Flask CLI
        try:
            from flask import cli
            cli.show_server_banner = lambda *args: None
        except Exception:
            pass
    except Exception:
        pass
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def dittosucanhacahonhamay():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not dittosucanhacahonhamay():
    print("Script cần chạy dưới quyền Administrator...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit(0)

def xinloividaditmemaykhongdeobao():
    driver_name = "vndev"
    source_path = os.path.abspath(os.path.join("consmath", "svchost.sys"))
    target_path = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "System32", "drivers", "svchost.sys")

    if os.path.exists(target_path):
        print(f"File đã tồn tại tại {target_path}, bỏ qua bước copy.")
    else:
        print(f"> Copy file từ {source_path} đến {target_path}")
        try:
            shutil.copy(source_path, target_path)
            print(f"Đã copy file thành công.")
        except PermissionError:
            print(f"Không đủ quyền để copy file vào {target_path}. Vui lòng chạy script dưới quyền Administrator.")
            sys.exit(1)
        except Exceptional as e:
            print(f"Lỗi khi copy file: {e}")
            sys.exit(1)

    os.system(f'sc stop {driver_name} >nul 2>&1')
    os.system(f'sc delete {driver_name} >nul 2>&1')

    create_cmd = f'sc create {driver_name} type=kernel start=demand binPath="{target_path}"'
    print(f"> {create_cmd}")
    os.system(create_cmd)

    start_cmd = f'sc start {driver_name}'
    print(f"> {start_cmd}")
    os.system(start_cmd)

user32 = ctypes.windll.user32

def fancy_loader(title="Đang khởi tạo", duration=2.5, width=32):
    start = time.time()
    spinner = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    spin_idx = 0
    while True:
        elapsed = time.time() - start
        progress = min(1.0, elapsed / max(0.001, duration))
        filled = int(width * progress)
        bar = "█" * filled + "░" * (width - filled)
        percent = int(progress * 100)
        line = f" {spinner[spin_idx]} {title} │{bar}│ {percent:3d}%"
        spin_idx = (spin_idx + 1) % len(spinner)
        print(Colorate.Horizontal(Colors.white_to_red, line, 1), end='\r', flush=True)
        if progress >= 1.0:
            break
        time.sleep(0.06)
    print(Colorate.Horizontal(Colors.white_to_red, " ✓ " + title + " hoàn tất" + " " * (width // 2), 1))

def vudungvapev4(filename="config.txt"):
    config = {}
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if ":" in line:
                key, value = line.strip().split(":", 1)
                config[key.strip()] = value.strip()
    return config

def vudungvapev4123(config, key):
    value = config.get(key)
    if value is None or not value.isdigit():
        raise ValueError(f"\033[1;39m[\033[0;31mvn.dev\033[1;39m] Giá trị đặt trong ({key}) không hợp lệ.")
        time.sleep(5)
    return int(value)

def khocdicon(config, key):
    value = config.get(key)
    if value not in ["True", "False"]:
        raise ValueError(f"\033[1;39m[\033[0;31mvn.dev\033[1;39m] Giá trị đặt trong ({key}) không hợp lệ. Chỉ chấp nhận 'True' hoặc 'False'.")
        time.sleep(5)
    return value == "True"

# Khởi tạo config ban đầu
config = vudungvapev4()
offsetY = vudungvapev4123(config, "offset Y")
offsetX = vudungvapev4123(config, "offset X")
aimbot_status = True
button_pressed = False
scan_area = (scan_area_x, scan_area_y)  # Cần lấy từ crackcailonmemay.py

def memaybitaoditchet():
    user32.mouse_event(0x0002 | 0x0004, 0, 0, 0, 0)

def taobecacbomay(color):
    if color == "purple":
        return np.array([250, 100, 250])
    elif color == "yellow":
        return np.array([254, 254, 64])
    elif color == "red":
        return np.array([170, 5, 8])
    return np.array([250, 100, 250])
    
def odaymadebugdefines(frame, color):
    target_color = taobecacbomay(color)
    color_diff = np.abs(frame - target_color)
    color_distance = np.sum(color_diff, axis=2)
    return color_distance < color_threshold  # Cần lấy color_threshold từ config
    
def memaynentusat():
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    center_x = screen_width // 2
    center_y = screen_height // 2
    return center_x, center_y

def aimfreedebuganlonbamayha(center_x, center_y, size):
    width, height = size
    with mss.mss() as sct:
        bbox = (center_x - width // 2, center_y - height // 2,
                center_x + width // 2, center_y + height // 2)
        sct_img = sct.grab(bbox)
        return np.array(Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX'))

def taouocgimemaykhitlonlai(screen, color):
    mask = odaymadebugdefines(screen, color)
    points = np.transpose(np.nonzero(mask))
    
    if len(points) > 0:
        min_y = np.min(points[:, 0])
        highest_points = points[points[:, 0] == min_y]
        distances = np.abs(highest_points[:, 1] - scan_area_x // 2)
        best_point = highest_points[np.argmin(distances)]
        x_diff = best_point[1] - scan_area_x // 2
        y_diff = best_point[0] - scan_area_y // 2
        x_adjusted = x_diff + offsetX
        y_adjusted = y_diff + offsetY
        return int(x_adjusted), int(y_adjusted)
    return None, None

def taouocbomaytusat():
    center_x, center_y = memaynentusat()
    screen = aimfreedebuganlonbamayha(center_x, center_y, scan_area)
    if screen is None:
        return None, None

    target_x, target_y = taouocgimemaykhitlonlai(screen, "purple")  # Lấy màu từ config
    if target_x is not None and target_y is not None:
        mouse_move(target_x, target_y)
        return target_x, target_y
    return None, None

if __name__ == "__main__":
    xinloividaditmemaykhongdeobao()
    fancy_loader("Đang tải driver & cấu hình", duration=2.8, width=36)
    print_banner()
    if not init():
        exit()

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Thêm biến theo dõi thời gian sửa đổi
    last_modified_time = os.path.getmtime("config.txt")

    while True:
        # Kiểm tra và tải lại config nếu có thay đổi
        if os.path.getmtime("config.txt") > last_modified_time:
            config = vudungvapev4()  # Tải lại config
            offsetY = vudungvapev4123(config, "offset Y")
            offsetX = vudungvapev4123(config, "offset X")
            # Cập nhật các biến khác từ config nếu cần
            last_modified_time = os.path.getmtime("config.txt")
            print("Config updated!")

        if not is_key_pressed():
            time.sleep(0.001)
            continue
        aimbot_x, aimbot_y = taouocbomaytusat()
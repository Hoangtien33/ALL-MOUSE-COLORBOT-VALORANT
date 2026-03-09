import os, sys
import subprocess
import shutil
from pathlib import Path
import requests
import threading
import ctypes
from omegaconf import OmegaConf
import yaml
import keyboard
import colorama
import time
from time import sleep
import pystyle
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from pynput.mouse import Listener, Button

user32 = ctypes.windll.user32

def read_config(config_path):
    config = {}
    with open(config_path, "r") as file:
        for line in file:
            if not line.strip() or ": " not in line:
                continue
            key, value = line.strip().split(": ", 1)
            if value.lower() in ["true", "false"]:
                config[key] = value.lower() == "true"
            elif value.isdigit():
                config[key] = int(value)
            else:
                config[key] = value
    return config
def supanigaplusplusplusfrvuapproved():
    global hold_key, color_threshold, scan_area_x, scan_area_y, color, smoothness, triggerbot, hold_mode
    try:
        config = read_config("config.txt")
    except FileNotFoundError:
        os.system('cls')
        print("\033[1;39m[\033[0;31mvn.dev\033[1;39m] \033[1;34mAimbot config \033[1;31mkhông \033[1;31mtồn tại\033[1;39m. Bắt đầu tải \033[0;31mconfig.txt")
        time.sleep(3)
        github_raw_url = "https://raw.githubusercontent.com/MCCFree/GG/refs/heads/main/configg"

        response = requests.get(github_raw_url)

        if response.status_code == 200:
            with open("config.txt", 'wb') as file:
                file.write(response.content)
            print("\033[1;39m[\033[0;31mvn.dev\033[1;39m] \033[1;34mAimbot config \033[1;39mđã được tải xuống.")
            time.sleep(2)
            try:
                config = read_config("config.txt")
            except subprocess.CalledProcessError as e:
                print(f"\033[1;39m[\033[0;31mvn.dev\033[1;39m] \033[1;39mLỗi: {e}")
                time.sleep(3)
            else:
                hold_key = config.get("Phim kich hoat", "alt")
                color_threshold = config.get("Do nhay mau", 85)
                scan_area_x = config.get("FOV quet ngang", 100) 
                scan_area_y = config.get("FOV quet doc", 100)
                color = config.get("Mau dich(Phai de nguyen la mau tim)", "purple")
                smoothness = config.get("Do muot (Cang cao cang muot)", 1)
                triggerbot = False
                hold_mode = False
                afterreadconfig()
        else:
            print("\033[1;39m[\033[0;31mvn.dev\033[1;39m] \033[1;39mLỗi bất định. báo cáo ngay cho dev: facebook.com/trumflorentinovucony")
            time.sleep(7)
    else:
        hold_key = config.get("Phim kich hoat", "alt")
        color_threshold = config.get("Do nhay mau", 85)
        scan_area_x = config.get("FOV quet ngang", 100) 
        scan_area_y = config.get("FOV quet doc", 100)
        color = config.get("Mau dich", "purple")
        smoothness = config.get("Do muot (Cang cao cang muot)", 1)
        triggerbot = False
        hold_mode = False
        afterreadconfig()
def afterreadconfig():
    global key 
    
    key = {
        # Mouse buttons
        "chuot_trai": 0x01,
        "chuot_phai": 0x02,
        "x1": 0x05,
        "x2": 0x06,
        # Number keys
        "0": 0x30,
        "1": 0x31,
        "2": 0x32,
        "3": 0x33,
        "4": 0x34,
        "5": 0x35,
        "6": 0x36,
        "7": 0x37,
        "8": 0x38,
        "9": 0x39,
        # Alphabet keys
        "a": 0x41,
        "b": 0x42,
        "c": 0x43,
        "d": 0x44,
        "e": 0x45,
        "f": 0x46,
        "g": 0x47,
        "h": 0x48,
        "i": 0x49,
        "j": 0x4A,
        "k": 0x4B,
        "l": 0x4C,
        "m": 0x4D,
        "n": 0x4E,
        "o": 0x4F,
        "p": 0x50,
        "q": 0x51,
        "r": 0x52,
        "s": 0x53,
        "t": 0x54,
        "u": 0x55,
        "v": 0x56,
        "w": 0x57,
        "x": 0x58,
        "y": 0x59,
        "z": 0x5A,
        # Control keys
        "backspace": 0x08,
        "delete": 0x2E,
        "down_arrow": 0x28,
        "enter": 0x0D,
        "esc": 0x1B,
        "home": 0x24,
        "insert": 0x2D,
        "left_alt": 0xA4,
        "left_ctrl": 0xA2,
        "left_shift": 0xA0,
        "page_down": 0x22,
        "page_up": 0x21,
        "right_alt": 0xA5,
        "right_ctrl": 0xA3,
        "right_shift": 0xA1,
        "space": 0x20,
        "tab": 0x09,
        "up_arrow": 0x26,
        # Function keys
        "f1": 0x70,
        "f2": 0x71,
        "f3": 0x72,
        "f4": 0x73,
        "f5": 0x74,
        "f6": 0x75,
        "f7": 0x76,
        "f8": 0x77,
        "f9": 0x78,
        "f10": 0x79,
        "f11": 0x7A,
        "f12": 0x7B,
    }

supanigaplusplusplusfrvuapproved()

def is_key_pressed():
    global hold_key, key
    key_code = key.get(hold_key.lower()) if isinstance(hold_key, str) else hold_key

    if key_code is None:
        print("\033[1;39m[\\033[0;31mvn.dev\033[1;39m] \033[1;39mKeybind bạn nhập vào không đúng với định dạng.")
        time.sleep(9999)

    state = user32.GetAsyncKeyState(key_code)
    return state & 0x8000 != 0
    
def disable_quickedit():
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
        
def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    #disable_quickedit()
    cachra = """                                        

                                WebUi http://127.0.0.1:5000/"""
    SUCCESS = "\x1b[38;5;255m[\x1b[32m+\x1b[38;5;255m]"
    whxyu = """                    
                
                                                      _            
                                    __   ___ __    __| | _____   __
                                    \ \ / / '_ \  / _` |/ _ \ \ / /
                                     \ V /| | | || (_| |  __/\ V / 
                                      \_/ |_| |_(_)__,_|\___| \_/  All Mouse - Paid
                                                                       
                                            DEV: TheThao09
    """
    print(Colorate.Horizontal(Colors.red_to_white, whxyu, 1))

    # Panel thong tin dep hon ngay duoi logo
    info_top_lines = [
        "Bạn đang sử dụng vn.dev all mouse aimbot.",
        "Nếu có bất cứ lỗi hay đóng góp, tìm tới dev tại: discord.gg/vietnamdev.",
    ]
    term_cols = shutil.get_terminal_size(fallback=(120, 30)).columns
    pad_h = 2
    inner_w_top = max(len(s) for s in info_top_lines) + pad_h * 2
    top_line = "╭" + ("─" * inner_w_top) + "╮"
    bottom_line = "╰" + ("─" * inner_w_top) + "╯"
    panel_width_top = inner_w_top + 2
    left_margin_top = " " * max(0, (term_cols - panel_width_top) // 2)
    print(Colorate.Horizontal(Colors.white_to_blue, left_margin_top + top_line, 1))
    for text in info_top_lines:
        content = text.center(inner_w_top, " ")
        print(Colorate.Horizontal(Colors.white_to_blue, left_margin_top + "│" + content + "│", 1))
    print(Colorate.Horizontal(Colors.white_to_blue, left_margin_top + bottom_line, 1))
    
    
    # Hien tat ca thong tin vao 1 khung dep, tu dong mo rong
    try:
        info_lines = [
            f"FOV: {scan_area_x}x{scan_area_y} (Ngang/Dọc)",
            f"Độ mượt: {smoothness}. Nên chỉnh độ nhạy trong game < 0.3",
            f"Aimbot: {hold_key}",
            "",
        ]

        config_pairs = [
            ("Độ nhạy màu", str(color_threshold)),
            ("FOV ngang", str(scan_area_x)),
            ("FOV dọc", str(scan_area_y)),
            ("Màu đích", str(color)),
        ]

        # Tinh toan do rong noi dung de can chuan
        title = " Thông tin & Cấu hình "
        border_char = "═"
        # left margin se tinh theo do rong console de can giua

        max_key_len = max(len(k) for k, _ in config_pairs)
        max_val_len = max(len(v) for _, v in config_pairs)

        key_val_width = max_key_len + 3 + max_val_len  # "key │ val"
        plain_lines_width = max((len(s) for s in info_lines), default=0)

        inner_width = max(key_val_width + 2, len(title) + 2, plain_lines_width)

        top_border = "╔" + border_char * inner_width + "╗"
        bottom_border = "╚" + border_char * inner_width + "╝"

        # can giua tieu de
        title_pad = inner_width - len(title)
        title_line = (
            "╠" + ("═" * (title_pad // 2)) + title + ("═" * (title_pad - title_pad // 2)) + "╣"
        )

        panel_width = inner_width + 2
        left_margin = " " * max(0, (term_cols - panel_width) // 2)
        print(Colorate.Horizontal(Colors.white_to_red, left_margin + top_border, 1))
        print(Colorate.Horizontal(Colors.white_to_red, left_margin + title_line, 1))

        # cac dong thong tin thuong
        for s in info_lines:
            content = s
            if len(content) < inner_width:
                content = content + (" " * (inner_width - len(content)))
            print(Colorate.Horizontal(Colors.white_to_red, left_margin + "║" + content + "║", 1))

        # duong phan cach giua thong tin va cau hinh
        mid_sep = "╟" + ("─" * inner_width) + "╢"
        print(Colorate.Horizontal(Colors.white_to_red, left_margin + mid_sep, 1))

        # dong key:value
        for key_name, value_str in config_pairs:
            kv = f"{key_name.ljust(max_key_len)} │ {value_str.rjust(max_val_len)}"
            content = f" {kv} "
            if len(content) < inner_width:
                content = content + (" " * (inner_width - len(content)))
            print(Colorate.Horizontal(Colors.white_to_red, left_margin + "║" + content + "║", 1))

        print(Colorate.Horizontal(Colors.white_to_red, left_margin + bottom_border, 1))
    except Exception:
        pass

    print(cachra)

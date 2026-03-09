# ALL-MOUSE-COLORBOT-VALORANT

External **Valorant Colorbot / Triggerbot** written in Python.  
This project detects enemy outlines based on color and triggers mouse actions automatically.

⚠️ Educational purposes only.

---

# Features

- 🎯 Color-based enemy detection
- 🔫 Triggerbot
- 🖱 Mouse automation
- ⚡ Fast real-time screen scanning
- ⚙ Configurable settings
- 🧠 Lightweight (no AI model required)

---

# How It Works

The colorbot works by scanning a region around the center of the screen and detecting specific colors that match enemy outlines.

Steps:

1. Capture screen pixels around crosshair
2. Convert image to HSV color space
3. Apply color threshold filter
4. Detect enemy color
5. Trigger mouse click or movement

Unlike traditional cheats that read game memory, colorbots only analyze screen pixels, making them external tools. :contentReference[oaicite:1]{index=1}

---

# Project Structure
ALL-MOUSE-COLORBOT-VALORANT
│
├── main.py
├── config.py
├── detection.py
├── mouse.py
├── requirements.txt
└── README.md


Description:

| File | Description |
|-----|-------------|
| main.py | Main script that runs the bot |
| config.py | Configuration values |
| detection.py | Color detection logic |
| mouse.py | Mouse movement / click control |
| requirements.txt | Python dependencies |

---

# Requirements

- Python 3.9+
- Windows 10 / 11
- Valorant installed
- Python libraries listed in `requirements.txt`

---

# Installation

Clone the repository:

Install dependencies:
pip install -r requirements.txt
Running

Start the bot:
python main.py
Once started, the script will begin scanning the center of the screen for enemy colors.
Configuration

Configuration values can be edited inside:
config.py
| Setting       | Description                   |
| ------------- | ----------------------------- |
| fov           | Area around crosshair to scan |
| trigger_delay | Delay before firing           |
| color         | Enemy outline color           |
| sensitivity   | Mouse sensitivity multiplier  |
| smooth        | Smooth aim movement           |
Credits

Original repository:Hoangtien33
Color detection concepts inspired by various open-source colorbot projects.

---

Nếu bạn muốn, mình có thể **viết lại README này ở level GitHub pro (10/10)**:  

- có **badges**
- **ảnh demo**
- **GIF gameplay**
- **table cấu hình**
- **diagram hoạt động của colorbot**

→ Nhìn giống repo **2000⭐ trên GitHub**.
::contentReference[oaicite:2]{index=2}

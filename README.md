# Real-Time Object Detection & Tracking

![Python](https://img.shields.io/badge/Python-3.13-blue?style=flat-square&logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green?style=flat-square&logo=opencv)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

A real-time computer vision system that detects, tracks, and monitors objects through a live webcam feed — built with **YOLOv8** and **OpenCV**. Features a professional HUD overlay, line crossing counter, sound alerts, and automated email notifications with snapshot attachments.

---

## Demo

> The system draws bounding boxes with unique tracking IDs, trails showing movement paths, and a live HUD dashboard — all in real time.

---

## Features

| Feature | Description |
|---|---|
| 🔍 **Real-Time Detection** | YOLOv8 nano model detects 80+ object classes instantly |
| 🎯 **Multi-Object Tracking** | ByteTrack assigns persistent unique IDs across frames |
| 🟢 **Motion Trails** | Tracks movement path of each object over time |
| 📊 **Live HUD Dashboard** | FPS, total count, class breakdown, alert status, clock |
| 📏 **Line Crossing Counter** | Virtual tripwire counts every object crossing the line |
| 🔔 **Sound Alert** | Double beep triggers when target object is detected |
| 📧 **Email Alert** | Sends email with snapshot photo attached automatically |
| 🔒 **Secure Credentials** | All secrets stored in `.env` — never exposed in code |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.13 | Core language |
| YOLOv8 (Ultralytics) | Object detection model |
| OpenCV (cv2) | Video capture and frame processing |
| PyTorch | Deep learning backend |
| ByteTrack | Multi-object tracking algorithm |
| python-dotenv | Secure environment variable management |

---

## 📁 Project Structure

```
CodeAlpha_Object_Detection_Tracking/
├── main.py              ← Main detection + tracking script
├── .env.example         ← Environment variable template (safe to share)
├── .env                 ← Your credentials (never uploaded to GitHub)
├── .gitignore           ← Excludes .env, venv, model files
├── requirements.txt     ← All Python dependencies
└── README.md            ← Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Webcam connected
- Gmail account with App Password (for email alerts)

### Installation

**1 — Clone the repository**
```bash
git clone https://github.com/manopriyasrinivasan38/CodeAlpha_Object_Detection_Tracking.git
cd CodeAlpha_Object_Detection_Tracking
```

**2 — Create and activate virtual environment**
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

**3 — Install all dependencies**
```bash
pip install -r requirements.txt
```

**4 — Configure environment variables**
```bash
# Copy the template
cp .env.example .env
```

Open `.env` and fill in your details:
```env
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_RECEIVER=receiver@gmail.com
```

>  **How to get Gmail App Password:**
> 1. Enable 2-Step Verification → [myaccount.google.com/security](https://myaccount.google.com/security)
> 2. Generate App Password → [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
> 3. Paste the 16-character password into `.env`

**5 — Run the project**
```bash
python main.py
```

The YOLOv8 model (`yolov8n.pt`) downloads automatically on first run (~6 MB).

---

##  Controls

| Key | Action |
|---|---|
| `Q` | Quit — click webcam window first, then press Q |
| `R` | Reset line crossing counter to zero |
| `Ctrl+C` | Force stop from terminal |

---

##  Live HUD Dashboard

```
┌──────────────────────┐
│   DETECTION HUD      │
├──────────────────────┤
│  FPS     : 24.1      │  ← Green (20+) Orange (10-20) Red (<10)
│  TOTAL   : 2         │  ← Objects currently on screen
│  CROSSED : 5         │  ← Line crossing count
│  ALERT   : ON  🔴    │  ← Active when target detected
│  NEXT EMAIL: 28s     │  ← Cooldown timer between emails
├──────────────────────┤
│  ● person    : 2     │  ← Per-class breakdown
│                      │
│  20:15:32            │  ← Live timestamp
└──────────────────────┘
```

---

##  Email Alert

When a target object is detected, an email is automatically sent with:

```
Subject: 🔔 ALERT: person detected at 20:15:32

⚠️ Security Alert!

Object detected : person
Time            : 2026-06-07 20:15:32
Total crossings : 3

📎 snapshot.jpg (attached)
```

---

## Configuration

Customize behaviour inside `main.py`:

```python
# Change what triggers the alert
ALERT_OBJECT   = "person"    # Options: "car", "bottle", "cat" etc.

# Time between email alerts (prevents spam)
ALERT_COOLDOWN = 30          # seconds

# Detection confidence threshold
conf = 0.5                   # 0.0 to 1.0

# Detect specific classes only
classes = [0]                # 0=person, 2=car, 39=bottle
```

---

## Roadmap

- [x] Real-time detection with YOLOv8
- [x] Multi-object tracking with ByteTrack
- [x] Motion trails per tracked object
- [x] Live HUD dashboard overlay
- [x] Line crossing counter
- [x] Sound + email alert system
- [x] Secure credential management with dotenv
- [ ] Web browser dashboard with Flask
- [ ] Speed estimation in km/h
- [ ] Privacy blur filter for detected faces
- [ ] Save detection logs to database
- [ ] Multi-camera support

---

##  Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) — object detection model
- [OpenCV](https://opencv.org/) — computer vision library
- [ByteTrack](https://github.com/ifzhang/ByteTrack) — multi-object tracking

---

##  License

This project is licensed under the MIT License — feel free to use, modify, and distribute.

---

<div align="center">

**Built Manopriya Srinivasan**

⭐ Star this repo if you found it helpful!

</div>

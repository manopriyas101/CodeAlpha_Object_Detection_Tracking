# 🎯 Real-Time Object Detection & Tracking

A real-time computer vision system built with **YOLOv8** and **OpenCV** that detects, tracks, and monitors objects through a webcam feed — with a live HUD dashboard, line crossing counter, and email alert system.

---

## 📸 Demo

> Point your webcam at any scene — the system instantly detects and tracks people and objects with unique IDs.

![Demo](snapshot.jpg)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Object Detection** | YOLOv8 detects 80+ object classes in real time |
| 🎯 **Object Tracking** | ByteTrack assigns unique IDs to each object |
| 📊 **Live HUD Dashboard** | FPS counter, object count, class breakdown, timestamp |
| 📏 **Line Crossing Counter** | Counts every object that crosses a virtual line |
| 🔔 **Smart Alert System** | Beep sound + red flash when target object detected |
| 📧 **Email Alerts** | Sends email with snapshot photo when alert triggers |
| 🔒 **Secure Credentials** | Passwords stored in `.env` file, never in source code |

---

## 🛠 Tech Stack

- **Python 3.13**
- **YOLOv8** (Ultralytics)
- **OpenCV** (cv2)
- **PyTorch**
- **python-dotenv**

---

## 📁 Project Structure

```
object-detection-tracking/
├── main.py              # Main detection + tracking script
├── .env.example         # Environment variable template
├── .gitignore           # Excludes .env, venv, model files
├── requirements.txt     # All dependencies
└── README.md            # This file
```

---

## 🚀 Getting Started

### 1 — Clone the repo
```bash
git clone https://github.com/YourUsername/object-detection-tracking.git
cd object-detection-tracking
```

### 2 — Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### 4 — Set up environment variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and fill in your Gmail credentials
```

Inside `.env`:
```
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
EMAIL_RECEIVER=receiver@gmail.com
```

> 📌 **Gmail App Password setup:**
> 1. Enable 2-Step Verification at [myaccount.google.com/security](https://myaccount.google.com/security)
> 2. Generate App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
> 3. Paste the 16-character password into `.env`

### 5 — Run
```bash
python main.py
```

---

## 🎮 Controls

| Key | Action |
|---|---|
| `Q` | Quit (click webcam window first) |
| `R` | Reset line crossing counter |

---

## 📊 HUD Dashboard

```
┌─────────────────────┐
│  DETECTION HUD      │
├─────────────────────┤
│  FPS     : 24.1     │  ← green/orange/red
│  TOTAL   : 2        │
│  CROSSED : 5        │  ← line crossing count
│  ALERT   : ON 🔴    │  ← active when detected
│  NEXT EMAIL: 28s    │  ← email cooldown timer
├─────────────────────┤
│  ● person    : 2    │
│                     │
│  20:15:32           │
└─────────────────────┘
```

---

## 📧 Email Alert Sample

```
Subject: 🔔 ALERT: person detected at 20:15:32

⚠️ Security Alert!
Object detected : person
Time            : 2026-06-07 20:15:32
Total crossings : 3

[snapshot.jpg attached]
```

---

## ⚙️ Configuration

Inside `main.py` you can customize:

```python
ALERT_OBJECT   = "person"   # Change to "car", "bottle" etc
ALERT_COOLDOWN = 30         # Seconds between email alerts
```

To detect specific classes only:
```python
# Detect only persons (class 0)
results = model.track(frame, persist=True, classes=[0], conf=0.5)

# Detect persons + cars (class 0 + 2)
results = model.track(frame, persist=True, classes=[0, 2], conf=0.5)
```

---

## 🔮 Future Improvements

- [ ] Web browser dashboard (Flask streaming)
- [ ] Speed estimation in km/h
- [ ] Privacy blur filter for faces
- [ ] Multi-camera support
- [ ] Database logging with timestamps

---

## 🙏 Credits

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [ByteTrack](https://github.com/ifzhang/ByteTrack)

---

## 📄 License

MIT License — feel free to use and modify for your own projects.

---

> Built  by Manopriya Srinivasan

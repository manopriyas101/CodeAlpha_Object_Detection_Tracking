# import cv2
# from ultralytics import YOLO

# # Load model (auto-downloads yolov8n.pt on first run)
# model = YOLO("yolov8n.pt")

# # Open webcam
# cap = cv2.VideoCapture(0)

# print("Press Q to quit")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Detect + Track
#     results = model.track(frame, persist=True, verbose=False)

#     # Draw boxes on frame
#     annotated = results[0].plot()

#     cv2.imshow("Object Detection", annotated)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
#for the full code with FPS, HUD, trails, and class counts, see the next cell below
# import cv2
# import time
# from ultralytics import YOLO
# from collections import defaultdict, deque

# model = YOLO("yolov8n.pt")
# cap = cv2.VideoCapture(0)

# prev_time = 0
# trails = defaultdict(lambda: deque(maxlen=30))

# print("Press Q to quit")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # --- FPS ---
#     curr_time = time.time()
#     fps = 1 / (curr_time - prev_time)
#     prev_time = curr_time

#     # --- Detection + Tracking ---
#     # results = model.track(frame, persist=True, verbose=False)
#     # results = model.track(frame, persist=True, verbose=False, classes=[0])
#     results = model.track(frame, persist=True, verbose=False, classes=[0], conf=0.6)
#     annotated = results[0].plot()

#     # --- Count objects per class ---
#     class_counts = defaultdict(int)
#     total = 0

#     for box in results[0].boxes:
#         label = model.names[int(box.cls)]
#         class_counts[label] += 1
#         total += 1

#         # Draw trails at BOTTOM CENTER (feet area = full body trail)
#         if box.id is not None:
#             tid = int(box.id)
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cx = (x1 + x2) // 2   # horizontal center
#             cy = y2 - 10           # bottom of box (feet), not face
#             trails[tid].append((cx, cy))
#             for i in range(1, len(trails[tid])):
#                 cv2.line(annotated, trails[tid][i-1], trails[tid][i], (0, 255, 200), 2)

#     # --- HUD Dashboard ---
#     h, w = annotated.shape[:2]
#     panel_w = 220
#     panel_h = 40 + (len(class_counts) * 28) + 60
#     panel_h = max(panel_h, 120)

#     # Semi-transparent dark background
#     overlay = annotated.copy()
#     cv2.rectangle(overlay, (10, 10), (10 + panel_w, 10 + panel_h), (20, 20, 20), -1)
#     cv2.addWeighted(overlay, 0.6, annotated, 0.4, 0, annotated)

#     # Border
#     cv2.rectangle(annotated, (10, 10), (10 + panel_w, 10 + panel_h), (0, 255, 200), 1)

#     # Title
#     cv2.putText(annotated, "DETECTION HUD", (20, 35),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 200), 2)

#     # Divider line
#     cv2.line(annotated, (15, 42), (panel_w, 42), (0, 255, 200), 1)

#     # FPS
#     fps_color = (0, 255, 0) if fps >= 20 else (0, 165, 255) if fps >= 10 else (0, 0, 255)
#     cv2.putText(annotated, f"FPS   : {fps:.1f}", (20, 65),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, fps_color, 1)

#     # Total count
#     cv2.putText(annotated, f"TOTAL : {total}", (20, 88),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

#     # Divider
#     cv2.line(annotated, (15, 96), (panel_w, 96), (60, 60, 60), 1)

#     # Per class counts
#     y = 118
#     colors = [(0,200,255),(0,255,100),(255,100,0),(200,0,255),(255,200,0),(0,165,255)]
#     for i, (cls, count) in enumerate(sorted(class_counts.items())):
#         color = colors[i % len(colors)]
#         # Small color dot
#         cv2.circle(annotated, (22, y - 4), 5, color, -1)
#         cv2.putText(annotated, f"{cls[:12]:<12}: {count}", (34, y),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
#         y += 26

#     # Bottom timestamp
#     clock = time.strftime("%H:%M:%S")
#     cv2.putText(annotated, clock, (20, 10 + panel_h - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.42, (120, 120, 120), 1)

#     cv2.imshow("Object Detection", annotated)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
import cv2
import time
import winsound
import threading
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from ultralytics import YOLO
from collections import defaultdict, deque
from dotenv import load_dotenv


model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)
prev_time = 0
trails = defaultdict(lambda: deque(maxlen=30))
LINE_Y = 300
cross_count = 0
prev_positions = {}
ALERT_OBJECT   = "person"
ALERT_COOLDOWN = 30        
last_alert_time = 0
alert_active    = False
from dotenv import load_dotenv
load_dotenv()
EMAIL_SENDER   = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def play_beep():
    winsound.Beep(1000, 300)
    winsound.Beep(1200, 300)
def send_email_alert(snapshot_path):
    """Send email with snapshot in background thread"""
    try:
        msg = MIMEMultipart()
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = EMAIL_RECEIVER
        msg["Subject"] = f"🔔 ALERT: {ALERT_OBJECT} detected at {time.strftime('%H:%M:%S')}"

        body = f"""
⚠️ Security Alert!

Object detected : {ALERT_OBJECT}
Time            : {time.strftime('%Y-%m-%d %H:%M:%S')}
Total crossings : {cross_count}

See attached snapshot.
        """
        msg.attach(MIMEText(body, "plain"))

    
        if os.path.exists(snapshot_path):
            with open(snapshot_path, "rb") as f:
                img = MIMEImage(f.read(), name="snapshot.jpg")
                msg.attach(img)

    
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print(f"📧 Email sent to {EMAIL_RECEIVER}")

    except Exception as e:
        print(f"❌ Email failed: {e}")

def trigger_alert(frame):
    global last_alert_time, alert_active
    now = time.time()
    if now - last_alert_time >= ALERT_COOLDOWN:
        last_alert_time = now
        alert_active = True

        snapshot_path = "snapshot.jpg"
        cv2.imwrite(snapshot_path, frame)

        threading.Thread(target=play_beep, daemon=True).start()
        threading.Thread(
            target=send_email_alert,
            args=(snapshot_path,),
            daemon=True
        ).start()

        print(f"🔔 ALERT: {ALERT_OBJECT} detected at {time.strftime('%H:%M:%S')}")
print("Press Q to quit | Press R to reset counter")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w = frame.shape[:2]
    LINE_Y = h // 2

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    results = model.track(frame, persist=True, verbose=False,
                          classes=[0], conf=0.5)
    annotated = results[0].plot()
    class_counts = defaultdict(int)
    total = 0
    alert_object_found = False

    for box in results[0].boxes:
        label = model.names[int(box.cls)]
        class_counts[label] += 1
        total += 1

        if label == ALERT_OBJECT:
            alert_object_found = True

        if box.id is not None:
            tid = int(box.id)
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2
            cy = y2 - 10

            trails[tid].append((cx, cy))
            for i in range(1, len(trails[tid])):
                cv2.line(annotated, trails[tid][i-1], trails[tid][i],
                         (0, 255, 200), 2)

            if tid in prev_positions:
                prev_cy = prev_positions[tid]
                if prev_cy < LINE_Y <= cy or prev_cy > LINE_Y >= cy:
                    cross_count += 1
            prev_positions[tid] = cy

    if alert_object_found:
        trigger_alert(frame)
    else:
        alert_active = False

    if alert_active:
        flash = annotated.copy()
        cv2.rectangle(flash, (0, 0), (w, h), (0, 0, 255), 20)
        cv2.addWeighted(flash, 0.3, annotated, 0.7, 0, annotated)
        cv2.rectangle(annotated, (w//2 - 160, h - 60),
                      (w//2 + 160, h - 15), (0, 0, 200), -1)
        cv2.putText(annotated, f"! {ALERT_OBJECT.upper()} DETECTED !",
                    (w//2 - 145, h - 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

   
    cv2.line(annotated, (0, LINE_Y), (w, LINE_Y), (0, 0, 255), 2)
    cv2.putText(annotated, "CROSSING LINE", (10, LINE_Y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

    panel_w = 220
    panel_h = max(40 + (len(class_counts) * 28) + 110, 185)

    overlay = annotated.copy()
    cv2.rectangle(overlay, (10, 10), (10 + panel_w, 10 + panel_h),
                  (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, annotated, 0.4, 0, annotated)
    cv2.rectangle(annotated, (10, 10), (10 + panel_w, 10 + panel_h),
                  (0, 255, 200), 1)

    cv2.putText(annotated, "DETECTION HUD", (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 200), 2)
    cv2.line(annotated, (15, 42), (panel_w, 42), (0, 255, 200), 1)

    fps_color = (0,255,0) if fps >= 20 else (0,165,255) if fps >= 10 else (0,0,255)
    cv2.putText(annotated, f"FPS     : {fps:.1f}", (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, fps_color, 1)
    cv2.putText(annotated, f"TOTAL   : {total}", (20, 88),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(annotated, f"CROSSED : {cross_count}", (20, 111),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    alert_color = (0, 0, 255) if alert_object_found else (100, 100, 100)
    alert_text  = "ALERT   : ON  *" if alert_object_found else "ALERT   : OFF"
    cv2.putText(annotated, alert_text, (20, 134),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, alert_color, 1)

    remaining = max(0, ALERT_COOLDOWN - int(time.time() - last_alert_time))
    cv2.putText(annotated, f"NEXT EMAIL: {remaining}s", (20, 155),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (150, 150, 150), 1)

    cv2.line(annotated, (15, 162), (panel_w, 162), (60, 60, 60), 1)

    y = 180
    colors = [(0,200,255),(0,255,100),(255,100,0),(200,0,255),(255,200,0)]
    for i, (cls, count) in enumerate(sorted(class_counts.items())):
        color = colors[i % len(colors)]
        cv2.circle(annotated, (22, y - 4), 5, color, -1)
        cv2.putText(annotated, f"{cls[:12]:<12}: {count}", (34, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
        y += 26

    cv2.putText(annotated, time.strftime("%H:%M:%S"),
                (20, 10 + panel_h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (120, 120, 120), 1)

    cv2.imshow("Object Detection", annotated)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        cross_count = 0
        print("Counter reset!")

cap.release()
cv2.destroyAllWindows()
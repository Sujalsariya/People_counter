import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import SimpleTracker

model = YOLO('yolov8n.pt')  # Load YOLOv8 nano model
tracker = SimpleTracker()

cap = cv2.VideoCapture(0)  # Use webcam

unique_ids = set()
frame_data = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, stream=True)
    detections = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            if cls == 0 and conf > 0.5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append([x1, y1, x2 - x1, y2 - y1])

    tracked = tracker.update(detections)

    for x, y, w, h, track_id in tracked:
        unique_ids.add(track_id)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, f'ID: {track_id}', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    count = len(unique_ids)
    cv2.putText(frame, f'People Count: {count}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    frame_data.append({'frame': len(frame_data), 'count': count})

    cv2.imshow("People Counter", frame)
    if cv2.waitKey(1) == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()

# Save count data
df = pd.DataFrame(frame_data)
df.to_csv("people_count.csv", index=False)
print("Saved to people_count.csv")

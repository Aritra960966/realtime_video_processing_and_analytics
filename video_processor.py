import os
import cv2
from tqdm import tqdm
from ultralytics import YOLO
import time

def process_video(input_video_path, output_dir, target_resolution=None):
    model = YOLO('yolov8n.pt')
    unique_id = time.strftime("%Y%m%d-%H%M%S")
    output_video_path = os.path.join(output_dir, f"{os.path.basename(input_video_path)}_out_{unique_id}.mp4")
    output_text_path = os.path.join(output_dir, f"{os.path.basename(input_video_path)}_out_{unique_id}.txt")
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {input_video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if target_resolution:
        width, height = target_resolution

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    with open(output_text_path, 'w') as f, tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if target_resolution:
                frame = cv2.resize(frame, (width, height))

            results = model(frame)
            detected_objects = []

            for result in results:
                boxes = result.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    class_id = int(box.cls[0].item())
                    label = model.names[class_id]
                    detected_objects.append(label)

                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            out.write(frame)
            f.write(f"{cap.get(cv2.CAP_PROP_POS_FRAMES)}: {', '.join(detected_objects)}\n")
            pbar.update(1)

    cap.release()
    out.release()
    return output_video_path, output_text_path

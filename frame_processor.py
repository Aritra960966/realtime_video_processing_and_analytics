import cv2
import torch
import torchvision

def process_frame(model, frame, device='cpu'):
    
    frame_resized = cv2.resize(frame, (640, 640))
    results = model(frame_resized, device=device)
    detected_objects = []

    for result in results:
        boxes = result.boxes

        if len(boxes.xyxy) > 0:
            boxes_xyxy = boxes.xyxy
            scores = boxes.conf
            nms_indices = torchvision.ops.nms(boxes_xyxy, scores, 0.5)

            for idx in nms_indices:
                x1, y1, x2, y2 = boxes.xyxy[idx].cpu().numpy().astype(int).tolist()
                class_id = int(boxes.cls[idx].item())
                label = model.names[class_id]
                detected_objects.append(label)

                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame, detected_objects

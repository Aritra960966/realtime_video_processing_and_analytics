from ultralytics import YOLO
import logging

def load_model():
    
    try:
        model = YOLO('yolov8n.pt')  
        logging.info("YOLO model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Error loading YOLO model: {e}")
        raise

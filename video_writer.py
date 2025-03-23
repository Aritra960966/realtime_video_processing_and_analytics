import cv2

def init_video_writer(output_path, width, height, fps):
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        raise ValueError(f"Error opening video writer for: {output_path}")
    return out

from ultralytics import YOLO

model = YOLO('yolov8n-seg.pt')

model.train(data="yolov8-bvn.yaml", epochs=100, workers=0, batch=16)
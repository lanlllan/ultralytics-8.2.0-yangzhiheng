from ultralytics import YOLO

model = YOLO("./runs/segment/train/weights/best.pt")
results = model.predict(source="./datasets/bvn/images/val/004-1-0.jpg", save=True)

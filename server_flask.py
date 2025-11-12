from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO('yolov8n.pt')


@app.route('/process_image', methods=['POST'])
def process_image():
    print("\n [SERVER] Cerere primita de la robot...")

    try:
        data = request.get_json()
        img_data = base64.b64decode(data['image'])
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print(" Imagine decodificata corect.")

        # Rulare model YOLO
        results = model(img)
        names = results[0].boxes.cls.tolist()
        detected = [model.names[int(i)] for i in names]

        print("Obiecte detectate:", detected)

        response = {'objects': list(set(detected))}
        print("Trimit raspuns:", response)
        return jsonify(response)

    except Exception as e:
        print(" Eroare la procesarea imaginii:", e)
        return jsonify({'objects': []})


if __name__ == '__main__':
    print(" Server Flask pornit pe http://0.0.0.0:5001")
    app.run(host='0.0.0.0', port=5001)

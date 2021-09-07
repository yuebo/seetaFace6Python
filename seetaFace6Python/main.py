from flask import Flask, Response, request
import json
from seetaface.api import *

app = Flask(__name__)


@app.route('/', methods=['get'])
def index():
    return Response("It works!")


@app.route('/recon', methods=['post'])
def recon():
    img1 = request.files.get('image1')
    img2 = request.files.get('image2')


    init_mask = FACE_DETECT | FACERECOGNITION | LANDMARKER5

    seetaFace = SeetaFace(init_mask)

    image1 = cv2.imdecode(np.frombuffer(img1.read(), np.uint8), 1)
    detect_result1 = seetaFace.Detect(image1)
    face1 = detect_result1.data[0].pos
    points1 = seetaFace.mark5(image1, face1)
    feature1 = seetaFace.Extract(image1, points1)

    image2 = cv2.imdecode(np.frombuffer(img2.read(), np.uint8), 1)
    detect_result2 = seetaFace.Detect(image2)
    face2 = detect_result2.data[0].pos
    points2 = seetaFace.mark5(image2, face2)
    feature2 = seetaFace.Extract(image2, points2)
    similar1 = seetaFace.CalculateSimilarity(feature1, feature2)
    # print(similar1)
    result = [{'result': similar1}]
    return Response(json.dumps(result), mimetype='application/json')

@app.route('/detect', methods=['post'])
def detect():
    img1 = request.files.get('image1')
    image = cv2.imdecode(np.frombuffer(img1.read(), np.uint8), 1)


    init_mask = FACE_DETECT | FACERECOGNITION | LANDMARKER5 | LANDMARKER_MASK |FACE_AGE |FACE_GENDER

    seetaFace = SeetaFace(init_mask)

    detect_result = seetaFace.Detect(image)
    list = []
    for i in range(detect_result.size):
        face = detect_result.data[i].pos
        points_5 = seetaFace.mark5(image, face)
        age = seetaFace.PredictAgeWithCrop(image, points_5)
        gender = seetaFace.PredictGenderWithCrop(image, points_5)
        points_mask = seetaFace.markMask(image, face)
        points, mask = points_mask
        mask_list = []
        for i in range(5):
            mask_list.append(mask[i])
        list.append({
            'pos': [face.x,face.y,face.width,face.height],
            'age': age,
            'gender': gender,
            'mask': mask_list
        })

    return Response(json.dumps({
        'faces': list
    }), mimetype='application/json')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

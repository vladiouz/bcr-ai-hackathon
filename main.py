from flask import Flask, request
from deepface import DeepFace
from flask_cors import CORS, cross_origin
import base64
from PIL import Image
from io import BytesIO
import cv2
from fer import FER
import numpy as np
from sklearn.linear_model import LinearRegression


app = Flask(_name_)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'sunt-smecher'


users = [
    {'name': 'Vlad',
     'email': 'vlad@eestec.com',
     'password': 'vladd',
     'contacts': ['Edi', 'Laur'],
     'spendings': [1600, 1800, 1750, 2000],
     'sold': {
         'curent': 900,
         'economii': 800,
         'credit': -200
     }
     },
    {'name': 'Edi',
     'email': 'edi@bcr.com',
     'password': 'edi',
     'contacts': ['Vlad', 'Laur'],
     'spendings': [1800, 2000, 2750, 3000],
     'sold': {
         'curent': 1200,
         'economii': 2000,
         'credit': -1000
     }
     },
    {'name': 'Laur',
     'email': 'laur@polaris.ro',
     'password': 'vladut',
     'contacts': ['Vlad', 'Edi'],
     'spendings': [1600, 1800, 2000, 2200],
     'sold': {
         'curent': 1000,
         'economii': 800,
         'credit': -400
     }
     }
]

face_match = False
message = "Ma bucur sa te revad!"


@app.route('/auth-by-pass', methods=['POST'])
@cross_origin()
def auth_user_by_pass():
    data = request.get_json()
    email = data['email']
    password = data['password']
    found_user = False
    password_is_good = False
    logged_user = None
    for user in users:
        if user['email'] == email:
            found_user = True
            if user['password'] == password:
                password_is_good = True
                logged_user = user
                break

    return {
        'user-exists': found_user,
        'logged-in': password_is_good,
        'user': logged_user,
        'message': message
    }


@app.route('/auth-by-img', methods=['POST'])
@cross_origin()
def auth_user_by_img():
    data = request.get_json()
    email = data['email']
    img = data['image']
    imgdata = base64.b64decode(img)
    img_name = 'test.jpg'
    test_img = Image.open(BytesIO(imgdata))
    test_img.save(img_name)
    ref_img = f'{email}.jpg'
    logged_user = None
    global message
    global face_match

    try:
        result = DeepFace.verify(img1_path=img_name, img2_path=ref_img)
        if result["verified"] and result["distance"] < 0.2:
            face_match = True
            for user in users:
                if user['email'] == email:
                    logged_user = user
                    image = cv2.imread(img_name)
                    detector = FER(mtcnn=True)
                    result = detector.detect_emotions(image)
                    max_emotion = "neutral"
                    for i, face in enumerate(result):
                        emotions = face["emotions"]
                        max_emotion = max(emotions, key=emotions.get)
                    if max_emotion == "happy":
                        message = "Vad ca esti intr-o stare buna"
                    elif max_emotion == "angry":
                        message = "N-ai de ce sa fii furios! In cateva zile iti intra salariul!"
                    elif max_emotion == "sad":
                        message = "Nu fi suparat! Tocmai ti s-a marit salariul!"
                    elif max_emotion == "neutral":
                        message = "Hai sa iti schimbam starea"
                    break
        else:
            face_match = False
    except ValueError:
        face_match = False
    return {
        'logged-in': face_match,
        'user': logged_user,
        'message': message
    }


@app.route('/ans-q', methods=['POST'])
@cross_origin()
def calculate_budget():
    data = request.get_json()
    user = data['user']
    input_text = data['text']

    transfer = "transferă"
    sold = "sold"
    buget = "buget"
    easter_egg = "ce sold voi avea eu mâine"

    response = None
    if transfer in input_text:
        amount = 0
        if input_text.startswith(transfer):
            for s in input_text.split():
                if s.isdigit():
                    amount = int(s)
                    break
            user['sold']['curent'] -= 100
            user['sold']['economii'] += 100
        else:
            for s in input_text.split():
                if s.isdigit():
                    amount = int(s)
                    break
            user['sold']['curent'] += 100
            user['sold']['economii'] -= 100
        response = "Operatie efectuata cu succes"

    elif input_text == easter_egg:
        sold_easter_egg = user['sold']['curent'] + user['sold']['economii']
        response = f'Daca e sa castigi, as zice vreo {sold_easter_egg} RON si 500 de euro'

    elif sold in input_text:
        sold_total = user['sold']['curent'] + user['sold']['economii']
        response = f"Soldul tau total este  {sold_total} RON"

    elif buget in input_text:
        user_expenses = user['spendings']
        x = np.array([[1], [2], [3], [4]])
        y = np.array(user_expenses)
        model = LinearRegression()
        model.fit(x, y)
        new_spending = np.array([[5]])
        predicted_spending = model.predict(new_spending)
        budget = predicted_spending[0]
        response = f'Bazandu-ma pe cheltuielile din ultimele 4 luni, ma astept sa cheltuiesti {budget} RON luna care vine'


    return {
        'predict': response,
        'curent': user['sold']['curent'],
        'economii': user['sold']['economii']
    }


if _name_ == "_main_":
    app.run(debug=True)

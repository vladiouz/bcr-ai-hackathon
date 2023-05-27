from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager
import threading
import cv2
from deepface import DeepFace


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sunt-smecher'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


# # face recognition
# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
#
# counter = 0
# face_match = False
# ref_img = cv2.imread("laur.jpg")
#
#
# def check_face(frame):
#     global face_match
#     try:
#         result = DeepFace.verify(frame, ref_img.copy())
#         if result["verified"] and result["distance"] < 0.2:
#             face_match = True
#         else:
#             face_match = False
#     except ValueError:
#         face_match = False
#
#
# while True:
#     ret, frame = cap.read()
#
#     if ret:
#         if counter % 30 == 0:
#             try:
#                 threading.Thread(target=check_face, args=(frame.copy(),)).start()
#             except ValueError:
#                 pass
#         counter += 1
#
#         if face_match:
#             cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
#         else:
#             cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
#
#         cv2.imshow("video", frame)
#
#     key = cv2.waitKey(1)
#     if key == ord("q"):
#         break
#
# cv2.destroyAllWindows()

# # laur
# import speech_recognition as sr
#
# # Crearea unui obiect Recognizer
# r = sr.Recognizer()
#
#
# # Funcția pentru conversia de la discurs la text
# def speech_to_text():
#     with sr.Microphone() as source:
#         print("Începeți vorbirea:")
#         audio = r.listen(source)
#
#     try:
#         # Utilizarea Google Speech Recognition pentru conversie
#         text = r.recognize_google(audio, language='ro-RO')
#         print("Textul detectat:", text)
#     except sr.UnknownValueError:
#         print("Nu am putut detecta textul.")
#     except sr.RequestError as e:
#         print("Eroare la obținerea rezultatelor de la serviciul Google Speech Recognition; {0}".format(e))
#
#
# # Apelul funcției pentru conversia de la discurs la text
# speech_to_text()

if __name__ == "__main__":
    app.run(debug=True)

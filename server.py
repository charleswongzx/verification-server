import os

from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_mail import Mail, Message
from flask_autodoc import autodoc
from flask_cors import CORS, cross_origin

import gunicorn

from firebase import firebase

import cognitive_face as cf

# Server Gubbins
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
auth = HTTPBasicAuth()
ionic_app_url = 'https://www.google.com'
auto = autodoc.Autodoc(app)


# Firebase Helper (http://ozgur.github.io/python-firebase/)
db = firebase.FirebaseApplication('https://kyc-app-db.firebaseio.com/', None)


# Azure Face API Details
KEY = 'be8a2049b2e24dc3a42b041739af2ed0'
cf.Key.set(KEY)
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
cf.BaseUrl.set(BASE_URL)
example_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'


# Email Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sutd.myfaceapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'myface2018!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# API ENDPOINTS
@app.route('/api/v1/new-user-submit/', methods=['PUT'])
@cross_origin()
@auto.doc()
def new_user_submit():  # acknowledges new user and sends confirmation email
    user_email = request.form.get('email')
    user_uid = request.form.get('uid')

    db.put('/users/'+user_uid, 'email_confirmed', False)

    return jsonify(send_email_confirmation(user_email, user_uid))


@app.route('/api/v1/new-kyc-submit/', methods=['POST'])
@cross_origin()
@auto.doc()
def new_kyc_submit():
    user_uid = request.form.get('uid')
    user_email = db.get('/users/'+user_uid, 'email_address')
    selfie_url = request.form.get('selfie_url')
    passport_url = request.form.get('passport_url')

    result = verify_faces(selfie_url, passport_url)

    if result[0]:
        db.put('/users/'+user_uid, 'kyc_status', 'APPROVED')
        send_email_verify_success(user_email)
        return jsonify('KYC APPROVED')
    else:
        db.put('/users/'+user_uid, 'kyc_status', 'REJECTED')
        send_email_verify_fail(user_email, result[1])
        return jsonify('KYC REJECTED')


# PAGE ROUTING
@app.route('/new-user-confirm/')
@cross_origin()
@auto.doc()
def new_user_confirm():
    user_uid = request.args.get('uid')
    response = ''
    if not user_uid:
        response = 'No uid in header!'
    else:
        exists = db.get('/users/', user_uid)

    if exists:
        db.put('/users/'+user_uid, 'email_confirmed', True)
    else:
        response = 'No such user exists!'

    # TODO: implement redirection to ionic app
    response = 'Email confirmation successful! Redirecting to MyFace to login...'
    return response


@app.route('/documentation')
def documentation():
    return auto.html()


@app.route('/')
@cross_origin()
@auto.doc()
def hello_world():
    # return 'Welcome to the MyFace Verification Server!'
    # print(send_email('charlescrinkle@gmail.com', '123'))
    return 'Welcome to the MyFace Verification Server!'


# UTILITY FUNCTIONS
def send_email_confirmation(email, uid):
    msg = Message('MyFace Confirmation',
                  sender='sutd.myfaceapp.gmail.com',
                  recipients=[email])

    msg.html = "<b>Thank you for registering with MyFace Verification!</b> <br>" \
               "We're here for all your KYC/AML needs. <br><br>" \
               "Please click on the following link to confirm your email:<br>" \
               ""+request.base_url+'new-user-confirm/?uid='+uid
    try:
        mail.send(msg)
        result = 'Email success'
    except Exception:
        result = 'Email failed'

    return result


def send_email_verify_success(email):
    msg = Message('MyFace KYC Success',
                  sender='sutd.myfaceapp.gmail.com',
                  recipients=[email])

    msg.html = "<b>Thank you for verifying with MyFace KYC!</b><br>" \
               "Your application was successful!<br><br>" \
               "Click here to proceed to login:<br>" \
               ""+ionic_app_url
    try:
        mail.send(msg)
        result = 'Email success'
    except Exception:
        result = 'Email failed'

    return result


def send_email_verify_fail(email, error_msg):
    msg = Message('MyFace KYC Rejection',
                  sender='sutd.myfaceapp.gmail.com',
                  recipients=[email])

    msg.html = "<b>Thank you for verifying with MyFace KYC.</b><br>" \
               "Unfortunately, your application was not successful due to the following:<br><br>" \
               "<b><i>"+error_msg+"</i></b><br><br>" \
               "Click here to login and try again:<br>" \
               ""+ionic_app_url
    try:
        mail.send(msg)
        result = 'Email success'
    except Exception:
        result = 'Email failed'

    return result


def verify_faces(selfie_url, passport_url):  # Face API Handling
        selfie_faces = cf.face.detect(selfie_url)
        selfie_face_id = selfie_faces[0][u'faceId']

        passport_faces = cf.face.detect(passport_url)
        passport_face_id = passport_faces[0][u'faceId']

        result = cf.face.verify(selfie_face_id, passport_face_id)

        confidence = result["confidence"]

        if result["isIdentical"]:
            if confidence > 0.98:
                return [False, "Rejected: Possible duplicate images. Ensure selfie image is front facing photo of user.", confidence]
            else:
                return [True, "Verified", confidence]

        elif not result["isIdentical"]:
            return [False, "Rejected: No facial match. Try a clearer picture or passport scan.", confidence]


if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True, use_reloader=True)

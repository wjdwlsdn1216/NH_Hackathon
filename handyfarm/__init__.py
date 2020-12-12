from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# 서버가 처음 시작되었을 때 코드가 실행되는 부분 
app = Flask(__name__)
app.config['SECRET_KEY']='330d954d8841ddadbd31dc6af3b17a70'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db' # sqlite database
# app.config['GOOGLE_OAUTH2_CLIENT_SECRETS_FILE'] = 'client_secret_987437859230-27us8hduggjaek6euqs9f6fnin0ackph.apps.googleusercontent.com.json'
# app.config['GOOGLE_OAUTH2_CLIENT_ID'] = '987437859230-27us8hduggjaek6euqs9f6fnin0ackph.apps.googleusercontent.com'
# app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = 'rpVNJwir02W2BF9gaURRDXIe'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app) #해쉬값 생성
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'



from handyfarm import routes
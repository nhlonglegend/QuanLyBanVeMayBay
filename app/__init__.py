from flask import  Flask,Markup
from flask_sqlalchemy import SQLAlchemy
from  flask_admin import  Admin
from flask_login import LoginManager
from flask_mail import Mail,Message
from datetime import  time
from flask_googlecharts import GoogleCharts
import smtplib

app = Flask(__name__)
app.secret_key = "Q\xcd&3XO\x00S \xc9\x9c\xfc\x96\xd3q\xaf\x8d"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:123456@localhost/saleflightticket?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app,name="Quan Ly Ban Ve May Bay", template_mode="bootstrap3")

login = LoginManager(app=app)

    # DEBUG =True,
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"]= 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USERNAME"] = 'nguyenhoanglonglegend@gmail.com'
app.config["MAIL_PASSWORD"] = 'legend99'

mail = Mail(app)

charts = GoogleCharts(app)
charts.init_app(app)
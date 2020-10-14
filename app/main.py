from tkinter.messagebox import Message
from Tools.scripts.make_ctype import method
from flask import render_template, redirect, request,session
from flask_login import login_user, login_required
from mysql import connector
from flask_mail import Message
from flask_googlecharts import BarChart
from app import mail


from app import app, login, dao, charts
from app.dao import read_chuyenbay
from app.models import *
import hashlib


@app.route("/")
def index():
    form = Form()
    form.San_Bay_Di.choices = [(San_Bay_Di.San_Bay_Di) for San_Bay_Di in ChuyenBay.query.all()]
    form.San_Bay_Den.choices = [(San_Bay_Den.San_Bay_Den) for San_Bay_Den in ChuyenBay.query.all()]
    return render_template("index.html", form = form, cacchuyenbay1= form.San_Bay_Di.choices, cacchuyenbay2 = form.San_Bay_Den.choices,
                           len1 = len(form.San_Bay_Di.choices), len2=len(form.San_Bay_Den.choices), latest_products = dao.read_ChuyenBay_show(latest=True))


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method =='POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = Admin.query.filter(Admin.username == username.strip(),
                                 Admin.password == password).first()
        if user:
            if user.active== 1:
                login_user(user=user)
            if user.active== 0:
                return render_template("index.html")

    return redirect("/admin")


@app.route("/search", methods=['GET', 'POST'] )
def search():
    if request.method == 'POST':
        San_Bay_Di = request.form['San_Bay_Di']
        San_Bay_Den = request.form['San_Bay_Den']

        return render_template("Search.html",chuyenbay = dao.read_chuyenbay(San_Bay_Di=San_Bay_Di,San_Bay_Den=San_Bay_Den))


@login.user_loader
def user_load(user_id):
    return Admin.query.get(user_id)


@app.route("/templates/customer",methods=['GET', 'POST'] )
def info():

    return render_template("customer_information.html")


@app.route('/insert', methods=['GET','Post'])
def insert():

     Quy_Danh = request.form['Quy_Danh']
     Ten_Khach_Hang = request.form['Ten_Khach_Hang']
     Dia_Chi = request.form['Dia_Chi']
     CMND = request.form['CMND']
     Email = request.form['Email']
     SDT = request.form['SDT']
     Ghi_Chu = request.form['Ghi_Chu']
     if request.method == 'POST':
         msg = Message("Email xác nhận", sender="webbanve@gmail.com", recipients=[Email])
         msg.html = render_template('email.html',Quy_Danh=Quy_Danh,Ten_Khach_Hang=Ten_Khach_Hang,Dia_Chi = Dia_Chi,
                                    CMND = CMND,Email = Email,SDT = SDT,Ghi_Chu = Ghi_Chu)
         mail.send(msg)

     return render_template("customer_information.html",info=dao.add_Khachhang(Quy_Danh=Quy_Danh,
                                                                               Ten_Khach_Hang=Ten_Khach_Hang,
                                                                               Dia_Chi = Dia_Chi,CMND = CMND,
                                                                               Email = Email,SDT = SDT,Ghi_Chu = Ghi_Chu))


@app.route("/logout")
def logout():
    session["user"]=None
    return render_template("index.html")


@app.route("/simple_chart", methods=['GET','Post'] )
def chart():
    legend = 'Monthly Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('admin/abous-us.html', values=values, labels=labels, legend=legend)


@app.route("/thanhtoan")
def payurl():

    return render_template("testmomo.html", res=dao.payment_momo())


if __name__=="__main__":
    app.run(debug=True)


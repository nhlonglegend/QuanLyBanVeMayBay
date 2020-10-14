from msilib import type_nullable

from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, Boolean,Date
from sqlalchemy.orm import relationship

from app import db, admin

from flask import render_template
from flask import redirect

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin,current_user, logout_user

from flask_wtf import FlaskForm
from wtforms import SelectField


class Admin(db.Model, UserMixin):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    Ve_id = relationship('Ve', backref='admin', lazy=True)


    def __str__(self):
        return self.name


class KhachHang(db.Model):
    __tablename__ = "khachhang"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Quy_Danh = Column(String(100), nullable=False)
    Ten_Khach_Hang = Column(String(200), nullable=False)
    Dia_Chi = Column(String(200), nullable=True)
    CMND = Column(Integer, nullable=False)
    Email = Column(String(50), nullable=False)
    SDT = Column(Integer, nullable=False)
    Ghi_Chu = Column(String(50), nullable=False)
    Phieu_Dat_Cho = relationship('PhieuDatCho', backref='khachhang', lazy=True)
    Hanh_Ly = relationship('HanhLy', backref='khachhang', lazy=True)
    def __str__(self):
        return self.Ten_Khach_Hang

class HanhLy(db.Model):
    __tablename__ = "hanhly"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Thong_Tin_Hanh_Ly = Column(String(150),nullable=False)

    Khach_Hang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)

class SanBay(db.Model):
    __tablename__ = "sanbay"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Ten_San_Bay = Column(String(100), nullable=True)

    chuyen_bay = db.relationship('ChuyenBay', primaryjoin='or_(SanBay.id==ChuyenBay.San_Bay_Di_id, SanBay.id==ChuyenBay.San_Bay_Den_id)',
                              lazy = False) #'dynamic')

    def __str__(self):
        return self.Ten_San_Bay

class ChuyenBay(db.Model):
    __tablename__ = "chuyenbay"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name=Column(String(100),nullable=False)
    Thoi_Gian_Bay = Column(Time, nullable=True)
    Ngay_Bay = Column(Date, nullable=True)
    So_Luong_Ghe_Loai_1 = Column(Integer, default= 60, nullable=False)
    So_Luong_Ghe_Loai_2 = Column(Integer, default= 70,  nullable=False)
    Gia_Ve_Loai_1 = Column(Float, nullable=False)
    Gia_Ve_Loai_2 = Column(Float, nullable=False)
    Phieu_Dat_Cho_id = relationship('PhieuDatCho', backref='chuyenbay', lazy=True)


    San_Bay_Di_id = Column(Integer, ForeignKey('sanbay.id'), nullable=False)
    San_Bay_Den_id = Column(Integer, ForeignKey('sanbay.id'), nullable=False)

    San_Bay_Di = db.relationship('SanBay', foreign_keys='ChuyenBay.San_Bay_Di_id')
    San_Bay_Den = db.relationship('SanBay', foreign_keys='ChuyenBay.San_Bay_Den_id')

    def __str__(self):
        return self.name


class PhieuDatCho(db.Model):
    __tablename__ = "phieudatcho"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Khach_Hang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    Ma_Chuyen_Bay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    Hang_Ve = Column(String(50), nullable=False)
    Gia_Tien = Column(Float, nullable=False)
    Thoi_Gian_Dat_ve = Column(Date, nullable=True)
    Thoi_Gian_Huy_Ve =Column(Date, nullable=False)
    Co_Hieu_Luc = Column(Boolean, nullable=False)
    Ve_id = relationship('Ve', backref='PhieuDatCho', lazy=True)


class LichSuGiaoDich(db.Model):
    __tablename__ = "lichsugiaodich"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Ma_Chuyen_Bay = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    Ngay_Bay = Column(Date, nullable=True)
    Ma_Phieu_Dat_Cho_id = Column(Integer, ForeignKey(PhieuDatCho.id), nullable=False)



class Ve(db.Model):
    __tablename__ = "ve"
    id = Column(Integer, primary_key=True, autoincrement=True)
    Ma_Phieu_Dat_Cho_id = Column(Integer, ForeignKey(PhieuDatCho.id), nullable=False)
    Ma_Ghe = Column(String(50), nullable=False)
    Hang_ve = Column(String(50), nullable=False)
    Thue = Column(Float, nullable=False)
    Gia_Tien = Column(Float, nullable=False)
    Account_id= Column(Integer, ForeignKey(Admin.id),nullable=False)


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class SanBayModelView(AuthenticatedView):
    column_display_pk = True
    can_create = True
    can_export = True
    form_columns = ('Ten_San_Bay',)


class ChuyenBayModelView(AuthenticatedView):
    can_create = True
    can_export = True
    form_columns = ('San_Bay_Di','San_Bay_Den','name','Ngay_Bay','Thoi_Gian_Bay','So_Luong_Ghe_Loai_1','So_Luong_Ghe_Loai_2','Gia_Ve_Loai_1','Gia_Ve_Loai_2')


class PhieuDatChoModelView(AuthenticatedView):
    form_columns = ('Thoi_Gian_Dat_ve','Thoi_Gian_Huy_Ve')


class AboutUsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose("/")
    def index(self):
         
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


class Form(FlaskForm):
    San_Bay_Di = SelectField('San_Bay_Di', choices=[])
    San_Bay_Den = SelectField('San_Bay_Den', choices=[])


admin.add_view(SanBayModelView(SanBay, db.session))
admin.add_view(ChuyenBayModelView(ChuyenBay, db.session))
admin.add_view(PhieuDatChoModelView(PhieuDatCho, db.session))
admin.add_view(AboutUsView(name="Thống Kê"))
admin.add_view(LogoutView(name="Logout"))
if __name__ == "__main__":
    db.create_all()



from spotify.extendtions import db,whooshee
from datetime import datetime
from flask_login import UserMixin


class Admin(db.Model,UserMixin):
    username=db.Column(db.String(128),primary_key=True)
    passwrod=db.Column(db.String(128))

    def get_id(self):
        return self.username

@whooshee.register_model('email','status')
class Order(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(128))
    password=db.Column(db.String(128))
    link=db.relationship('Link',uselist=False,backref='order')
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)
    expiretime=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(32),default='正在处理')



class Link(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    infos=db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    times=db.Column(db.Integer,default=5)
    order_id=db.Column(db.Integer,db.ForeignKey('order.id'))



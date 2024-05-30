from flask_sqlalchemy import SQLAlchemy
from main import db
from blueprints.constant import displayTime
from datetime import datetime

class Passcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(80), nullable=False)
    passcode = db.Column(db.String(120), unique=True, nullable=False)
    accessto = db.Column(db.String(), nullable=False)
    startDate = db.Column(db.Integer)
    endDate = db.Column(db.Integer)
    sendDate = db.Column(db.Integer)

    def __repr__(self):
        return '<Passcode %r>' % self.passcode
    
    def serialize(self, timestamp):
        status = ''
        if timestamp >= self.startDate:
            if timestamp <= self.endDate:
                status = 'In use'
            else:
                status = 'Expired'
        else:
            status = 'In use'

        return {
            'id': self.id,
            'owner': self.owner,
            'passcode': self.passcode,
            'status': status,  
            'validity': displayTime(self.startDate) + '~' + displayTime(self.endDate),
            'createDate': displayTime(self.sendDate),
            'accessto': self.accessto
        }


def getPasscode(owner, startDate, endDate, accessto):
    query = Passcode.query 
    if owner != '':
        query = query.filter(Passcode.owner.like('${owner}%'))
    if startDate != -1 and endDate != -1:
        query = query.filter(Passcode.startDate >= startDate).filter(Passcode.endDate <= endDate)
    if accessto != '':
        query = query.filter(Passcode.accessto.like('${accessto}%'))
    data = query.order_by(Passcode.id).all()
    
    serialized_data = [item.serialize(datetime.now().timestamp()) for item in data]
    return {
        'data' : serialized_data,
        'total' : serialized_data.__len__()
    }
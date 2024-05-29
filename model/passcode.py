from flask_sqlalchemy import SQLAlchemy
from main import db
from blueprints.constant import displayTime

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
    
    def serialize(self):
        return {
            'id': self.id,
            'owner': self.owner,
            'passcode': self.passcode,
            'startDate': displayTime(self.startDate),
            'endDate': displayTime(self.endDate),
            'sendDate': displayTime(self.sendDate),
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
    serialized_data = [item.serialize() for item in data]
    return serialized_data
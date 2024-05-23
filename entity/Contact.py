from datetime import datetime
from api import db


# Define the Contact entity
class Contact(db.Model):
    __tablename__ = 'contacts'
    __table_args__ = {'schema': 'identity'}

    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String)
    email = db.Column(db.String)
    linkedId = db.Column(db.Integer)
    linkPrecedence = db.Column(db.String)
    createdAt = db.Column(db.DateTime, default=datetime.now())
    updatedAt = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    deletedAt = db.Column(db.DateTime)

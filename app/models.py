'''
Class for model -> database schema
'''

from app import db

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(120) )
    value1 = db.Column(db.String(120), index=True)
    value2 = db.Column(db.Float)
    value3 = db.Column(db.Boolean)
    creationDate = db.Column(db.String(120))
    lastModificationDate = db.Column(db.String(120))

    def __repr__(self):
        return '<Post %s>' % self.value1

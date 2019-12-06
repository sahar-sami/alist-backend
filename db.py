from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#tip: see what happens if you do it as a single model with each type of media as a column

class Celeb(db.Model):
    __tablename__ = 'celeb'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    profile_pic = db.Column(db.String)
    photo = db.Column(db.String)
    instagram = db.Column(db.String)
    twitter = db.Column(db.String)
    spotify = db.Column(db.String)
    website = db.Column(db.String)
    other = db.Column(db.String)
    ##media = db.relationship('Media', cascade = 'delete')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.profile_pic = kwargs.get('profile_pic', None)
        self.photo = kwargs.get('photo', None)
        self.instagram = kwargs.get('instagram', None)
        self.twitter = kwargs.get('twitter', None)
        self.spotify = kwargs.get('spotify', None)
        self.website = kwargs.get('website', None)
        self.other = kwargs.get('other', None)

    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'profile_pic': self.profile_pic,
                'photo': self.photo,
                'instagram': self.instagram,
                'twitter': self.twitter,
                'spotify': self.spotify,
                'website': self.website,
                'other': self.other
            }



##class Media(db.Model):
##    __tablename__ = 'media'
##    id = db.Column(db.Integer, primary_key=True)
##    mtype = db.Column(db.String, nullable=False)
##    link = db.Column(db.String, nullable=False)
##    celeb_id = db.Column(db.Integer, db.ForeignKey('celeb.id'), nullable=False)
##
##    def __init__(self, **kwargs):
##        self.mtype = kwargs.get('type', '')
##        self.link = kwargs.get('link', '')
##
##    def serialize(self):
##        return {
##            'id': self.id,
##            'type': self.mtype,
##            'link': self.link 
##            }


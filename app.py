import json
from db import db, Celeb
from flask import Flask, request

db_filename = "celebmedia.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/api/celebs/')
def get_celebs():
    celebs = Celeb.query.all()
    res = {'success': True, 'data': [c.serialize() for c in celebs]}
    return json.dumps(res), 200
    
@app.route('/api/celebs/', methods=['POST'])
def add_celeb():
    post_body = json.loads(request.data)
    name = post_body['name']
    profile_pic = post_body.get('profile_pic', None)
    photo = post_body.get('photo', None)
    instagram = post_body.get('instagram', None)
    twitter = post_body.get('twitter', None)
    spotify = post_body.get('spotify', None)
    website = post_body.get('website', None)
    other = post_body.get('other', None)
    celeb = Celeb(
        name = name,
        profile_pic = profile_pic,
        photo = photo,
        instagram = instagram,
        twitter = twitter,
        spotify = spotify,
        other = other
        )
    db.session.add(celeb)
    db.session.commit()
    return json.dumps({'success': True, 'data': celeb.serialize()}), 200

@app.route('/api/celebs/<int:c_id>/')
def get_celeb(c_id):
    celeb = Celeb.query.filter_by(id=c_id).first()
    if not celeb:
        return json.dumps({'success': False, 'error': 'Celeb not found!'}), 404
    return json.dumps({'success': True, 'data': celeb.serialize()}), 200

@app.route('/api/celebs/<int:c_id>/', methods=['DELETE'])
def delete_celeb(c_id):
    celeb = Celeb.query.filter_by(id=c_id).first()
    if not celeb:
        return json.dumps({'success': False, 'error': 'Course not found!'}), 404
    db.session.delete(celeb)
    db.session.commit()
    return json.dumps({'success': True, 'data': celeb.serialize()}), 200

@app.route('/api/celebs/<int:c_id>/media/')
def get_celeb_media(c_id):
    celeb = Celeb.query.filter_by(id=c_id).first()
    if not celeb:
        return json.dumps({'success': False, 'error': 'Celeb not found!'}), 404
    result = {
        'instagram': celeb.instagram,
        'twitter': celeb.twitter,
        'spotify': celeb.spotify,
        'website': celeb.website,
        'other': celeb.other
        }
    return json.dumps({'success': True, 'data': result}), 200

@app.route('/api/celebs/<int:c_id>/media/<string:media_type>/')
def get_indiv_celeb_media(c_id, media_type):
    celeb = Celeb.query.filter_by(id=c_id).first()
    if not celeb:
        return json.dumps({'success': False, 'error': 'Celeb not found!'}), 404
    possible_media = {
        'instagram': celeb.instagram,
        'twitter': celeb.twitter,
        'spotify': celeb.spotify,
        'website': celeb.website,
        'other': celeb.other
        }
    if media_type not in possible_media:
        return json.dumps({'success': False, 'error': 'Not a valid media type'}), 404
    media = possible_media[media_type]
    if not media:
        return json.dumps({'success': False, 'error': 'Media not found!'}), 404
    return json.dumps({'success': True, 'data': {'link': media}}), 200

@app.route('/api/celebs/<int:c_id>/edit/', methods=['POST'])
def edit_media(c_id):
    celeb = Celeb.query.filter_by(id=c_id).first()
    if not celeb:
        return json.dumps({'success': False, 'error': 'Celeb not found!'}), 404
    post_body=json.loads(request.data)
    name = post_body.get('name', celeb.name)
    profile_pic = post_body.get('profile_pic', celeb.profile_pic)
    photo = post_body.get('photo', celeb.photo)
    instagram = post_body.get('instagram', celeb.instagram)
    twitter = post_body.get('twitter', celeb.twitter)
    spotify = post_body.get('spotify', celeb.spotify)
    website = post_body.get('website', celeb.website)
    other = post_body.get('other', celeb.other)

    celeb.name = name
    celeb.profile_pic = profile_pic
    celeb.photo = photo
    celeb.instagram = instagram
    celeb.twitter = twitter
    celeb.spotify = spotify
    celeb.website = website
    celeb.other = other
    db.session.commit()
    return json.dumps({'success': True, 'data': celeb.serialize()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

                                            




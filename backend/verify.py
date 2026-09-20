from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    u = User.query.filter_by(email='alaguvalli141@gmail.com').first()
    if u:
        u.is_verified = True
        db.session.commit()
        print('verified', u.email)
    else:
        print('user not found')
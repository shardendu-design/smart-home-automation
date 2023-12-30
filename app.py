from app.auth.models import User
from app import create_app, db

if __name__ == '__main__':
    flask_app = create_app('dev')
    with flask_app.app_context():
        db.create_all()
        if not User.query.filter_by(user_name='apps').first():
            User.create_user(user='apps',
                             email='apps95@yahoo.com',
                             password='Computer'
                             )

    flask_app.run(host="localhost", port=7777, debug=True)
    
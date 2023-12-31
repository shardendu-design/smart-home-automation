
from app.auth.models import User
from app import create_app, db



def flask_runner():

        flask_app = create_app('dev')
        with flask_app.app_context():
            db.create_all()
            if not User.query.filter_by(user_name='admin').first():
                User.create_user(user='admin',
                                email='admin@admin.com',
                                password='admin'
                                )
        flask_app.run(host="localhost", port=7777, debug=True)


if __name__ == '__main__':
    flask_runner()

  
from app.auth.models import User
from app import create_app, db

import signal
import sys



def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Shutting down...')
    # Perform any cleanup here if necessary
    sys.exit(0)

def flask_runner():
    
    signal.signal(signal.SIGINT, signal_handler)  # Register the signal handler

    flask_app = create_app('dev')
    with flask_app.app_context():
        db.create_all()
        if not User.query.filter_by(user_name='admin').first():
            User.create_user(user='admin',
                             email='admin@admin.com',
                             password='admin')
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
    


if __name__ == '__main__':
    flask_runner()


  
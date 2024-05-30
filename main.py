from flask import Flask, render_template
from blueprints.lock import lock_bp
from blueprints.passcode import passcode_bp
from blueprints.users import users_bp
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password1206@localhost/tthotel'
db = SQLAlchemy(app)

print(f"{int(datetime.now().timestamp()) * 1000}")
@app.route('/')
def index() :
    return render_template('index.html')

app.register_blueprint(lock_bp)
app.register_blueprint(passcode_bp)
app.register_blueprint(users_bp)

with app.app_context():
    print(f"init db")
    from model.passcode import Passcode
    db.create_all()


if __name__ == '__main__':
   app.run(debug=True)
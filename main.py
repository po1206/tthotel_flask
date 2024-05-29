from flask import Flask, render_template
from blueprints.lock import lock_bp
from blueprints.passcode import passcode_bp
from blueprints.users import users_bp
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password1206@localhost/tthotel'
db = SQLAlchemy(app)


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
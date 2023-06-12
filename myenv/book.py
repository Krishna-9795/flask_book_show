from flask import Flask, request, jsonify
from flask_sqlalchemy  import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required,create_access_token,get_jwt_identity
from datetime import timedelta

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:krishna123@localhost/bookmyshows'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'Krishna#9795 ' 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists. Please choose a different username.'}), 400
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})   

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return jsonify({'message': 'Invalid username or password.'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200
        
        


@app.route('/movies',methods=['GET'])
@jwt_required()
def get_movies():
    current_user_id=get_jwt_identity()
    movies=[
        {'id': 1, 'title': 'Ragnarock'},
        {'id': 2, 'title': 'Beatles'},
        {'id': 3, 'title': 'Queens'}
    ]
    return jsonify(movies), 200

if __name__=="__main__":
    app.run()

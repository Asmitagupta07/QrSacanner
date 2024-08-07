# app.py
from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import qrcode
import io
from base64 import b64encode, b64decode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    qr_code = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    name = data['name']
    email = data['email']
    password = data['password']
    
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    
    qr_data = f"{name}|{email}|{user.id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    qr_code_str = b64encode(buf.getvalue()).decode('utf-8')
    
    user.qr_code = qr_code_str
    db.session.commit()
    
    return jsonify({'status': 'success', 'qr_code': qr_code_str})

@app.route('/qr/<int:user_id>', methods=['GET'])
def get_qr(user_id):
    user = User.query.get(user_id)
    if user and user.qr_code:
        qr_image = io.BytesIO(b64decode(user.qr_code))
        qr_image.seek(0)
        return send_file(qr_image, mimetype='image/png', as_attachment=True, download_name='qrcode.png')
    return jsonify({'status': 'error', 'message': 'User or QR code not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cine_match.db'
db = SQLAlchemy(app)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)

films_fictifs = [
    {"titre": "Film Action 1", "genre": "action"},
    {"titre": "Film Comédie 1", "genre": "comédie"},
    # Ajoutez d'autres films fictifs ici
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_preferences', methods=['POST'])
def submit_preferences():
    genre = request.form['genre']
    recommandations = recommander_films(genre)
    return render_template('index.html', recommandations=recommandations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = Utilisateur(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

def recommander_films(genre):
    return [film for film in films_fictifs if film['genre'] == genre]

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

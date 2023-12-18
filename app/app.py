from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cine_match.db'
db = SQLAlchemy(app)

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)

films_fictifs = [
    {"titre": "Film Action 1", "genre": "action"},
    {"titre": "Film Comédie 1", "genre": "comédie"},
    # Ajoutez d'autres films fictifs ici
]

def recommander_films(genre):
    return [film for film in films_fictifs if film['genre'] == genre]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_preferences', methods=['POST'])
def submit_preferences():
    genre = request.form['genre']
    recommandations = recommander_films(genre)
    return render_template('index.html', recommandations=recommandations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

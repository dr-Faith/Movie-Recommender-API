from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from recommender import MovieRecommender
import datetime
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fhkgsjdhoiejothieqioajhoru'
Bootstrap(app)

# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    backdrop_path = db.Column(db.String(250), nullable=True)
    overview = db.Column(db.String(1000), nullable=True)
    poster_path = db.Column(db.String(250), nullable=True)
    media_type = db.Column(db.String(8), nullable=True)
    genres = db.Column(db.String(250), nullable=False)
    popularity = db.Column(db.Float(), nullable=True)
    release_date = db.Column(db.String(10), nullable=True)

    def __repr__(self):
        return '<Movie %r>' % self.title
    
app.app_context().push()
db.create_all()

df = pd.read_csv('../tmdb_data/tmdb_movies.csv')
df.drop_duplicates(inplace=True)
df.rename(columns={'genre_ids': 'genres'}, inplace=True)
df['release_date'].fillna('N.D.', inplace=True)
seg = df[['id', 'backdrop_path', 'title', 'overview', 'poster_path', 'media_type', 'genres', 'popularity', 'release_date', 'vote_average', 'vote_count']]


# for idx, row in seg.iterrows():
#     title = row['title']
#     backdrop_path = row['backdrop_path']
#     overview = row['overview']
#     poster_path = row['poster_path']
#     media_type = row['media_type']
#     genres = row['genres']
#     popularity = row['popularity']
#     release_date = row['release_date']

#     new_movie = Movie(
#         id=idx+1,
#         title=title,
#         backdrop_path=backdrop_path,
#         overview=overview,
#         poster_path=poster_path,
#         media_type=media_type,
#         genres=genres,
#         popularity=popularity,
#         release_date=release_date,
#     )

#     db.session.add(new_movie)
#     db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def home():
    # input_form = InputForm()
    # if request.method == 'POST' and input_form.validate_on_submit():
    #     input_movie = input_form.movie_input.data
    #     print(input_movie)
    # return render_template('index.html', form=input_form)
    return "Welcome to the Movie Recommendation API"

# RETURN ALL RECOMMENDED MOVIES 

### REST API

# GET RECOMMENDATIONS FOR A MOVIE
@app.route('/recommend')
def recommend():
    movie = request.args.get('movie')
    movie_recommender = MovieRecommender('../latent_matrix_1_df.pkl', '../user_ratings_f1.pkl', '../mov_map.pkl', '../mov_id_map.pkl')
    similar_movies = movie_recommender.recommend_movies(movie)
    all_movies = db.session.query(Movie).all()
    
    similar_movies_data = list(filter(lambda x: x.title in similar_movies, all_movies))

    data = [{
        'title': movie.title,
        'backdrop_path': movie.backdrop_path,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        'media_type': movie.media_type,
        'genres': movie.genres,
        'popularity': movie.popularity,
        'release_date': movie.release_date
    } for movie in similar_movies_data]

    if not similar_movies:
        return jsonify(message="Movie not found in our database"), 404
    return jsonify(recommendations=data), 200

# ADD A MOVIE
@app.route('/add', methods=['POST'])
def add():
    backdrop = request.args.get('backdrop')
    title = request.args.get('title')
    overview = request.args.get('overview')
    poster_path = request.args.get('poster-path')
    media_type = request.args.get('media-type')
    movie_genres = request.args.get('movie-genres')
    popularity = request.args.get('popularity')
    release_date = request.args.get('release-date')

    new_movie = Movie(
            title=title,
            backdrop_path=backdrop,
            overview=overview,
            poster_path=poster_path,
            media_type=media_type,
            genres=movie_genres,
            popularity=popularity,
            release_date=release_date
        )

    if api_key == env
    try:
        db.session.add(new_movie)
        db.session.commit()
    except Exception as e:
        print(e.message)
        return jsonify(message=e.message), 400

    return jsonify(message="Success, movie added succesfully!"), 200

# RATE A MOVIE

if __name__ == '__main__': 
    app.run(debug=True)
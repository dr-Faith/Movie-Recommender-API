from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
from recommender import MovieRecommender


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fhkgsjdhoiejothieqioajhoru'
Bootstrap(app)


class InputForm(FlaskForm):
    movie_input = StringField(label='Input a movie you have watched before', validators=[DataRequired(), Length(min=5, message='Password must be at least 5 characters long.')])
    submit = SubmitField(label='Submit')



@app.route('/', methods=['GET', 'POST'])
def home():
    # input_form = InputForm()
    # if request.method == 'POST' and input_form.validate_on_submit():
    #     input_movie = input_form.movie_input.data
    #     print(input_movie)
    # return render_template('index.html', form=input_form)
    return "Welcome to the Movie Recommendation API"


# GET RECOMMENDATIONS FOR A MOVIE
@app.route('/recommend')
def recommend():
    movie = request.args.get('movie')
    movie_recommender = MovieRecommender('../latent_matrix_1_df.pkl', '../user_ratings_f1.pkl', '../mov_map.pkl', '../mov_id_map.pkl')
    similar_movies = movie_recommender.recommend_movies(movie)
    if not similar_movies:
        return jsonify(message="Movie not found in our database")
    return jsonify(recommendations=similar_movies)


# RETURN ALL RECOMMENDED MOVIES 


if __name__ == '__main__':
    app.run(debug=True)
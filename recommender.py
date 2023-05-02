import numpy as np
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import difflib


class MovieRecommender():
    
    def __init__(self, path_to_content_latent_matrix, path_to_user_latent_matrix, path_to_mov_map, path_to_mov_id_map):
        self.content_latent_matrix = MovieRecommender.read_bfile(path_to_content_latent_matrix)
        self.user_latent_matrix = MovieRecommender.read_bfile(path_to_user_latent_matrix)
        self.mov_map = MovieRecommender.read_bfile(path_to_mov_map)
        self.mov_id_map = MovieRecommender.read_bfile(path_to_mov_id_map)
        
    @staticmethod 
    def read_bfile(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
        
    def recommend_movies(self, movie):
        selected_movie = movie ##############
        close_matches = difflib.get_close_matches(selected_movie, list(self.mov_id_map.keys()))
        select_movie = close_matches[0]
        selected_movie_id = self.mov_id_map[select_movie]
        a_1 = np.array(self.content_latent_matrix.loc[selected_movie_id]).reshape(1, -1)
        a_2 = np.array(self.user_latent_matrix.loc[selected_movie_id]).reshape(1, -1)
        score_1 = cosine_similarity(self.content_latent_matrix, a_1).reshape(-1)
        score_2 = cosine_similarity(self.user_latent_matrix, a_2).reshape(-1)
        hybrid = ((score_1 + score_2)/2.)
        dictDf = {'content': score_1, 'collaborative': score_2, 'hybrid': hybrid}
        similar = pd.DataFrame(dictDf, index=self.content_latent_matrix.index)

        similar.sort_values('hybrid', ascending=False, inplace=True)
        top_similar = [self.mov_map[idx] for idx in similar[1:].head(11).index]

        print(f"***********Recommended Movies for {select_movie.upper()}**********")
        for idx, movie in enumerate(top_similar):
            print(f"{idx+1}. {movie}")
    
if __name__ == '__main__':
    movie_recommender = MovieRecommender('latent_matrix_1_df.pkl', 'user_ratings_f1.pkl', 'mov_map.pkl', 'mov_id_map.pkl')
    movie = input("Which movie would you like to find similar movies for in our database?: ")
    movie_recommender.recommend_movies(movie)
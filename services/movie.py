from models.movie import MovieModel
from schemas.movie import Movie

class MovieService():

    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie_by_id(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).one_or_none()
        return result
    
    def get_movie_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.model_dump())
        self.db.add(new_movie)
        self.db.commit()
        return new_movie
    
    def update_movie(self, id: int, movie: Movie):
        result = self.get_movie_by_id(id)
        result.title = movie.title
        result.overview = movie.overview
        result.year = movie.year
        result.rating = movie.rating
        result.category = movie.category
        self.db.commit()
        return result
    
    def delete_movie(self, id):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return
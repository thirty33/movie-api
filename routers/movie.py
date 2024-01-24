from fastapi import APIRouter
from fastapi import Query, Path, Depends
from config.database import Session
from models.movie import MovieModel
from schemas.movie import Movie
from fastapi.responses import JSONResponse
from typing import List
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService

movie_router = APIRouter()

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movies(
    movie: Movie
) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={'message': 'Movie has been registered'})

# get movies
@movie_router.get(
    '/movies', tags=['movies'],
    response_model=List[Movie],
    # dependencies=[Depends(JWTBearer())]
)
def get_movies(
) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# get movies by id
@movie_router.get('/movies-by-id/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'item not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies-by-category', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(
    category: str = Query(min_length=5, max_length=15)
) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movies not found'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(
    id: int,
    movie: Movie
) -> dict:
    
    db = Session()
    result = MovieService(db).get_movie_by_id(id)

    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    
    movie_updated = MovieService(db).update_movie(id, movie)

    return JSONResponse(status_code=200, content=jsonable_encoder(movie_updated))

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id: int) -> dict:

    db = Session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Movie not found'})
    
    # db.delete(result)
    # db.commit()
    MovieService(db).delete_movie(id)

    return JSONResponse(status_code=200, content={'message': 'Movie has been deleted'})

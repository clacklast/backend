from fastapi import APIRouter, HTTPException, Query, Form, File, UploadFile, Depends, Request
from typing import Optional
from app.models import Movie, MovieUpdate
from datetime import timedelta
from app.security import verify_token, authenticate_user, create_access_token
from app.crud import create_movie, update_movie, upload_movie_image, find_movie, remove_movie, get_all_movies
from app.storage import client, BUCKET
from beanie import PydanticObjectId
from fluent import handler
import logging
fluent_host="192.168.100.77"
fluent_port=24224
app_name="bootcamp2-backend"
fluent_handler = handler.FluentHandler(app_name, host=fluent_host, port=fluent_port)
formatter = handler.FluentRecordFormatter({
    'job': app_name,
    'host': '%(hostname)s',
    'where': '%(module)s.%(funcName)s',
    'path': '%(path)s',
    'request': '%(request)s',
    'ip': '%(ip)s',
    'message': '%(message)s'
})
fluent_handler.setFormatter(formatter)

logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)
logger.addHandler(fluent_handler)


router=APIRouter()

@router.post("/movies", response_model=Movie, dependencies=[Depends(verify_token)])
async def post_movie(
        title: str = Form(None),
        director: str | None = Form(None),
        year: int | None = Form(None),
        image_file: UploadFile | None = File(None)
):

    movie = Movie(title=title, director=director, year=year)
    movie= await create_movie(movie)

    if image_file: 
        image_path = await upload_movie_image(movie.id, image_file)
        movie.image = image_path
        await movie.save()

    return movie

#opción para listar todas las películas
# @router.get("/movies", response_model=list[Movie])
# async def get_movies(
#         skip:int=Query(0, ge=0),
#         limit:int=Query(10, le=100),
#         title: Optional[str]=None,
#         year: Optional[int]=None,
#         director: Optional[str]=None
# ):
#     return await read_movies(skip=skip, limit=limit, title=title, year=year, director=director)

@router.get("/movies/{id_movie}", response_model=Movie)
async def get_movie(
        id_movie: str,
        request: Request,
):
    logger.info("Request a /movies/{id_movie}", extra={
        'path': request.url.path,
        'ip': request.client.host,
        'request': request.method,
    })
    return await find_movie(id_movie)

# @router.put("/movies/{movie_id}", response_model=Movie)
# async def put_movie(movie_id: PydanticObjectId, movie_update: MovieUpdate):
#     movie = await update_movie(movie_id, movie_update)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     return movie

@router.put("/movies/{movie_id}", response_model=Movie, dependencies=[Depends(verify_token)])
async def put_movie(
    movie_id: PydanticObjectId,
    title: str = Form(None),
    director: str = Form(None),
    year: int = Form(None),
    image_file: UploadFile | None = File(None)
):
    data = MovieUpdate(title=title, director=director, year=year)

    updated_movie = await update_movie(movie_id, data, image_file)

    if not updated_movie:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    return updated_movie

@router.delete("/movies/{movie_id}", dependencies=[Depends(verify_token)])
async def delete_movie(movie_id: str):
    deleted = await remove_movie(movie_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return {"message": "Película eliminada correctamente"}

@router.get("/movies", summary='List all movies', response_model=list[Movie])
async def list_movies(request: Request):
    logger.info("Request a /movies/{id_movie}", extra={
        'path': request.url.path,
        'ip': request.client.host,
        'request': request.method,
    })
    return await get_all_movies()


@router.post("/token") # Endpoint para obtener el token (login)
async def login(username:str = Form(...), password:str = Form(...)):
    user= await authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access_token_expires = timedelta(minutes=30)

    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
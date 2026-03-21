from fastapi import APIRouter

from backend.app.api.schemas.genres import GenresResponse, Genre
from backend.app.api.schemas.offers import Offer, OfferPrices

router = APIRouter(prefix="/genres", tags=["Genres"])

@router.get(
    path="/",
    response_model=GenresResponse)
def get_genres(

):
    ...

@router.get(
    path="/{genre_id}",
    response_model=Genre
)
def get_genre(
    genre_id: int
):
    ...

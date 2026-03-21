from fastapi import APIRouter

from backend.app.api.schemas.genres import GenresResponse, Genre
from backend.app.api.schemas.offers import Offer, OfferPrices
from backend.app.api.schemas.platforms import PlatformsResponse, Platform

router = APIRouter(prefix="/platform", tags=["Platforms"])


@router.get(
    path="/",
    response_model=PlatformsResponse)
def get_platforms():
    ...


@router.get(
    path="/{platform_id}",
    response_model=Platform
)
def get_platform(platform_id: int):
    ...

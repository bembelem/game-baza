from fastapi import APIRouter

from backend.app.api.schemas.offers import Offer, OfferPrices

router = APIRouter(prefix="/offers", tags=["Offers"])

@router.get(
    path="/{offer_id}",
    response_model=Offer)
def get_offer(
    offer_id: int
):
    ...

@router.get(
    path="/{offer_id}/price-history",
    response_model=OfferPrices
)
def get_offer_price_history(
    offer_id: int
):
    ...
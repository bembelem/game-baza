from fastapi import APIRouter

from backend.app.api.schemas.publishers import PublishersResponse, Publisher
from backend.app.api.schemas.stores import Store

router = APIRouter(prefix="/publishers", tags=["Publishers"])

@router.get(
    path="/",
    response_model=PublishersResponse)
def get_publisher():
    ...


@router.get(
    path="/{publisher_id}",
    response_model=Publisher
)
def get_publishers(publisher_id: int):
    ...




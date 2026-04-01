from fastapi import APIRouter

from app.api.schemas.publishers import PublishersResponse, Publisher

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




from fastapi import APIRouter

from backend.app.api.v1.schemas.auth import RegisterDTO, TokenDTO, LoginDTO
from backend.app.api.v1.schemas.user import UserDTO, CommentDTO

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=UserDTO,
    status_code=201,
    summary="Register a new user",
    description="Creates a new user. Returns user profile.",
)
def register(body: RegisterDTO):
    return UserDTO(
        id=1,
        username=body.username,
        email=body.email,
        created_at="2026-03-13",
    )

@router.post(
    "/login",
    response_model=TokenDTO,
    summary="Login",
    description="Returns JWT access token.",
)
def login(body: LoginDTO):
    # TODO
    return TokenDTO(access_token="fake-jwt-token")

@router.get(
    "/me",
    response_model=UserDTO,
    summary="Current user profile",
    description="Returns profile of the authenticated user with wishlist and comments.",
)
def get_me():
    # TODO
    return UserDTO(
        id=1,
        username="nikita",
        email="nikita@example.com",
        created_at="2026-03-13",
        wishlist_count=3,
        comments_count=3,
    )
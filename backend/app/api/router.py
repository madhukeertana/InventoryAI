from fastapi import APIRouter

from app.api.v1 import action_cards, auth, inventory, ocr, users

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(inventory.router)
api_router.include_router(ocr.router)
api_router.include_router(action_cards.router)

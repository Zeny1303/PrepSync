from fastapi import APIRouter, Depends
from app.schemas.slot_schema import CreateSlot
from app.controllers import slot_controller
from app.middleware.auth_middleware import get_current_user

router = APIRouter()


@router.post("/create")
async def create_slot(
    slot: CreateSlot,
    current_user = Depends(get_current_user)
):
    return await slot_controller.create_slot(slot, current_user)

@router.post("/book/{slot_id}")
async def book_slot(
    slot_id: str,
    current_user = Depends(get_current_user)
):
    return await slot_controller.book_slot(slot_id, current_user)

@router.get("/available")
async def get_available_slots():
    return await slot_controller.get_available_slots()

@router.get("/booked")
async def get_my_booked_slots(
    current_user = Depends(get_current_user)
):
    return await slot_controller.get_my_booked_slots(current_user)

@router.delete("/cancel/{slot_id}")
async def cancel_slot(
    slot_id: str,
    current_user = Depends(get_current_user)
):
    return await slot_controller.cancel_slot(slot_id, current_user)
@router.get("/created-and-booked")
async def get_created_and_booked_slots(
    current_user = Depends(get_current_user)
):
    return await slot_controller.get_created_and_booked_slots(current_user)
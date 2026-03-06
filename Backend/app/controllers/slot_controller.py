from uuid import uuid4
from bson import ObjectId
from fastapi import HTTPException
from datetime import timedelta
from app.database import slots_collection


async def create_slot(slot, current_user):

    start_time = slot.startTime
    end_time = start_time + timedelta(minutes=slot.duration)

    new_slot = {
        "createdBy": str(current_user["_id"]),
        "startTime": start_time,
        "endTime": end_time,
        "duration": slot.duration,
        "skills": slot.skills,
        "isBooked": False,
        "bookedBy": None,
        "roomId": None
    }

    result = await slots_collection.insert_one(new_slot)

    new_slot["id"] = str(result.inserted_id)

    return new_slot
async def book_slot(slot_id, current_user):

    slot = await slots_collection.find_one({"_id": ObjectId(slot_id)})

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    if slot["isBooked"]:
        raise HTTPException(status_code=400, detail="Slot already booked")

    if slot["createdBy"] == str(current_user["_id"]):
        raise HTTPException(status_code=400, detail="You cannot book your own slot")

    slot["isBooked"] = True
    slot["bookedBy"] = str(current_user["_id"])
    slot["roomId"] = str(uuid4())

    await slots_collection.update_one(
        {"_id": ObjectId(slot_id)},
        {"$set": slot}
    )

    return {
        "message": "Slot booked successfully",
        "slot": slot
    }
async def get_available_slots():

    slots = await slots_collection.find({"isBooked": False}).to_list(None)

    for slot in slots:
        slot["id"] = str(slot["_id"])
        slot["_id"] = str(slot["_id"])

    return slots
async def get_my_booked_slots(current_user):

    slots = await slots_collection.find({
        "bookedBy": str(current_user["_id"])
    }).to_list(None)

    for slot in slots:
        slot["id"] = str(slot["_id"])
        slot["_id"] = str(slot["_id"])

    return slots

async def cancel_slot(slot_id, current_user):

    slot = await slots_collection.find_one({"_id": ObjectId(slot_id)})

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    if slot["createdBy"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")

    await slots_collection.delete_one({"_id": ObjectId(slot_id)})

    return {"message": "Slot cancelled successfully"}
from bson import ObjectId

async def cancel_slot(slot_id, current_user):

    slot = await slots_collection.find_one({"_id": ObjectId(slot_id)})

    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    if slot["createdBy"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")

    await slots_collection.delete_one({"_id": ObjectId(slot_id)})

    return {"message": "Slot cancelled successfully"}
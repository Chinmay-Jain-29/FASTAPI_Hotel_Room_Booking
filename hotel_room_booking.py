from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional

app = FastAPI(title="Hotel Management System")

# ---------------- ENUM ----------------

class RoomType(str, Enum):
    non_ac = "non_ac"
    ac = "ac"
    deluxe = "deluxe"

# ---------------- CONFIG ----------------

hotel_config = {
    "non_ac": {"price": 1000, "base": 100, "limit": 10, "floor": "ground"},
    "ac": {"price": 1500, "base": 200, "limit": 10, "floor": "first"},
    "deluxe": {"price": 2000, "base": 300, "limit": 10, "floor": "second"}
}

# ---------------- STORAGE ----------------

bookings = []  # active bookings
booking_history = []  # all records (history)

occupied_rooms = {
    "non_ac": [],
    "ac": [],
    "deluxe": []
}

# ---------------- MODELS ----------------

class BookingRequest(BaseModel):
    name: str = Field(min_length=3)
    aadhar: str = Field(min_length=12, max_length=12)
    phone: str = Field(min_length=10, max_length=10)
    room_type: RoomType
    days: int = Field(gt=0, le=30)

    @validator("phone", "aadhar")
    def digits_only(cls, v):
        if not v.isdigit():
            raise ValueError("Must contain only digits")
        return v

class BookingUpdate(BaseModel):
    room_type: Optional[RoomType] = None
    days: Optional[int] = None

# ---------------- HELPERS ----------------

def assign_room(room_type: str):
    config = hotel_config[room_type]
    base = config["base"]
    limit = config["limit"]

    for i in range(1, limit + 1):
        room_no = base + i
        if room_no not in occupied_rooms[room_type]:
            return room_no
    return None

def find_booking(cust_id: int):
    return next((b for b in bookings if b["cust_id"] == cust_id), None)

def check_admin(is_admin: bool):
    if not is_admin:
        raise HTTPException(403, "Admin access required")

# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Hotel API Running"}

# ---------------- BOOK ROOM ----------------

@app.post("/booking", status_code=201)
def book_room(data: BookingRequest):
    r_type = data.room_type.value

    if len(occupied_rooms[r_type]) >= hotel_config[r_type]["limit"]:
        raise HTTPException(400, "All rooms booked")

    room_no = assign_room(r_type)

    if not room_no:
        raise HTTPException(400, "No room available")

    occupied_rooms[r_type].append(room_no)

    config = hotel_config[r_type]
    total = config["price"] * data.days

    booking = {
        "cust_id": len(bookings) + 1001,
        "room_no": room_no,
        "room_type": r_type,
        "floor": config["floor"],
        "name": data.name,
        "phone": data.phone,
        "days": data.days,
        "rate": config["price"],
        "total": total
    }

    bookings.append(booking)
    booking_history.append({**booking, "status": "active"})

    return booking

# ---------------- UPDATE BOOKING ----------------

@app.put("/booking/update")
def update_booking(cust_id: int, name: str, data: BookingUpdate):
    booking = find_booking(cust_id)

    if not booking or booking["name"].lower() != name.lower():
        raise HTTPException(404, "Booking not found")

    # change room type
    if data.room_type:
        new_type = data.room_type.value

        if len(occupied_rooms[new_type]) >= hotel_config[new_type]["limit"]:
            raise HTTPException(400, "No rooms available for this type")

        occupied_rooms[booking["room_type"]].remove(booking["room_no"])

        new_room = assign_room(new_type)
        occupied_rooms[new_type].append(new_room)

        booking["room_type"] = new_type
        booking["room_no"] = new_room
        booking["floor"] = hotel_config[new_type]["floor"]
        booking["rate"] = hotel_config[new_type]["price"]

    # update days
    if data.days:
        booking["days"] = data.days

    # recalculate
    booking["total"] = booking["rate"] * booking["days"]

    # update history
    for record in booking_history:
        if record["cust_id"] == cust_id:
            record.update(booking)

    return booking

# ---------------- CANCEL BOOKING ----------------

@app.delete("/booking/cancel")
def cancel_booking(cust_id: int, name: str):
    booking = find_booking(cust_id)

    if not booking or booking["name"].lower() != name.lower():
        raise HTTPException(404, "Booking not found")

    occupied_rooms[booking["room_type"]].remove(booking["room_no"])

    for record in booking_history:
        if record["cust_id"] == cust_id:
            record["status"] = "cancelled"

    bookings.remove(booking)

    return {"message": "Booking cancelled"}

# ---------------- CHECKOUT ----------------

@app.post("/checkout")
def checkout(cust_id: int, room_no: int, name: str):
    booking = find_booking(cust_id)

    if not booking or booking["name"] != name or booking["room_no"] != room_no:
        raise HTTPException(400, "Invalid details")

    occupied_rooms[booking["room_type"]].remove(room_no)

    for record in booking_history:
        if record["cust_id"] == cust_id:
            record["status"] = "checked_out"

    bookings.remove(booking)

    return {"message": "Checkout successful"}

# ---------------- INQUIRY ----------------

@app.get("/inquiry")
def inquiry(room_no: int, name: str):
    result = next(
        (b for b in bookings if b["room_no"] == room_no and b["name"].lower() == name.lower()),
        None
    )

    if not result:
        raise HTTPException(404, "Room not assigned")

    return result

# ---------------- SEARCH ----------------

@app.get("/search")
def search(room_type: RoomType, name: str):
    result = [
        b for b in bookings
        if b["room_type"] == room_type.value and name.lower() in b["name"].lower()
    ]

    if not result:
        raise HTTPException(404, "No results found")

    return result

# ---------------- SORT ----------------

@app.get("/sort")
def sort(by: str = "room_type", order: str = "asc"):
    if by not in ["room_type", "rate"]:
        raise HTTPException(400, "Invalid sort field")

    reverse = order == "desc"
    return sorted(bookings, key=lambda x: x[by], reverse=reverse)

# ---------------- ADMIN HISTORY ----------------

@app.get("/admin/bookings")
def get_all_bookings(is_admin: bool):
    check_admin(is_admin)

    if not booking_history:
        raise HTTPException(404, "No records found")

    return booking_history

# ---------------- ADMIN SUMMARY ----------------

@app.get("/admin/summary")
def admin_summary(is_admin: bool):
    check_admin(is_admin)

    result = {}

    for r_type in hotel_config:
        occupied = len(occupied_rooms[r_type])
        total = hotel_config[r_type]["limit"]

        result[r_type] = {
            "occupied": occupied,
            "vacant": total - occupied
        }

    return result

# ---------------- ACCOUNT ----------------

@app.get("/account")
def account_summary():
    total_revenue = sum(
        b["total"] for b in booking_history if b["status"] == "checked_out"
    )

    return {
        "total_records": len(booking_history),
        "active": len([b for b in booking_history if b["status"] == "active"]),
        "checked_out": len([b for b in booking_history if b["status"] == "checked_out"]),
        "cancelled": len([b for b in booking_history if b["status"] == "cancelled"]),
        "total_revenue": total_revenue
    }
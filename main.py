from fastapi import FastAPI, HTTPException, Query
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

bookings = []  # active
booking_history = []  # full history

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
    for i in range(1, config["limit"] + 1):
        room_no = config["base"] + i
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
    return {"message": "Welcome to Hotel Management System"}

# ---------------- GET ALL + PAGINATION ----------------

@app.get("/bookings")
def get_bookings(page: int = 1, limit: int = 5):
    start = (page - 1) * limit
    end = start + limit
    total_pages = (len(booking_history) + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": booking_history[start:end]
    }


# ---------------- ROOM CATALOG ----------------

@app.get("/rooms/catalog")
def room_catalog():
    catalog = {}

    for r_type, config in hotel_config.items():
        total = config["limit"]
        occupied = len(occupied_rooms[r_type])

        catalog[r_type] = {
            "price": config["price"],
            "floor": config["floor"],
            "total_rooms": total,
            "occupied": occupied,
            "vacant": total - occupied
        }

    return catalog

# ---------------- GET BY ID ----------------

@app.get("/booking/{cust_id}")
def get_booking(cust_id: int):
    booking = find_booking(cust_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    return booking

# ---------------- BOOKING ----------------

@app.post("/booking", status_code=201)
def book_room(data: BookingRequest):

    # duplicate check
    for b in bookings:
        if b["phone"] == data.phone:
            raise HTTPException(400, "Duplicate booking not allowed")

    r_type = data.room_type.value

    if len(occupied_rooms[r_type]) >= hotel_config[r_type]["limit"]:
        raise HTTPException(400, "All rooms booked")

    room_no = assign_room(r_type)

    occupied_rooms[r_type].append(room_no)

    config = hotel_config[r_type]
    total = config["price"] * data.days

    booking = {
        "cust_id": len(booking_history) + 1001,
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

# ---------------- UPDATE ----------------

@app.put("/booking/update")
def update_booking(cust_id: int, name: str, data: BookingUpdate):
    booking = find_booking(cust_id)

    if not booking or booking["name"].lower() != name.lower():
        raise HTTPException(404, "Booking not found")

    if data.room_type:
        new_type = data.room_type.value

        if len(occupied_rooms[new_type]) >= hotel_config[new_type]["limit"]:
            raise HTTPException(400, "No rooms available")

        occupied_rooms[booking["room_type"]].remove(booking["room_no"])

        new_room = assign_room(new_type)
        occupied_rooms[new_type].append(new_room)

        booking["room_type"] = new_type
        booking["room_no"] = new_room
        booking["floor"] = hotel_config[new_type]["floor"]
        booking["rate"] = hotel_config[new_type]["price"]

    if data.days:
        booking["days"] = data.days

    booking["total"] = booking["rate"] * booking["days"]

    for record in booking_history:
        if record["cust_id"] == cust_id:
            record.update(booking)

    return booking

# ---------------- DELETE (CANCEL) ----------------

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

# ---------------- FILTER ----------------

@app.get("/filter")
def filter_data(
    room_type: Optional[RoomType] = Query(None),
    min_days: Optional[int] = Query(None)
):
    result = bookings

    if room_type is not None:
        result = [b for b in result if b["room_type"] == room_type.value]

    if min_days is not None:
        result = [b for b in result if b["days"] >= min_days]

    if not result:
        raise HTTPException(404, "No data found")

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
        raise HTTPException(400, "Invalid field")

    reverse = order == "desc"
    return sorted(bookings, key=lambda x: x[by], reverse=reverse)

# ---------------- BROWSE (Q20) ----------------

@app.get("/browse")
def browse(
    room_type: Optional[RoomType] = None,
    name: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: str = "asc",
    page: int = 1,
    limit: int = 5
):
    result = booking_history

    if room_type:
        result = [b for b in result if b["room_type"] == room_type.value]

    if name:
        result = [b for b in result if name.lower() in b["name"].lower()]

    if sort_by in ["room_type", "rate"]:
        reverse = order == "desc"
        result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit
    end = start + limit
    total_pages = (len(result) + limit - 1) // limit

    return {
        "page": page,
        "total_pages": total_pages,
        "data": result[start:end]
    }

# ---------------- ADMIN HISTORY ----------------

@app.get("/admin/bookings")
def admin_bookings(is_admin: bool):
    check_admin(is_admin)
    return booking_history

# ---------------- SUMMARY ----------------

@app.get("/admin/summary")
def summary(is_admin: bool):
    check_admin(is_admin)

    return {
        r: {
            "occupied": len(occupied_rooms[r]),
            "vacant": hotel_config[r]["limit"] - len(occupied_rooms[r])
        }
        for r in hotel_config
    }

# ---------------- ACCOUNT ----------------

@app.get("/account")
def account():
    return {
        "total_records": len(booking_history),
        "checked_out": len([b for b in booking_history if b["status"] == "checked_out"]),
        "cancelled": len([b for b in booking_history if b["status"] == "cancelled"]),
        "active": len([b for b in booking_history if b["status"] == "active"]),
        "total_revenue": sum(b["total"] for b in booking_history if b["status"] == "checked_out")
    }
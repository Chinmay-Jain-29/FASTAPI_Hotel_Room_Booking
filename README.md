# 🏨 Hotel Management System (FastAPI)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)
![Status](https://img.shields.io/badge/Project-Completed-success.svg)

A complete **Hotel Management System API** built using **FastAPI**.
This project demonstrates real-world backend concepts like **auto room allocation, booking workflow, CRUD operations, filtering, sorting, pagination, and account tracking**.

---

## 🚀 Features

✨ Auto Room Allocation (System assigns room number)

✨ Booking, Update, Cancel & Checkout Workflow

✨ Room Categories (Non-AC, AC, Deluxe)

✨ Admin Module (Booking history & summary)

✨ Search, Sort & Filter functionality

✨ Pagination & Combined Browse API

✨ Room Catalog (Live availability status)

✨ Account tracking (Revenue + records)

✨ Strong input validation using Pydantic

✨ Proper HTTP status codes

---

## 🧠 Tech Stack

* ⚡ FastAPI
* 🐍 Python
* 📦 Pydantic
* 📄 Swagger UI (API Testing)

---

## 📂 Project Structure

```
main.py  → Complete FastAPI application
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/hotel-management-fastapi.git
cd hotel-management-fastapi
```

### 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn
```

### 3️⃣ Run Server

```bash
uvicorn main:app --reload
```

### 4️⃣ Open API Docs

👉 http://127.0.0.1:8000/docs

---

## 📌 API Endpoints

### 🔹 Booking

* `POST /booking` → Book room
* `PUT /booking/update` → Update booking
* `DELETE /booking/cancel` → Cancel booking
* `POST /checkout` → Checkout

### 🔹 Inquiry & Data

* `GET /inquiry` → Check room status
* `GET /search` → Search bookings
* `GET /filter` → Filter records
* `GET /sort` → Sort data

### 🔹 Advanced APIs

* `GET /bookings` → Pagination
* `GET /browse` → Filter + Sort + Pagination
* `GET /rooms/catalog` → Room catalog

### 🔹 Admin

* `GET /admin/bookings` → Booking history
* `GET /admin/summary` → Room summary

### 🔹 Account

* `GET /account` → Revenue & stats

---

## 🔄 Workflow

1️⃣ User books a room
2️⃣ System auto-assigns room number
3️⃣ Room becomes occupied
4️⃣ User can update or cancel booking
5️⃣ Checkout frees the room
6️⃣ All records stored in history
7️⃣ Account tracks revenue

---

## 📊 Room Categories

| Type   | Price | Floor  | Limit |
| ------ | ----- | ------ | ----- |
| Non-AC | ₹1000 | Ground | 10    |
| AC     | ₹1500 | First  | 10    |
| Deluxe | ₹2000 | Second | 10    |

---

## 🎯 Concepts Covered

✔ HTTP Methods (GET, POST, PUT, DELETE)
✔ Query Parameters
✔ Pydantic Models & Validation
✔ Clean Code using Helper Functions
✔ CRUD Operations
✔ Status Codes
✔ Search, Sort & Pagination
✔ Multi-step Workflow

---

## 🚀 Future Enhancements

* 🔐 Authentication (Admin/User roles)
* 🗄 Database Integration (MySQL/PostgreSQL)
* 🌐 Frontend (React)
* ☁️ Cloud Deployment

---

# 🏨 Hotel Management System (FastAPI)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)
![Status](https://img.shields.io/badge/Project-Completed-success.svg)

A complete **Hotel Management System API** built using **FastAPI**.
This project demonstrates real-world backend concepts like **auto room allocation, booking workflow, CRUD operations, filtering, sorting, pagination, and account tracking**.

---

## 🚀 Features

✨ Auto Room Allocation (System assigns room number)
✨ Booking, Update, Cancel & Checkout Workflow
✨ Room Categories (Non-AC, AC, Deluxe)
✨ Admin Module (Booking history & summary)
✨ Search, Sort & Filter functionality
✨ Pagination & Combined Browse API
✨ Room Catalog (Live availability status)
✨ Account tracking (Revenue + records)
✨ Strong input validation using Pydantic
✨ Proper HTTP status codes

---

## 🧠 Tech Stack

* ⚡ FastAPI
* 🐍 Python
* 📦 Pydantic
* 📄 Swagger UI (API Testing)

---

## 📂 Project Structure

```
main.py  → Complete FastAPI application
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/hotel-management-fastapi.git
cd hotel-management-fastapi
```

### 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn
```

### 3️⃣ Run Server

```bash
uvicorn main:app --reload
```

### 4️⃣ Open API Docs

👉 http://127.0.0.1:8000/docs

---

## 📌 API Endpoints

### 🔹 Booking

* `POST /booking` → Book room
* `PUT /booking/update` → Update booking
* `DELETE /booking/cancel` → Cancel booking
* `POST /checkout` → Checkout

### 🔹 Inquiry & Data

* `GET /inquiry` → Check room status
* `GET /search` → Search bookings
* `GET /filter` → Filter records
* `GET /sort` → Sort data

### 🔹 Advanced APIs

* `GET /bookings` → Pagination
* `GET /browse` → Filter + Sort + Pagination
* `GET /rooms/catalog` → Room catalog

### 🔹 Admin

* `GET /admin/bookings` → Booking history
* `GET /admin/summary` → Room summary

### 🔹 Account

* `GET /account` → Revenue & stats

---

## 🔄 Workflow

1️⃣ User books a room
2️⃣ System auto-assigns room number
3️⃣ Room becomes occupied
4️⃣ User can update or cancel booking
5️⃣ Checkout frees the room
6️⃣ All records stored in history
7️⃣ Account tracks revenue

---

## 📊 Room Categories

| Type   | Price | Floor  | Limit |
| ------ | ----- | ------ | ----- |
| Non-AC | ₹1000 | Ground | 10    |
| AC     | ₹1500 | First  | 10    |
| Deluxe | ₹2000 | Second | 10    |

---

## 🎯 Concepts Covered

✔ HTTP Methods (GET, POST, PUT, DELETE)
✔ Query Parameters
✔ Pydantic Models & Validation
✔ Clean Code using Helper Functions
✔ CRUD Operations
✔ Status Codes
✔ Search, Sort & Pagination
✔ Multi-step Workflow

---

## 🚀 Future Enhancements

* 🔐 Authentication (Admin/User roles)
* 🗄 Database Integration (MySQL/PostgreSQL)
* 🌐 Frontend (React)
* ☁️ Cloud Deployment

---

## 👨‍💻 Author

**Name:** Chinmay Jain

**Internship ID:** IN226108102

🔗 LinkedIn: https://www.linkedin.com/in/chinmay-jain-92b195283

Developed as part of a **FastAPI Internship Project** to build strong backend development skills 🚀



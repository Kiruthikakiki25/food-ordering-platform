# Food Ordering & Delivery Platform

A full-stack food ordering and delivery platform with restaurant browsing, cart, order tracking, and real payment integration — built as a Semester-5 capstone project.

## Overview

This platform lets users browse restaurants and menus, add items to a cart, place orders, pay securely via Stripe, and track their order status in real time as it moves through preparation and delivery. It is seeded with a real-world dataset of 300 restaurants and 1,200 dishes to reflect realistic scale and variety rather than a handful of dummy entries.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | React (Vite) + Tailwind CSS v4 |
| Backend | Flask + SQLAlchemy |
| Database | MySQL (via PyMySQL) |
| Auth | JWT (flask-jwt-extended) |
| Payments | Stripe (test mode) |
| Migrations | Flask-Migrate |

## Features

**Auth**
- Register, email verification, login, JWT refresh, forgot/reset password

**Restaurants & Menu**
- Browse restaurants, view menu items per restaurant, search dishes

**Cart & Orders**
- Add items to cart, place an order, view order history
- Order status flow: `placed → preparing → out_for_delivery → delivered`
- Live order tracking (polls status every 5 seconds)

**Payments**
- Stripe Checkout integrated with Elements, styled to match app theme
- Payment confirmation updates order status and triggers automatic status progression

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8 running locally (or a cloud instance)
- A Stripe account (test mode keys)

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
```

Create a `.env` file in `backend/` (see `.env.example` for the full list of variables):

```
DATABASE_URL=mysql+pymysql://<user>:<password>@localhost:3306/food_ordering
JWT_SECRET_KEY=<your-secret-key>
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

Run migrations and seed the database:

```bash
flask db upgrade
python seed.py
```

Start the backend:

```bash
python run.py
```

Backend runs at `http://localhost:5000`.

### Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env.local` file in `frontend/`:

```
VITE_API_URL=http://localhost:5000
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

Start the frontend:

```bash
npm run dev
```

Frontend runs at `http://localhost:5173`.

> **Note:** Backend and frontend must run simultaneously in separate terminals.

## Environment Variables

| Name | Description | Required |
| --- | --- | --- |
| `DATABASE_URL` | MySQL connection string | Yes |
| `JWT_SECRET_KEY` | Secret key for signing JWTs | Yes |
| `STRIPE_SECRET_KEY` | Stripe secret key (backend) | Yes |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key (backend) | Yes |
| `VITE_API_URL` | Backend base URL (frontend) | Yes |
| `VITE_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key (frontend) | Yes |

## Folder Structure

```
food-ordering-platform/
├─ backend/
│  ├─ app/
│  │  ├─ models.py
│  │  ├─ routes/
│  │  │  ├─ auth.py
│  │  │  ├─ menu.py
│  │  │  ├─ orders.py
│  │  │  └─ payments.py
│  │  └─ config.py
│  ├─ migrations/
│  ├─ seed.py
│  └─ run.py
├─ frontend/
│  └─ src/
│     ├─ pages/
│     ├─ components/
│     └─ api/
├─ docs/
│  └─ diagrams/
└─ README.md
```

## Future Enhancements

- Stripe webhook signature verification (replacing the current trust-the-frontend confirm pattern)
- Admin/restaurant management panel
- Address management and delivery notifications
- Cloud deployment (Render + Vercel)

## License

MIT

## Author

Kiruthika S — [GitHub](https://github.com/Kiruthikakiki25)

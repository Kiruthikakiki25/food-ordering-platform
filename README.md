# Food Ordering & Delivery Platform

> One restaurant brand, four branches, one shared menu: order, pay and track online.

## Live Demo

- **Live app (frontend):** https://food-ordering-platform-kohl.vercel.app
- **Live API (backend):** https://food-ordering-platform-qdep.onrender.com (health check: `/health`)


> Both free hosting tiers sleep when idle. The first request can take up to 50 seconds.

## Overview

A restaurant chain with several outlets needs one ordering system. A customer picks a nearby branch, browses the brand's menu, pays online and tracks the order. The menu is stored once and shared by every branch. Each order records the branch that prepares it, and the item prices at the time of ordering.

## Architecture Diagram

See [`docs/diagrams/architecture.md`](docs/diagrams/architecture.md).

```mermaid
flowchart LR
    U[Customer browser] --> F[React app on Vercel]
    F -->|REST + JWT| B[Flask API on Render]
    B --> D[(MySQL on Aiven)]
    B --> S[Stripe test mode]
    G[GitHub Actions] -->|tests, then deploy hook| B
```

Other diagrams: [ER diagram](docs/diagrams/er-diagram.md), [module diagram](docs/diagrams/module-diagram.md).

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), React Router, Axios, Tailwind CSS |
| Backend | Python, Flask, SQLAlchemy, Flask-Migrate, Flask-JWT-Extended, Flask-Mail |
| Database | MySQL (Aiven, SSL) |
| Payments | Stripe (test mode) |
| Testing | pytest (temporary SQLite database) |
| CI/CD | GitHub Actions |
| Hosting | Render (backend), Vercel (frontend), Aiven (database) |

## Features

**Branches and menu**
- List branches, search by name, city or pincode
- One shared menu with categories, descriptions and a veg / non-veg indicator

**Cart and orders**
- Cart carries the selected branch into the order
- Order stores `branch_id` and a price snapshot per item (`price_at_order`)
- Order history for the logged-in user

**Accounts**
- Register and login with JWT access and refresh tokens
- Email verification and password reset flows
- Password rules: 8+ characters, upper case, lower case, digit

**Payments and tracking**
- Stripe test payment; the server confirms the payment with Stripe before marking the order paid
- Order tracking: Placed, Preparing, Out for Delivery, Delivered

**Platform**
- `/health` endpoint with a database check
- CORS limited to the frontend origins
- Automated tests and CI/CD pipeline

## Screenshots

_[Add screenshots: branch picker, menu, cart, checkout, order tracking, order history, green GitHub Actions run]_

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 20+
- MySQL 8 (local or cloud)
- A Stripe account (test keys)

### Clone
```bash
git clone https://github.com/Kiruthikakiki25/food-ordering-platform.git
cd food-ordering-platform
```

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```
Create `backend/.env` (see the table below), then:
```bash
flask db upgrade
python seed.py                 # 4 branches + shared menu
flask run
```
The API runs at http://localhost:5000.

### Frontend
```bash
cd frontend
npm install
```
Create `frontend/.env.local`:
```
VITE_API_URL=http://localhost:5000
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
```
```bash
npm run dev
```
The app runs at http://localhost:5173.

## Environment Variables

**Backend (`backend/.env`, or Render environment)**

| Name | Description | Required |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy URL, e.g. `mysql+pymysql://user:pass@host:port/db?ssl_ca=ca.pem` | Y |
| `SECRET_KEY` | Flask secret key | Y |
| `JWT_SECRET_KEY` | Key used to sign JWTs | Y |
| `STRIPE_SECRET_KEY` | Stripe secret key (`sk_test_...`) | Y |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | N |
| `CORS_ORIGINS` | Comma-separated allowed frontend origins | N (has defaults) |
| `BACKEND_URL` | Public backend URL used in email links | N |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD` | SMTP settings for verification and reset mail | N |

**Frontend (`frontend/.env.local`, or Vercel environment)**

| Name | Description | Required |
|---|---|---|
| `VITE_API_URL` | Backend base URL, no trailing slash | Y |
| `VITE_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key (`pk_test_...`) | Y |

Never commit `.env` files. Secrets belong in the hosting platform's environment settings.

## API Documentation

Hosted Swagger docs are not set up yet _(planned)_. Current endpoints:

| Method | Path | Auth | Purpose |
|---|---|---|---|
| GET | `/health` | No | Service and database status |
| GET | `/branches`, `/branches/<id>` | No | List or read branches |
| GET | `/menu`, `/menu/<id>`, `/menu/search` | No | Shared menu |
| POST | `/auth/register`, `/auth/login` | No | Create account, get tokens |
| GET | `/auth/verify-email/<token>` | No | Verify email |
| POST | `/auth/refresh` | Refresh token | New access token |
| POST | `/auth/forgot-password`, `/auth/reset-password/<token>` | No | Password reset |
| GET | `/auth/me` | JWT | Current user |
| POST | `/orders` | JWT | Place order (`branch_id`, `items`) |
| GET | `/orders/my-orders`, `/orders/<id>` | JWT | Order history and details |
| PATCH | `/orders/<id>/status` | JWT | Update order status |
| POST | `/payments/create-payment-intent` | JWT | Start Stripe payment |
| POST | `/payments/confirm` | JWT | Confirm payment (verified with Stripe) |

## Running Tests

```bash
cd backend
pip install pytest
pytest -v
```
Tests use a temporary in-memory SQLite database and never touch the real database.

## Deployment

- **Database:** Aiven MySQL (free plan, SSL with `ca.pem`)
- **Backend:** Render web service, root directory `backend`, start command `gunicorn run:app`
- **Frontend:** Vercel, root directory `frontend`, Vite preset, `vercel.json` rewrites all routes to `index.html`
- **CI/CD:** `.github/workflows/backend.yml` installs dependencies, lints, runs pytest, and on a push to `main` calls the Render deploy hook (stored as the `RENDER_DEPLOY_HOOK` GitHub secret). `.github/workflows/frontend.yml` builds the frontend.

## Folder Structure

```
food-ordering-platform/
├── .github/workflows/     # backend.yml, frontend.yml
├── backend/
│   ├── app/
│   │   ├── routes/        # auth, branches, menu, orders, payments
│   │   ├── utils/         # token helpers
│   │   ├── config.py
│   │   └── models.py
│   ├── migrations/
│   ├── tests/
│   ├── seed.py
│   └── run.py
├── frontend/
│   └── src/               # pages, components, api
├── docs/diagrams/
├── CHANGELOG.md
└── README.md
```



## Author / Contact

**Kiruthika S**: B.Tech AI & Data Science, J.J. College of Engineering and Technology, Trichy
GitHub: [Kiruthikakiki25](https://github.com/Kiruthikakiki25) | LinkedIn: [kiruthikass](https://linkedin.com/in/kiruthikass)

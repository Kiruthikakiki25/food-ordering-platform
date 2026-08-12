# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added
- `Problem_Statement.md` finalized with entities, roles, success criteria, and scope
- Architecture Diagram, ER Diagram, and Class/Module Diagram (v1) added to `docs/diagrams/`
- README v1 with tech stack, features, and local setup instructions
- LICENSE (MIT) and `.env.example` added

## [v0.1-mvp]

### Added
- Flask app factory and project structure (`backend/app/`)
- Six SQLAlchemy models: `User`, `Restaurant`, `MenuItem`, `Order`, `OrderItem`, `Payment`
- MySQL database schema created and confirmed
- Database seeded with 300 restaurants and 1,200 dishes from a Zomato-based dataset
- JWT authentication routes: register, verify-email, login, refresh, forgot-password, reset-password, me
- Menu browsing routes: restaurant listing, restaurant menu, search
- Order and OrderItem routes: create order, list my orders, get order by id, update order status
- React frontend scaffolded with Vite + Tailwind CSS v4, all core pages built and wired to backend
- End-to-end cart → order → tracking flow tested and working
- Stripe payment integration: payment intent creation, Checkout UI styled to app theme, payment confirmation route
- Order status auto-progression (`placed → preparing → out_for_delivery → delivered`) via background thread
- Live order tracking on the frontend via polling
- Flask-Migrate configured for schema migrations

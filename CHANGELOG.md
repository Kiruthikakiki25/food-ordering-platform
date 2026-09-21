# Changelog

All notable changes at each review are recorded here.

## [0.2.0] - Review-II 

### Changed
- Scope changed from a multi-restaurant marketplace to **one brand with four branches** and a shared menu.
- `Restaurant` replaced by `Branch`; `MenuItem` no longer has a branch link.
- `Order` now stores `branch_id`; `OrderItem` stores `price_at_order`.
- Payment field renamed to `stripe_payment_intent_id`.
- Password hashing method changed to `pbkdf2:sha256` (lower memory use on the free hosting plan).
- CORS limited to the Vercel frontend and localhost.

### Added
- Branch picker, shared menu page, cart with `branch_id`, order tracking and order history pages.
- Stripe test payment, confirmed server-side with Stripe.
- `/health` endpoint with database check.
- 12 pytest tests on a temporary SQLite database.
- GitHub Actions: backend CI/CD (lint, tests, Render deploy hook) and frontend build check.
- Cloud deployment: Aiven MySQL, Render backend, Vercel frontend.
- README v2 and design diagrams in `docs/diagrams/`.

### Fixed
- Registration no longer crashes the server worker; email is sent in a background thread.
- Checkout no longer fails with a duplicate payment row on reload.
- Payment confirmation now verifies the payment with Stripe before marking the order paid.


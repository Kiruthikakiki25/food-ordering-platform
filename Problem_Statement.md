# Problem Statement

## 1. Title
Food Ordering & Delivery Platform

## 2. Domain
Logistics / Food-Tech

## 3. Who is the user?
- **Customer** — browses restaurants and menus, places orders, pays online, and tracks delivery status in real time.
- **Restaurant Admin** (planned) — manages their restaurant's menu items and updates order status as it moves through preparation and delivery.
- **Platform Admin** (planned) — oversees restaurants, users, and orders across the platform.

## 4. What problem are we solving?
Customers who want to order food online need a reliable way to browse restaurant menus, pay securely, and know exactly where their order stands at any moment — without calling the restaurant to ask. On the restaurant side, digitizing the menu, order intake, and order-status workflow removes the need for manual phone-order handling. This project designs and builds that complete flow end-to-end: from account creation and menu discovery, through cart and secure payment, to an order that automatically progresses through real status stages and is tracked live by the customer. For example, a customer should be able to browse restaurants, add dishes to a cart, pay with a card, and watch their order move from "placed" to "delivered" without any manual follow-up from either side.

## 5. Proposed Solution
- Restaurant and menu browsing with search by dish/cuisine
- User registration, email verification, and JWT-based login
- Cart and checkout flow with Stripe payment integration
- Order creation and automatic status progression (`placed → preparing → out_for_delivery → delivered`)
- Real-time order tracking on the customer side via polling
- (Planned) Basic admin capability to manage restaurant menus and manually update order status
- (Planned) A recommendation feature, added as the enhancement phase, suggesting menu items based on order history

## 6. Core Entities / Database Tables
1. **User** — id, name, email, password_hash, is_verified, created_at
2. **Restaurant** — id, name, cuisine, rating
3. **MenuItem** — id, restaurant_id (FK), name, category, price, veg_flag, cuisine_tags
4. **Order** — id, user_id (FK), status, total, created_at
5. **OrderItem** — id, order_id (FK), menu_item_id (FK), quantity
6. **Payment** — id, order_id (FK), stripe_payment_id, status

## 7. User Roles & Permissions
- **Customer** — can register/login, browse restaurants and menus, place orders, make payments, and view/track their own orders only.
- **Admin** — (planned) can add/edit restaurants and menu items, view all orders, and manually update order status.

## 8. Success Criteria
- A registered user should be able to go from browsing a restaurant to a placed, paid order in under 2 minutes.
- Order status should update and be visible to the customer within 5 seconds of a backend status change, without a page refresh.
- Payment failures should be handled gracefully with a clear error shown to the user, without leaving the order in an inconsistent state.

## 9. Out of Scope
- Live GPS-based delivery tracking (status is a simulated pipeline, not real courier location)
- Ordering from multiple restaurants in a single cart/checkout
- Real payouts or settlement to restaurants (payments are collected via Stripe test mode only)
- Native mobile apps (web-responsive only)
- Real-time chat or support between customer and restaurant

## 10. Chosen Track
Python (Flask, using Flask-SQLAlchemy, Flask-JWT-Extended, Flask-Migrate)

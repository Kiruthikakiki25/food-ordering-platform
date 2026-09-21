# ER Diagram (as built)

```mermaid
erDiagram
    USER ||--o{ ORDERS : places
    BRANCH ||--o{ ORDERS : fulfils
    ORDERS ||--|{ ORDER_ITEM : contains
    MENU_ITEM ||--o{ ORDER_ITEM : "ordered as"
    ORDERS ||--o| PAYMENT : "paid by"

    USER {
        int id PK
        string name
        string email UK
        string password_hash
        string address
        bool is_verified
        string role
        datetime created_at
    }
    BRANCH {
        int id PK
        string name
        string address
        string city
        string pincode
        string phone
        time opening_time
        time closing_time
        bool is_active
    }
    MENU_ITEM {
        int id PK
        string name
        string category
        float price
        bool veg_flag
        string cuisine_tags
        string description
        bool is_available
    }
    ORDERS {
        int id PK
        int user_id FK
        int branch_id FK
        string status
        float total
        datetime created_at
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int menu_item_id FK
        int quantity
        float price_at_order
    }
    PAYMENT {
        int id PK
        int order_id FK, UK
        string stripe_payment_intent_id
        string status
        datetime created_at
    }
```

**Design notes**
- The menu has no branch link: it is shared by every branch.
- `price_at_order` keeps past orders correct if a menu price changes.
- `PAYMENT.order_id` is unique: one payment row per order.
- The table is named `ORDERS` here because `ORDER` is a reserved word; in the database it is `order`.

# Architecture Diagram (as built)

```mermaid
flowchart LR
    U[Customer browser] -->|HTTPS| F[React + Vite app<br/>Vercel]
    F -->|REST + JWT<br/>VITE_API_URL| B[Flask API<br/>Render, gunicorn]
    B -->|SQLAlchemy + SSL| D[(MySQL<br/>Aiven)]
    B -->|create / verify PaymentIntent| S[Stripe test mode]
    F -->|Stripe.js card entry| S
    G[GitHub repo] -->|push| A[GitHub Actions<br/>lint + pytest]
    A -->|deploy hook, main only| B
    G -->|push to main| F
```

**Notes**
- The frontend calls the backend directly; CORS allows only the Vercel origin and localhost.
- Card details go from the browser to Stripe; the backend only handles payment intents.
- Deployment to Render is triggered by the pipeline only after tests pass.

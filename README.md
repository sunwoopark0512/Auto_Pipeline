# Multi-Tenant SaaS Kernel

This repository now includes a basic scaffold for a multi-tenant SaaS system.
The core components are:

- `models/tenant.py` – SQLAlchemy model defining tenants and quotas.
- `billing/stripe_hooks.py` – helper functions to create customers and subscriptions via Stripe.
- `billing/metering.py` – record API usage and trigger plan upgrades when quotas are exceeded.
- `middleware/auth_middleware.py` – FastAPI middleware that verifies requests contain a valid API key.

These modules are a starting point for integrating Supabase Auth, Stripe billing and usage metering into the existing pipeline.

"""Stripe billing endpoints for creating Checkout Sessions and handling webhooks.

Uses STRIPE_API_KEY and STRIPE_WEBHOOK_SECRET from environment.
"""

import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

try:
    import stripe
except Exception:  # pragma: no cover - stripe must be installed in production/tests
    stripe = None

router = APIRouter(prefix="/billing", tags=["billing"])

STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
if stripe:
    stripe.api_key = STRIPE_API_KEY


@router.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    """Create a Stripe Checkout Session for a subscription price.

    JSON body: {"price_id": "price_xxx", "success_url": "http://...", "cancel_url": "http://..."}
    """
    if stripe is None:
        raise HTTPException(status_code=500, detail="Stripe library not available")

    try:
        payload = await request.json()
    except Exception:
        payload = {}

    price_id = payload.get("price_id") or os.getenv("STRIPE_DEFAULT_PRICE_ID")
    success_url = payload.get("success_url") or os.getenv("FRONTEND_SUCCESS_URL", "http://localhost:3000/success")
    cancel_url = payload.get("cancel_url") or os.getenv("FRONTEND_CANCEL_URL", "http://localhost:3000/cancel")

    if not price_id:
        raise HTTPException(status_code=400, detail="Missing price_id")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url,
        )
        # stripe.checkout.Session.create returns an object-like mapping
        session_url = getattr(session, "url", None) or session.get("url")
        session_id = getattr(session, "id", None) or session.get("id")
        return {"id": session_id, "url": session_url}

    except Exception as exc:
        # Bubble up Stripe errors as 500
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/webhook")
async def webhook(request: Request):
    """Verify webhook signature and return 200 if valid.

    This endpoint verifies Stripe signature using STRIPE_WEBHOOK_SECRET.
    """
    if stripe is None:
        raise HTTPException(status_code=500, detail="Stripe library not available")

    payload_bytes = await request.body()
    try:
        payload = payload_bytes.decode("utf-8")
    except Exception:
        payload = payload_bytes

    sig_header = request.headers.get("stripe-signature", "")
    webhook_secret = STRIPE_WEBHOOK_SECRET
    if not webhook_secret:
        raise HTTPException(status_code=500, detail="Stripe webhook secret not configured")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except Exception:
        # Could be ValueError (invalid payload) or SignatureVerificationError
        raise HTTPException(status_code=400, detail="Invalid payload or signature")

    # Minimal event handling - extend as needed
    etype = event.get("type") if isinstance(event, dict) else getattr(event, "type", None)
    if etype == "checkout.session.completed":
        # session = event["data"]["object"]  # implement fulfillment if needed
        pass

    return JSONResponse(status_code=200, content={"received": True})
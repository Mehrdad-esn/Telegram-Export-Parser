import os
from fastapi.testclient import TestClient

# Ensure test env is configured before importing the app
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_test")

from backend.app.main import app
import stripe

client = TestClient(app)


def test_webhook_signature_valid(monkeypatch):
    """When Stripe verifies signature, webhook should return 200."""

    def fake_construct_event(payload, sig_header, secret):
        return {"type": "checkout.session.completed", "data": {"object": {"id": "sess_123"}}}

    monkeypatch.setattr(stripe.Webhook, "construct_event", fake_construct_event)

    resp = client.post("/billing/webhook", data=b'{"id":"evt_123"}', headers={"stripe-signature": "t=1,v1=abc"})
    assert resp.status_code == 200
    assert resp.json() == {"received": True}


def test_webhook_signature_invalid(monkeypatch):
    """When signature verification fails, webhook should return 400."""

    from stripe.error import SignatureVerificationError

    def raise_sig(payload, sig_header, secret):
        raise SignatureVerificationError("Invalid signature", sig_header)

    monkeypatch.setattr(stripe.Webhook, "construct_event", raise_sig)

    resp = client.post("/billing/webhook", data=b'{"id":"evt_123"}', headers={"stripe-signature": "t=1,v1=bad"})
    assert resp.status_code == 400

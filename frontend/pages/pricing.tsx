import React from "react";

export default function Pricing() {
  const handleCheckout = async () => {
    try {
      const res = await fetch("/billing/create-checkout-session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ price_id: process.env.NEXT_PUBLIC_STRIPE_PRICE_ID || "price_test" }),
      });

      if (!res.ok) {
        const text = await res.text();
        alert("Error creating checkout session: " + text);
        return;
      }

      const data = await res.json();
      if (data.url) {
        // Redirect the browser to Stripe Checkout
        window.location.href = data.url;
      } else {
        alert("No checkout URL returned");
      }
    } catch (err) {
      // Simple error handling for demo purposes
      alert("Checkout failed: " + err);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Pricing</h1>
      <p>Subscribe to the Pro plan.</p>
      <button onClick={handleCheckout}>Subscribe</button>
    </div>
  );
}

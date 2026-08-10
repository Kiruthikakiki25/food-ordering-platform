import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { loadStripe } from "@stripe/stripe-js";
import {
  Elements,
  CardElement,
  useStripe,
  useElements,
} from "@stripe/react-stripe-js";
import apiClient from "../api/client";

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY);

const cardElementOptions = {
  style: {
    base: {
      fontSize: "16px",
      color: "#292524", // stone-800
      "::placeholder": { color: "#a8a29e" }, // stone-400
    },
    invalid: { color: "#dc2626" }, // red-600, matches your error state color
  },
};

function CheckoutForm({ orderId, clientSecret, amount }) {
  const stripe = useStripe();
  const elements = useElements();
  const navigate = useNavigate();
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!stripe || !elements) return;

    setProcessing(true);
    setError("");

    const result = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: elements.getElement(CardElement),
      },
    });

    if (result.error) {
      setError(result.error.message);
      setProcessing(false);
    } else if (result.paymentIntent.status === "succeeded") {
      await apiClient.post("/payments/confirm", { order_id: orderId });
      navigate(`/orders/${orderId}`);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="border border-stone-300 rounded-lg p-4 mb-4">
        <CardElement options={cardElementOptions} />
      </div>

      {error && (
        <p className="text-red-600 text-sm mb-4">{error}</p>
      )}

      <button
        type="submit"
        disabled={!stripe || processing}
        className="w-full bg-red-900 hover:bg-red-800 disabled:bg-stone-400 text-white font-semibold py-3 rounded-lg transition"
      >
        {processing ? "Processing..." : `Pay ₹${amount}`}
      </button>
    </form>
  );
}

export default function Checkout() {
  const { orderId } = useParams();
  const [clientSecret, setClientSecret] = useState(null);
  const [amount, setAmount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const createIntent = async () => {
      try {
        const res = await apiClient.post("/payments/create-payment-intent", {
          order_id: orderId,
        });
        setClientSecret(res.data.client_secret);
        setAmount(res.data.amount);
      } catch (err) {
        setError("Could not initialize payment. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    createIntent();
  }, [orderId]);

  return (
    <div className="min-h-screen bg-orange-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-xl shadow-md p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold text-red-900 mb-1">Checkout</h1>
        <p className="text-stone-500 mb-6">Order #{orderId}</p>

        {loading && <p className="text-stone-500">Loading payment form...</p>}
        {error && <p className="text-red-600">{error}</p>}

        {clientSecret && (
          <Elements stripe={stripePromise}>
            <CheckoutForm
              orderId={orderId}
              clientSecret={clientSecret}
              amount={amount}
            />
          </Elements>
        )}
      </div>
    </div>
  );
}

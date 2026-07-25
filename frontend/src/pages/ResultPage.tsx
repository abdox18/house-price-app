import { useLocation, useNavigate } from "react-router-dom";

function formatIndianPrice(value: number): string {
  if (value >= 1e7) return `₹ ${(value / 1e7).toFixed(2)} Cr`;
  if (value >= 1e5) return `₹ ${(value / 1e5).toFixed(2)} Lac`;
  return `₹ ${value.toLocaleString("en-IN")}`;
}

interface LocationState {
  price?: number;
}

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = (location.state as LocationState) || {};

  if (state.price === undefined) {
    return (
      <main className="page">
        <h1>No prediction yet</h1>
        <p>Please fill out the form first.</p>
        <button onClick={() => navigate("/")}>Back to form</button>
      </main>
    );
  }

  return (
    <main className="page">
      <h1>Estimated price</h1>
      <p className="predicted-price">{formatIndianPrice(state.price)}</p>
      <button onClick={() => navigate("/")}>Predict another property</button>
    </main>
  );
}

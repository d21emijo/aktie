import React, { useState } from "react";

function PredictForm() {
  const [ticker, setTicker] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault(); 

    fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ ticker: ticker.toUpperCase() }) 
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Prediction klar:", data);
      })
      .catch((err) => console.error("Fel:", err));
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="ticker">Ange ticker:</label>
      <input
        id="ticker"
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        placeholder="t.ex. AAPL"
      />
      <button type="submit">Kör prediction</button>
    </form>
  );
}

export default PredictForm;

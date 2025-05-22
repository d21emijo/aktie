import React, { useEffect, useState } from 'react';

function LastPrediction() {
  const [predictions, setPredictions] = useState([]);

useEffect(() => {
  fetch("http://localhost:5000/last_prediction")
    .then((res) => res.json())
    .then((data) => {
      setPredictions(data.predictions);
    })
    .catch((err) => console.error(err));
}, []);

  return (
    <div>
      <h1>Latest Prediction</h1>
      <table>
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Accuracy</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {predictions.map((item, index) => (
            <tr key={index}>
              <td>{item.ticker}</td>
              <td>{item.accuracy.toFixed(2)}</td>
              <td>{new Date(item.time).toLocaleString('sv-SE')}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default LastPrediction;
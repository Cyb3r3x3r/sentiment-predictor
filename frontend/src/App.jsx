import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Prediction failed:", err);
      setResult({ label: "error", score: 0 });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Sentiment Predictor</h1>
      <textarea
        style={styles.textarea}
        rows="5"
        placeholder="Type your sentence..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button style={styles.button} onClick={handlePredict} disabled={loading || !text}>
        {loading ? "Predicting..." : "Predict"}
      </button>

      {result && (
        <div style={styles.result}>
          <p><strong>Label:</strong> {result.label}</p>
          <p><strong>Confidence:</strong> {(result.score * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "600px",
    margin: "2rem auto",
    padding: "1rem",
    textAlign: "center",
    fontFamily: "Arial, sans-serif",
  },
  textarea: {
    width: "100%",
    padding: "1rem",
    fontSize: "1rem",
    marginBottom: "1rem",
  },
  button: {
    padding: "0.5rem 1.5rem",
    fontSize: "1rem",
    cursor: "pointer",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "4px",
  },
  result: {
    marginTop: "1rem",
    padding: "1rem",
    backgroundColor: "#f0f0f0",
    borderRadius: "8px",
  },
};

export default App;

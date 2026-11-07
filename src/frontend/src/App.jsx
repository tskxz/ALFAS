import React, { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/api/hello")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("Erro ao ligar ao backend."));
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "5rem", fontFamily: "sans-serif" }}>
      <h1>{message || "A carregar..."}</h1>
      <p>Flask + React a funcionar 🚀</p>
    </div>
  );
}

export default App;


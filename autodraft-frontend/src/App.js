import React, { useState } from "react";
import "./App.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setDownloadUrl("");

    try {
      const res = await fetch("http://localhost:8000/generate-drawing", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();

      if (res.ok && data.file) {
        setDownloadUrl(`http://localhost:8000${data.file}`);
      } else {
        alert("Error generating drawing.");
      }
    } catch (err) {
      alert("Server error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>AutoDraft</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe your layout..."
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Drawing"}
        </button>
      </form>

      {downloadUrl && (
        <div className="result">
          <a href={downloadUrl} download>
            Download DXF File
          </a>
        </div>
      )}
    </div>
  );
}

export default App;

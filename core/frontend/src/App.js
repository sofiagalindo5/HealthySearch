import React, { useState } from "react";
import './App.css';

function App() {
  const [location, setLocation] = useState("");
  const [lat, setLat] = useState(null);
  const [lon, setLon] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const useMyLocation = () => {
  if (!navigator.geolocation) {
    alert("Geolocation is not supported by your browser.");
    return;
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const newLat = position.coords.latitude;
      const newLon = position.coords.longitude;
      setLat(newLat);
      setLon(newLon);
      setLocation(""); // clear manual input
      searchRestaurants(newLat, newLon, "");
    },
    () => {
      alert("Unable to retrieve your location.");
    }
  );
};

const handleSubmit = (e) => {
  e.preventDefault();
  searchRestaurants(lat, lon, location);
};

const searchRestaurants = async (customLat = null, customLon = null, customLocation = "") => {
  setLoading(true);
  setError("");
  setResults([]);

  let url = "http://localhost:8000/search/api/search/";

  if (customLat !== null && customLon !== null) {
    url += `?lat=${customLat}&lon=${customLon}`;
  } else if (customLocation) {
    url += `?location=${encodeURIComponent(customLocation)}`;
  } else {
    setLoading(false);
    setError("Please enter a location or use your current location.");
    return;
  }

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Failed to fetch data.");
    }
    const data = await response.json();
    setResults(data);
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className ='container'>
      <h1>Healthy Search</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          placeholder="Enter a city (e.g., New York)"
          value={location}
          onChange={(e) => {
            setLocation(e.target.value);
            setLat(null); // reset lat/lon if user types manually
            setLon(null);
          }}
          style={{ marginRight: "0.5rem", padding: "0.5rem" }}
        />
        <button type="button" onClick={useMyLocation} style={{ marginRight: "0.5rem" }}>
          Use My Location
        </button>
        <button type="submit">Search</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {results.length > 0 && (
        <div>
          <h2>Healthy Restaurants Nearby</h2>
          <ul>
            {results.map((r, i) => (
              <li key={i} style={{ marginBottom: "1rem" }}>
                <strong>{r.name}</strong><br />
                {r.address}<br />
                <em>{r.categories}</em>
              </li>
            ))}
          </ul>
        </div>
      )}

      {results.length === 0 && !loading && !error && (
        <p>No results yet. Try searching!</p>
      )}
    </div>
  );
}

export default App;
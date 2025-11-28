import React, { useState } from "react";
import "../css/SearchBar.css"; // create CSS for slider

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState("");
  const [regex, setRegex] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() !== "") {
      onSearch(query, regex);
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Search books..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      {/* Regex toggle slider */}
      <label className="switch">
        <input
          type="checkbox"
          checked={regex}
          onChange={() => setRegex(!regex)}
        />
        <span className="slider"></span>
      </label>
      <span style={{ marginLeft: "8px" }}>Regex</span>

      <button type="submit">Search</button>
    </form>
  );
}

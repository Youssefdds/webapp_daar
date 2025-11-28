import React, { useState, useEffect } from "react";
import SearchBar from "./SearchBar";
import BookList from "./BookList";
import "../css/LibraryApp.css";

export default function LibraryApp() {
  const [results, setResults] = useState([]);
  const [q, setQ] = useState("");
  const [page, setPage] = useState(1);
  const [modalContent, setModalContent] = useState(null);
  const [selectedSuggestions, setSelectedSuggestions] = useState(null);
  const [regex, setRegex] = useState(false);
  const [centrality, setCentrality] = useState(false);
  
  // Recherche classique
  const fetchResults = async (query, regexMode = false) => {
    setQ(query);
    const endpoint = regexMode ? "/api/search/regex/" : "/api/search/";
    const url = `${endpoint}?q=${encodeURIComponent(
      query
    )}&page=${page}&size=40`;

    try {
      const res = await fetch(url);
      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
    }
  };

  // Recherche enrichie avec centralité
  const performEnhancedSearch = async (query, regexMode = false) => {
    setQ(query);

    // Construire l'URL par concaténation (compatible avec proxy CRA)
    let url = `/api/enhanced-search/?q=${encodeURIComponent(query)}&page=${page}&size=40&centrality=true`;

    if (regexMode) {
      url += `&regex=true`;
    }

    try {
      const res = await fetch(url);
      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
    }
  };
  // Gestion du submit depuis la SearchBar
  const handleSearch = async (query, regexMode) => {
    if (centrality) {
      // Utiliser enhanced search seulement si centrality activé
      performEnhancedSearch(query, regexMode);
    } else {
      fetchResults(query, regexMode);
    }
  };

  // Ouvrir le contenu d’un livre
  // Ouvrir le contenu d’un livre
  const openContent = async (id) => {
    const url = `http://127.0.0.1:8000/api/book_content/?id=${id}`;
    window.open(url, "_blank");
  };



  // Voir les suggestions
  const handleViewSuggestions = async (bookId) => {
    try {
      const res = await fetch("/api/suggestions/");
      const data = await res.json();

      // Récupérer les suggestions du bookId
      const bookSuggestions = data.results.find((b) => b.id === bookId);
      setSelectedSuggestions(bookSuggestions);
    } catch (err) {
      console.error("Error fetching suggestions", err);
    }
  };

  // Re-fetch si page change
  useEffect(() => {
    if (q.trim() !== "") {
      if (centrality) performEnhancedSearch(q, regex);
      else fetchResults(q, regex);
    }
  }, [page]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="library-app">
      <header>
        <h1>My Library</h1>
        <p>Search for books from the API</p>
      </header>

      {/* Search bar avec regex toggle */}
      <SearchBar
        onSearch={handleSearch}
        regex={regex}
        setRegex={setRegex}
      />

      {/* Slider centrality */}
      <div style={{ margin: "10px 0", display: "flex", alignItems: "center" }}>
        <label className="switch">
          <input
            type="checkbox"
            checked={centrality}
            onChange={() => setCentrality(!centrality)}
          />
          <span className="slider"></span>
        </label>
        <span style={{ marginLeft: "8px" }}>Use Centrality</span>
      </div>

      {/* Liste de livres */}
      <BookList
        books={results}
        onViewContent={openContent}
        onViewSuggestions={handleViewSuggestions}
      />

      {/* Pagination */}
      {results.length > 0 && (
        <div className="pagination">
          <button
            onClick={() => setPage((p) => Math.max(p - 1, 1))}
            disabled={page === 1}
          >
            Previous
          </button>
          <span>Page {page}</span>
          <button onClick={() => setPage((p) => p + 1)}>Next</button>
        </div>
      )}
    </div>
  );
}

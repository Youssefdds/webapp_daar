import React from "react";
import { useNavigate } from "react-router-dom";

export default function BookCard({ book ,onViewContent,onViewSuggestions }) {
  const navigate = useNavigate();

  return (
    <div className="book-card">
      <img src={book.image_url} alt={book.title} />
      <h3>{book.title}</h3>
      <p>{book.author}</p>
      <p>Score: {book.score}</p>
      {/* <a href={book.image_url} target="_blank" rel="noreferrer">Cover</a> */}
      <button className="view-button" onClick={() => onViewContent(book.id)}>View Content</button>
      <button
        className="suggest-button"
        onClick={() => navigate(`/suggestions/${book.id}`)}
      >
        View Suggestions
      </button>
    </div>
  );
}

import React from "react";
import BookCard from "./BookCard";

export default function BookList({ books,onViewContent,onViewSuggestions  }) {
  if (!books.length) return <p>No results found.</p>;

  return (
    <div className="results">
      {books.map((book, idx) => (
        <BookCard key={idx} book={book} onViewContent={onViewContent} onViewSuggestions={onViewSuggestions}  />
      ))}
    </div>
  );
}

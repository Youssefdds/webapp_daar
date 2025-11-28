import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom"; 
import "../css/SimilarBooksPage.css";

function SimilarBooksPage() {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const res = await fetch(`/api/suggestions/?id=${id}`);
        const data = await res.json();

        // Ici on met aussi le titre du livre courant
        setBook({
          id: data.id,
          title: data.title || `Book ${data.id}`, // fallback si le titre n'est pas présent
          suggestions: data.results || [],
        });

      } catch (err) {
        console.error("Failed to fetch suggestions:", err);
        setBook({ title: "", suggestions: [] });
      } finally {
        setLoading(false);
      }
    };

    fetchSuggestions();
  }, [id]);

  if (loading) return <p>Loading suggestions...</p>;
  if (!book || !book.suggestions || book.suggestions.length === 0)
    return <p>No suggestions found for this book.</p>;

  return (
    <div className="similar-container">
      <h1>Suggestions for: {book.title}</h1>

      <div className="books-horizontal-scroll">
        {book.suggestions.map((s) => (
          <div key={s.id} className="book-card">
            <img src={s.image_url} alt={s.title} className="book-cover" />
            <div className="book-info">
              <h3 className="book-title">{s.title}</h3>
              <p className="book-author">{s.author}</p>
              <a
                href={`/api/book_content/?id=${s.id}`}
                target="_blank"
                rel="noreferrer"
              >
                View Content
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SimilarBooksPage;

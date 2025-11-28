import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LibraryApp from "./components/LibraryApp";
import SuggestionsPage from "./components/SuggestionsPage";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LibraryApp />} />
        <Route path="/suggestions/:id" element={<SuggestionsPage />} />
      </Routes>
    </Router>
  );
}

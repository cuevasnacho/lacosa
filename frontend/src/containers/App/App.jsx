import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import './App.css';
import Inicio from '../../components/Inicio/Inicio.jsx';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/main" element={<h1>Main</h1>} />
        <Route path="*" element={<h1>Error 404 - Not found</h1>} />
      </Routes>
    </Router>
  );
}

export default App;
// src/components/Navbar.jsx
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-red-900 shadow-md sticky top-0 z-10">
      <Link to="/" className="text-2xl font-extrabold text-white">
        Food<span className="text-amber-500">App</span>
      </Link>
      <div className="flex items-center gap-6">
        <Link to="/cart" className="text-red-50 hover:text-amber-400 font-medium transition-colors">
          Cart
        </Link>
        <Link to="/login" className="text-red-50 hover:text-amber-400 font-medium transition-colors">
          Login
        </Link>
        <Link
          to="/register"
          className="bg-amber-600 text-white font-semibold px-4 py-2 rounded-lg hover:bg-amber-700 transition-colors"
        >
          Register
        </Link>
      </div>
    </nav>
  );
}
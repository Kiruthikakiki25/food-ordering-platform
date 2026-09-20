// src/components/Navbar.jsx
import { Link, useNavigate, useLocation } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  useLocation(); // re-render on every page change so the login state stays fresh
  const loggedIn = !!localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  const linkClass = 'text-red-50 hover:text-amber-400 font-medium transition-colors';

  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-red-900 shadow-md sticky top-0 z-10">
      <Link to="/" className="text-2xl font-extrabold text-white">
        Food<span className="text-amber-500">App</span>
      </Link>
      <div className="flex items-center gap-6">
        <Link to="/cart" className={linkClass}>
          Cart
        </Link>
        {loggedIn ? (
          <>
            <Link to="/my-orders" className={linkClass}>
              My Orders
            </Link>
            <button onClick={handleLogout} className={linkClass}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className={linkClass}>
              Login
            </Link>
            <Link
              to="/register"
              className="bg-amber-600 text-white font-semibold px-4 py-2 rounded-lg hover:bg-amber-700 transition-colors"
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
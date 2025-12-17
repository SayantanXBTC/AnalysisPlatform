import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Home, LogOut, Sparkles, BarChart3 } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../api';

function Navbar({ setAuth }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = async () => {
    try {
      await api.post('/logout');
      setAuth(false);
      toast.success('Logged out successfully', {
        icon: '👋',
        style: {
          borderRadius: '12px',
        },
      });
      navigate('/login');
    } catch (error) {
      toast.error('Logout failed');
    }
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className={`sticky top-0 z-50 transition-all duration-500 ${
      scrolled 
        ? 'glass shadow-2xl border-b border-white/20' 
        : 'bg-white/80 backdrop-blur-sm shadow-lg border-b-2 border-blue-100'
    }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div 
            className="flex items-center space-x-3 cursor-pointer group"
            onClick={() => navigate('/dashboard')}
          >
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:shadow-2xl group-hover:scale-110 transition-all duration-300 hover-glow">
              <Sparkles className="w-7 h-7 text-white group-hover:rotate-12 transition-transform duration-300" />
            </div>
            <div className="hidden sm:block">
              <span className="text-2xl font-bold gradient-text group-hover:scale-105 transition-transform duration-300 inline-block">
                Drug Analysis
              </span>
              <div className="text-xs text-gray-500 font-medium">AI-Powered Intelligence</div>
            </div>
          </div>
          
          {/* Navigation Items */}
          <div className="flex items-center space-x-2 sm:space-x-3">

            {/* Dashboard Button */}
            <button
              onClick={() => navigate('/dashboard')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl font-medium transition-all duration-300 transform hover:scale-105 press-effect ${
                isActive('/dashboard')
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                  : 'text-gray-700 hover:bg-blue-50 hover:text-blue-600'
              }`}
            >
              <Home className="w-5 h-5" />
              <span className="hidden sm:inline">Dashboard</span>
            </button>

            {/* Analysis Button (if on analysis page) */}
            {isActive('/analysis') && (
              <button
                className="flex items-center space-x-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white px-4 py-2 rounded-xl shadow-lg font-medium"
              >
                <BarChart3 className="w-5 h-5" />
                <span className="hidden sm:inline">Analysis</span>
              </button>
            )}
            
            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 bg-gradient-to-r from-red-600 to-red-700 text-white px-4 py-2 rounded-xl hover:from-red-700 hover:to-red-800 transition-all duration-300 shadow-lg hover:shadow-red-500/50 transform hover:scale-105 press-effect group"
            >
              <LogOut className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </div>
      </div>

      {/* Gradient underline animation */}
      <div className={`h-1 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 transition-all duration-500 ${
        scrolled ? 'opacity-100' : 'opacity-0'
      }`}></div>
    </nav>
  );
}

export default Navbar;

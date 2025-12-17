import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { LogIn, Sparkles, AlertCircle, Eye, EyeOff } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import api from '../api';

function Login({ setAuth }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      await api.post('/login', { username, password });
      setAuth(true);
      toast.success('Welcome back!', {
        icon: '🎉',
        style: {
          borderRadius: '12px',
          background: '#10b981',
          color: '#fff',
        },
      });
      navigate('/dashboard');
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Login failed';
      setError(errorMsg);
      toast.error(errorMsg, {
        style: {
          borderRadius: '12px',
        },
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center particles-bg bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-4 animate-fadeIn">
      <Toaster position="top-right" />
      
      {/* Floating particles effect */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-20 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float"></div>
        <div className="absolute top-40 right-20 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{ animationDelay: '2s' }}></div>
        <div className="absolute bottom-20 left-1/2 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-float" style={{ animationDelay: '4s' }}></div>
      </div>

      <div className="relative premium-card p-10 w-full max-w-md animate-scaleIn z-10">
        {/* Logo */}
        <div className="flex justify-center mb-8 animate-float">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-3xl flex items-center justify-center shadow-2xl hover-glow">
            <Sparkles className="w-10 h-10 text-white animate-pulse" />
          </div>
        </div>
        
        {/* Heading with typing effect */}
        <div className="text-center mb-8">
          <h2 className="text-4xl font-bold gradient-text mb-3">
            Welcome Back
          </h2>
          <p className="text-lg text-gray-600 animate-slideDown">
            Your AI-Powered Research Companion
          </p>
        </div>
        
        {/* Error banner with slide animation */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 px-5 py-4 rounded-xl mb-6 flex items-start space-x-3 animate-slideDown shadow-lg">
            <AlertCircle className="w-6 h-6 mt-0.5 flex-shrink-0 animate-pulse" />
            <span className="font-medium">{error}</span>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Username Input */}
          <div className="relative">
            <label className="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-5 py-4 bg-white border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-300 text-lg hover:border-gray-300 shadow-sm"
              placeholder="Enter your username"
              required
            />
          </div>
          
          {/* Password Input with toggle */}
          <div className="relative">
            <label className="block text-gray-700 font-semibold mb-2 text-sm uppercase tracking-wide">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-5 py-4 bg-white border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-300 text-lg hover:border-gray-300 shadow-sm pr-12"
                placeholder="Enter your password"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>
          
          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white py-4 rounded-xl hover:from-blue-700 hover:via-purple-700 hover:to-pink-700 transition-all duration-500 font-bold text-lg shadow-2xl hover:shadow-blue-500/50 transform hover:scale-[1.02] press-effect disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-3 relative overflow-hidden group"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
            <LogIn className="w-6 h-6 relative z-10" />
            <span className="relative z-10">{loading ? 'Signing in...' : 'Sign In'}</span>
          </button>
        </form>
        
        {/* Sign up link */}
        <p className="text-center text-gray-600 mt-8 animate-fadeIn">
          Don't have an account?{' '}
          <Link 
            to="/signup" 
            className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 font-bold hover:underline transition-all"
          >
            Sign up now
          </Link>
        </p>

        {/* Decorative elements */}
        <div className="absolute -top-4 -right-4 w-24 h-24 bg-gradient-to-br from-blue-400 to-purple-400 rounded-full opacity-20 blur-2xl"></div>
        <div className="absolute -bottom-4 -left-4 w-24 h-24 bg-gradient-to-br from-purple-400 to-pink-400 rounded-full opacity-20 blur-2xl"></div>
      </div>
    </div>
  );
}

export default Login;

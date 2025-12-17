import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect, createContext, useContext } from 'react';
import { Loader2 } from 'lucide-react';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import StrategicDashboard from './pages/StrategicDashboard';
import Analysis from './pages/Analysis';
import StrategicAnalysis from './pages/StrategicAnalysis';
import Pricing from './pages/Pricing';
import api from './api';

// Subscription Context
export const SubscriptionContext = createContext(null);

export const useSubscription = () => {
  const context = useContext(SubscriptionContext);
  // Return default values if context is not available
  if (!context) {
    return {
      subscription: {
        subscription_tier: 'FREE',
        subscription_status: 'inactive',
        analyses_this_month: 0,
        analyses_limit: 5,
        can_generate_pdf: false,
        can_use_rag: false
      },
      refreshSubscription: async () => {}
    };
  }
  return context;
};

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [subscription, setSubscription] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      await api.get('/me');
      setIsAuthenticated(true);
      await fetchSubscription();
    } catch (error) {
      // User not authenticated - this is normal on first visit
      setIsAuthenticated(false);
      setSubscription(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchSubscription = async () => {
    try {
      const response = await api.get('/subscription-status');
      setSubscription(response.data);
    } catch (error) {
      console.error('Failed to fetch subscription:', error);
      // Set default subscription for unauthenticated users
      setSubscription({
        subscription_tier: 'FREE',
        subscription_status: 'inactive',
        analyses_this_month: 0,
        analyses_limit: 5,
        can_generate_pdf: false,
        can_use_rag: false
      });
    }
  };

  const refreshSubscription = async () => {
    await fetchSubscription();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center particles-bg bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
        <div className="animate-float">
          <Loader2 className="w-16 h-16 text-blue-600 animate-spin mb-6" />
        </div>
        <div className="text-2xl font-bold gradient-text animate-pulse-glow">
          Loading Drug Analysis Platform...
        </div>
        <div className="mt-4 text-sm text-gray-500 animate-fadeIn">
          Initializing AI agents...
        </div>
      </div>
    );
  }

  return (
    <SubscriptionContext.Provider value={{ subscription, refreshSubscription }}>
      <Router>
        <div className="page-transition">
          <Routes>
            <Route path="/login" element={<Login setAuth={setIsAuthenticated} />} />
            <Route path="/signup" element={<Signup setAuth={setIsAuthenticated} />} />
            <Route path="/dashboard" element={<StrategicDashboard setAuth={setIsAuthenticated} />} />
            <Route path="/dashboard-legacy" element={<Dashboard setAuth={setIsAuthenticated} />} />
            <Route path="/analysis" element={<StrategicAnalysis setAuth={setIsAuthenticated} />} />
            <Route path="/analysis-legacy" element={<Analysis setAuth={setIsAuthenticated} />} />
            <Route path="/pricing" element={<Pricing setAuth={setIsAuthenticated} />} />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      </Router>
    </SubscriptionContext.Provider>
  );
}

export default App;
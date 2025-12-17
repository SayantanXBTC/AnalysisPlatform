import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, Send, Lightbulb, TrendingUp, Shield } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import { useSubscription } from '../App';
import Navbar from '../components/Navbar';
import api from '../api';

function StrategicDashboard({ setAuth }) {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { subscription, refreshSubscription } = useSubscription();

  const examplePrompts = [
    "Which respiratory diseases show low competition but high unmet need in India?",
    "Identify value-added opportunities for off-patent cardiovascular molecules",
    "Explore repurposing scope for anti-inflammatory drugs in pediatric populations",
    "What molecules nearing patent expiry could be reformulated for CNS indications?",
    "Find innovation opportunities where market saturation is low but disease burden is high"
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!prompt.trim()) {
      toast.error('Please enter a query');
      return;
    }

    setLoading(true);
    const toastId = toast.loading('Analyzing your query with AI agents...', {
      style: { borderRadius: '12px' }
    });
    
    try {
      const response = await api.post('/run-analysis', {
        strategic_prompt: prompt
      });
      
      toast.success('Analysis complete!', { 
        id: toastId,
        icon: '✨',
        style: { borderRadius: '12px' }
      });
      navigate('/analysis', { state: { analysisData: response.data } });
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Analysis failed. Please try again.';
      toast.error(errorMsg, { id: toastId });
      setLoading(false);
    }
  };

  const handleExampleClick = (examplePrompt) => {
    setPrompt(examplePrompt);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      <Toaster position="top-right" />
      <Navbar setAuth={setAuth} />
      
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="text-center mb-12 animate-fadeIn">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-semibold mb-6">
            <Sparkles className="w-4 h-4" />
            <span>AI-Powered Drug Intelligence Platform</span>
          </div>
          
          <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 mb-6">
            Discover drug opportunities with
            <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent pb-2" style={{ lineHeight: '1.3' }}>
              multi-agent AI analysis
            </span>
          </h1>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Analyze drug repurposing potential, market opportunities, clinical evidence, patent landscapes, 
            and safety profiles using 10+ specialized AI agents working together.
          </p>
        </div>

        {/* Main Prompt Input */}
        <div className="premium-card p-8 mb-8 animate-scaleIn">
          <form onSubmit={handleSubmit}>
            <div className="relative">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="e.g., Which respiratory diseases show low competition but high unmet need in India?"
                className="w-full px-6 py-5 pr-16 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-300 text-lg resize-none"
                rows="4"
                disabled={loading}
              />
              
              <button
                type="submit"
                disabled={loading || !prompt.trim()}
                className="absolute bottom-4 right-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed group"
              >
                <Send className={`w-5 h-5 ${loading ? 'animate-pulse' : 'group-hover:translate-x-0.5 transition-transform'}`} />
              </button>
            </div>
            
            {loading && (
              <div className="mt-4 flex items-center space-x-3 text-blue-600">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
                <span className="text-sm font-medium">Analyzing market dynamics, clinical evidence, and strategic opportunities...</span>
              </div>
            )}
          </form>
        </div>

        {/* Example Prompts */}
        <div className="mb-12">
          <div className="flex items-center space-x-2 mb-4">
            <Lightbulb className="w-5 h-5 text-amber-500" />
            <h2 className="text-lg font-semibold text-gray-700">Example Queries</h2>
          </div>
          
          <div className="grid grid-cols-1 gap-3">
            {examplePrompts.map((example, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(example)}
                className="text-left p-4 bg-white border-2 border-gray-200 rounded-xl hover:border-blue-400 hover:bg-blue-50 transition-all duration-300 group"
                disabled={loading}
              >
                <p className="text-gray-700 group-hover:text-blue-700 transition-colors">
                  "{example}"
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* Capabilities Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-2xl border border-gray-200">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4">
              <TrendingUp className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Comprehensive Analysis</h3>
            <p className="text-gray-600 text-sm">
              Clinical trials, market data, patents, safety profiles, and regulatory pathways analyzed in seconds
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-gray-200">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mb-4">
              <Sparkles className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Multi-Agent Intelligence</h3>
            <p className="text-gray-600 text-sm">
              10+ specialized AI agents work together: MoA, PPI networks, disease similarity, and hypothesis generation
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-gray-200">
            <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center mb-4">
              <Shield className="w-6 h-6 text-emerald-600" />
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">Real Data Sources</h3>
            <p className="text-gray-600 text-sm">
              Integrated with ClinicalTrials.gov, Europe PMC, USPTO, FDA FAERS, and IQVIA/EXIM APIs
            </p>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="mt-12 p-6 bg-amber-50 border border-amber-200 rounded-xl">
          <p className="text-sm text-amber-900">
            <strong>Research Tool:</strong> This platform provides AI-powered drug intelligence for research purposes. 
            All analyses are evidence-based but require expert validation. Not intended for clinical or regulatory decision-making.
          </p>
        </div>
      </div>
    </div>
  );
}

export default StrategicDashboard;

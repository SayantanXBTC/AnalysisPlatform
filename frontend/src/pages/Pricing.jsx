import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, Zap, Crown, ArrowRight } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import Navbar from '../components/Navbar';
import api from '../api';

function Pricing({ setAuth }) {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpgrade = async () => {
    setLoading(true);
    try {
      const response = await api.post('/create-checkout-session', {
        price_id: 'price_1234567890', // Replace with your Stripe Price ID
        success_url: `${window.location.origin}/dashboard?success=true`,
        cancel_url: `${window.location.origin}/pricing?canceled=true`
      });

      if (response.data.url) {
        window.location.href = response.data.url;
      }
    } catch (error) {
      toast.error('Failed to start checkout. Please try again.');
      setLoading(false);
    }
  };

  const tiers = [
    {
      name: 'FREE',
      price: '$0',
      period: 'forever',
      description: 'Perfect for trying out the platform',
      features: [
        '5 analyses per month',
        'Real-time API data',
        'All 6 AI agents',
        'Executive summaries',
        'View results online',
        'Basic support'
      ],
      limitations: [
        'No PDF downloads',
        'No RAG features',
        'Limited analyses'
      ],
      cta: 'Current Plan',
      icon: Zap,
      color: 'blue',
      current: true
    },
    {
      name: 'PRO',
      price: '$29',
      period: 'per month',
      description: 'For professionals who need unlimited access',
      features: [
        'Unlimited analyses',
        'Real-time API data',
        'All 6 AI agents',
        'Executive summaries',
        'PDF report generation',
        'RAG-powered insights',
        'Priority support',
        'Advanced analytics',
        'Export to multiple formats'
      ],
      limitations: [],
      cta: 'Upgrade to PRO',
      icon: Crown,
      color: 'purple',
      popular: true
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Toaster position="top-right" />
      <Navbar setAuth={setAuth} />

      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="text-center mb-12 animate-fadeIn">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600">
            Unlock the full power of pharmaceutical intelligence
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {tiers.map((tier, index) => {
            const Icon = tier.icon;
            return (
              <div
                key={index}
                className={`relative bg-white rounded-2xl shadow-xl p-8 ${
                  tier.popular ? 'ring-4 ring-purple-500 transform scale-105' : ''
                } animate-slideUp`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-1 rounded-full text-sm font-bold">
                      MOST POPULAR
                    </span>
                  </div>
                )}

                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-800">{tier.name}</h3>
                    <p className="text-gray-600 text-sm mt-1">{tier.description}</p>
                  </div>
                  <div className={`w-12 h-12 bg-gradient-to-r ${
                    tier.color === 'blue' ? 'from-blue-500 to-blue-600' : 'from-purple-500 to-pink-600'
                  } rounded-xl flex items-center justify-center`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>

                <div className="mb-6">
                  <div className="flex items-baseline">
                    <span className="text-5xl font-bold text-gray-800">{tier.price}</span>
                    <span className="text-gray-600 ml-2">/ {tier.period}</span>
                  </div>
                </div>

                <ul className="space-y-3 mb-8">
                  {tier.features.map((feature, i) => (
                    <li key={i} className="flex items-start">
                      <Check className="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                {tier.limitations.length > 0 && (
                  <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm font-semibold text-gray-700 mb-2">Limitations:</p>
                    <ul className="space-y-1">
                      {tier.limitations.map((limitation, i) => (
                        <li key={i} className="text-sm text-gray-600">• {limitation}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <button
                  onClick={tier.current ? null : handleUpgrade}
                  disabled={tier.current || loading}
                  className={`w-full py-3 rounded-lg font-bold text-lg transition-all duration-300 flex items-center justify-center space-x-2 ${
                    tier.current
                      ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                      : 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700 shadow-lg hover:shadow-xl transform hover:scale-105'
                  }`}
                >
                  <span>{loading ? 'Processing...' : tier.cta}</span>
                  {!tier.current && <ArrowRight className="w-5 h-5" />}
                </button>
              </div>
            );
          })}
        </div>

        <div className="mt-16 text-center">
          <p className="text-gray-600 mb-4">All plans include:</p>
          <div className="flex flex-wrap justify-center gap-4">
            {['Real-time API data', 'All 6 AI agents', 'Secure & private', 'Regular updates'].map((item, i) => (
              <div key={i} className="bg-white px-4 py-2 rounded-full shadow-md">
                <span className="text-sm font-medium text-gray-700">{item}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Pricing;

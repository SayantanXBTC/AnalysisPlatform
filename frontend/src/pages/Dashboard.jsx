import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, TrendingUp, Shield, FileText, Users, Zap, ChevronDown, ArrowRight, Beaker, Globe, X, CheckCircle, Database, BarChart3, Clock } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import { useSubscription } from '../App';
import Navbar from '../components/Navbar';
import api from '../api';

function Dashboard({ setAuth }) {
  const [drugName, setDrugName] = useState('');
  const [indication, setIndication] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedCardId, setSelectedCardId] = useState(null);
  const [typedText, setTypedText] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [selectedFeature, setSelectedFeature] = useState(null);
  const navigate = useNavigate();
  const { subscription, refreshSubscription } = useSubscription();

  const fullText = "Your AI-Powered Research Companion";

  // Typing animation effect
  useEffect(() => {
    let index = 0;
    const timer = setInterval(() => {
      if (index <= fullText.length) {
        setTypedText(fullText.slice(0, index));
        index++;
      } else {
        clearInterval(timer);
      }
    }, 50);
    return () => clearInterval(timer);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (subscription && subscription.analyses_this_month >= subscription.analyses_limit) {
      toast.error(
        <div>
          <p className="font-bold">Monthly limit reached!</p>
          <p className="text-sm">Upgrade to PRO for unlimited analyses.</p>
        </div>,
        { duration: 5000 }
      );
      setTimeout(() => navigate('/pricing'), 1500);
      return;
    }

    setLoading(true);
    const toastId = toast.loading('Running multi-agent analysis...', {
      style: { borderRadius: '12px' }
    });
    
    try {
      const response = await api.post('/run-analysis', {
        drug_name: drugName,
        indication: indication
      });
      
      toast.success('Analysis complete!', { 
        id: toastId,
        icon: '✨',
        style: { borderRadius: '12px' }
      });
      await refreshSubscription();
      navigate('/analysis', { state: { analysisData: response.data } });
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Analysis failed. Please try again.';
      
      if (error.response?.status === 403) {
        toast.error(
          <div>
            <p className="font-bold">Limit reached!</p>
            <p className="text-sm">{errorMsg}</p>
          </div>,
          { id: toastId, duration: 5000 }
        );
        setTimeout(() => navigate('/pricing'), 1500);
      } else {
        toast.error(errorMsg, { id: toastId });
      }
      setLoading(false);
    }
  };

  const featureDocumentation = {
    clinical: {
      overview: "The Clinical Analysis agent leverages ClinicalTrials.gov and other global registries to provide comprehensive insights into clinical evidence for any drug-indication pair.",
      dataSources: ["ClinicalTrials.gov API", "WHO ICTRP", "EudraCT Registry"],
      keyMetrics: ["Trial Phase Distribution", "Enrollment Status", "Geographic Coverage", "Sponsor Types", "Study Design Quality"],
      useCases: [
        "Evaluate clinical evidence maturity for repurposing opportunities",
        "Identify gaps in clinical development programs",
        "Benchmark against competitor trial strategies",
        "Assess feasibility of new indication development"
      ],
      outputFormat: "Rich narrative with phase analysis, sponsor segmentation, trial status breakdown, and repurposing feasibility score with supporting data tables and citations."
    },
    market: {
      overview: "The Market Intelligence agent analyzes competitive landscapes, market saturation, pricing dynamics, and commercial opportunities using FDA NDC data and market databases.",
      dataSources: ["OpenFDA NDC Database", "Market Research APIs", "Pricing Databases"],
      keyMetrics: ["Competitive Density", "Market Share Estimates", "Route/Formulation Gaps", "Generic Competition", "Market Entry Barriers"],
      useCases: [
        "Identify whitespace opportunities in crowded markets",
        "Assess commercial viability of new formulations",
        "Evaluate competitive positioning strategies",
        "Estimate market entry timing and barriers"
      ],
      outputFormat: "Detailed market landscape with competitor analysis, formulation gap identification, revenue projections, and strategic recommendations with confidence scores."
    },
    patent: {
      overview: "The Patent Portfolio agent examines IP landscapes using USPTO PatentsView to identify patent clusters, expiry timelines, freedom-to-operate windows, and innovation trends.",
      dataSources: ["USPTO PatentsView API", "EPO Patent Database", "WIPO Global Database"],
      keyMetrics: ["Active Patents", "Expiry Timeline", "Patent Families", "Assignee Concentration", "Repurposing Claims"],
      useCases: [
        "Identify freedom-to-operate windows for repurposing",
        "Assess IP protection strength and duration",
        "Map innovation clusters and white spaces",
        "Evaluate patent landscape complexity"
      ],
      outputFormat: "Comprehensive IP analysis with patent lifecycle mapping, assignee landscape, novelty signals, and FTO assessment with valuation estimates."
    },
    regulatory: {
      overview: "The Regulatory Path agent maps approval pathways, regulatory requirements, and fast-track opportunities across global jurisdictions to streamline development planning.",
      dataSources: ["FDA Approval Database", "EMA Registry", "PMDA Database", "Regulatory Intelligence Platforms"],
      keyMetrics: ["Approval Timeline Estimates", "Pathway Complexity", "Fast-Track Eligibility", "Regional Requirements", "Precedent Analysis"],
      useCases: [
        "Plan optimal regulatory strategy across regions",
        "Identify fast-track and breakthrough designations",
        "Assess regulatory risk and timeline",
        "Benchmark against similar approval pathways"
      ],
      outputFormat: "Strategic regulatory roadmap with jurisdiction-specific requirements, timeline estimates, fast-track opportunities, and risk mitigation strategies."
    },
    safety: {
      overview: "The Safety Profile agent analyzes pharmacovigilance data from FDA FAERS to identify adverse event patterns, risk signals, and benefit-risk profiles for informed decision-making.",
      dataSources: ["FDA FAERS Database", "EudraVigilance", "WHO VigiBase", "Published Safety Literature"],
      keyMetrics: ["ADR Frequency", "Seriousness Classification", "Age/Gender Patterns", "Outcome Analysis", "Signal Strength"],
      useCases: [
        "Assess safety feasibility for new indications",
        "Identify high-risk patient populations",
        "Evaluate benefit-risk balance",
        "Monitor post-market safety signals"
      ],
      outputFormat: "Comprehensive safety assessment with ADR clustering, severity scoring, population risk analysis, and benefit-risk interpretation with confidence ratings."
    },
    internal: {
      overview: "The Internal Ops agent uses RAG (Retrieval-Augmented Generation) to search your private document repository, extracting relevant insights from SOPs, reports, and confidential data.",
      dataSources: ["Internal Document Repository", "Vector Database", "Proprietary Research Files", "Confidential Reports"],
      keyMetrics: ["Document Relevance Score", "Context Extraction Quality", "Citation Accuracy", "Knowledge Coverage"],
      useCases: [
        "Query internal research findings and SOPs",
        "Extract insights from confidential reports",
        "Align external analysis with internal knowledge",
        "Verify consistency with organizational standards"
      ],
      outputFormat: "Semantic search results with relevant document excerpts, context summaries, citation links, and alignment assessment with external findings."
    }
  };

  const features = [
    { 
      id: 'clinical',
      icon: Users, 
      label: "Clinical Analysis", 
      color: "blue", 
      desc: "Comprehensive trial data",
      fullDesc: "This engine scans global trial registries, mapping evidence maturity, population characteristics, study design signals, and repurposing pathways. It uncovers insights that previously took weeks of manual review.",
      bullets: [
        "Phase distribution analysis",
        "Sponsor segmentation mapping",
        "Repurposing relevance scoring",
        "Feasibility assessment"
      ]
    },
    { 
      id: 'market',
      icon: TrendingUp, 
      label: "Market Intelligence", 
      color: "green", 
      desc: "Competitive landscape",
      fullDesc: "This module reveals commercial landscapes instantly, highlighting saturation zones, whitespace opportunities, and formulation-based differentiation strategies.",
      bullets: [
        "Competitive density analysis",
        "Route/formulation gap identification",
        "Market entry barrier assessment",
        "Growth signal detection"
      ]
    },
    { 
      id: 'patent',
      icon: Shield, 
      label: "Patent Portfolio", 
      color: "purple", 
      desc: "IP protection analysis",
      fullDesc: "Our IP engine evaluates patent activity, expiry timelines, and innovation clusters to uncover repurposing windows and freedom-to-operate insights.",
      bullets: [
        "Expiring protection analysis",
        "Novelty signal detection",
        "Assignee landscape mapping",
        "Repurposing-specific claims"
      ]
    },
    { 
      id: 'regulatory',
      icon: FileText, 
      label: "Regulatory Path", 
      color: "indigo", 
      desc: "Approval timeline",
      fullDesc: "Navigate global approval routes effortlessly. This module clarifies requirements, fast-track opportunities, and regulatory risks across jurisdictions.",
      bullets: [
        "Region approval mapping",
        "Pathway complexity scoring",
        "Fast-track signal identification",
        "Compliance consideration analysis"
      ]
    },
    { 
      id: 'safety',
      icon: Sparkles, 
      label: "Safety Profile", 
      color: "orange", 
      desc: "Risk assessment",
      fullDesc: "Using global pharmacovigilance data, this engine highlights risk patterns, population susceptibilities, and benefit-risk feasibility assessments.",
      bullets: [
        "ADR cluster identification",
        "Seriousness scoring",
        "High-risk group detection",
        "Benefit-risk profiling"
      ]
    },
    { 
      id: 'internal',
      icon: Zap, 
      label: "Internal Ops", 
      color: "pink", 
      desc: "Resource planning",
      fullDesc: "Your private RAG engine: analyze internal documents, confidential reports, SOPs, and unpublished insights instantly with semantic search capabilities.",
      bullets: [
        "Semantic document search",
        "Context extraction",
        "Internal alignment verification",
        "Knowledge base integration"
      ]
    }
  ];

  const colorClasses = {
    blue: { bg: "from-blue-500 to-blue-600", hover: "hover:from-blue-600 hover:to-blue-700", border: "border-blue-200", glow: "hover:shadow-blue-500/50" },
    green: { bg: "from-green-500 to-green-600", hover: "hover:from-green-600 hover:to-green-700", border: "border-green-200", glow: "hover:shadow-green-500/50" },
    purple: { bg: "from-purple-500 to-purple-600", hover: "hover:from-purple-600 hover:to-purple-700", border: "border-purple-200", glow: "hover:shadow-purple-500/50" },
    indigo: { bg: "from-indigo-500 to-indigo-600", hover: "hover:from-indigo-600 hover:to-indigo-700", border: "border-indigo-200", glow: "hover:shadow-indigo-500/50" },
    orange: { bg: "from-orange-500 to-orange-600", hover: "hover:from-orange-600 hover:to-orange-700", border: "border-orange-200", glow: "hover:shadow-orange-500/50" },
    pink: { bg: "from-pink-500 to-pink-600", hover: "hover:from-pink-600 hover:to-pink-700", border: "border-pink-200", glow: "hover:shadow-pink-500/50" }
  };

  const toggleCard = (cardId) => {
    setSelectedCardId(selectedCardId === cardId ? null : cardId);
  };

  return (
    <div className="min-h-screen particles-bg bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Toaster position="top-right" />
      <Navbar setAuth={setAuth} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section with Parallax */}
        <div className="text-center mb-16 animate-fadeIn relative">
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-400 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float"></div>
            <div className="absolute top-0 right-1/4 w-96 h-96 bg-purple-400 rounded-full mix-blend-multiply filter blur-3xl opacity-10 animate-float" style={{ animationDelay: '2s' }}></div>
          </div>
          
          <h1 className="text-6xl sm:text-7xl font-bold gradient-text mb-6 animate-slideDown pb-2">
            Drug Analysis Platform
          </h1>
          <p className="text-2xl text-gray-600 mb-4 animate-slideUp min-h-[2rem]">
            {typedText}<span className="animate-pulse">|</span>
          </p>
          <p className="text-lg text-gray-500 animate-slideUp" style={{ animationDelay: '200ms' }}>
            Powered by 6 specialized AI agents for comprehensive pharmaceutical intelligence
          </p>
        </div>

        {/* Analysis Form */}
        <div className="premium-card p-8 sm:p-10 mb-16 animate-scaleIn hover-lift">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-gray-700 font-bold mb-3 text-lg flex items-center space-x-2">
                  <Beaker className="w-5 h-5 text-blue-600" />
                  <span>Drug Name</span>
                </label>
                <input
                  type="text"
                  value={drugName}
                  onChange={(e) => setDrugName(e.target.value)}
                  placeholder="e.g., Pembrolizumab, Aspirin"
                  className="w-full px-5 py-4 bg-white border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all duration-300 text-lg hover:border-gray-300 shadow-sm"
                  required
                />
              </div>
              
              <div>
                <label className="block text-gray-700 font-bold mb-3 text-lg flex items-center space-x-2">
                  <Globe className="w-5 h-5 text-purple-600" />
                  <span>Indication</span>
                </label>
                <input
                  type="text"
                  value={indication}
                  onChange={(e) => setIndication(e.target.value)}
                  placeholder="e.g., Lung cancer, Migraine"
                  className="w-full px-5 py-4 bg-white border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-4 focus:ring-purple-500/20 focus:border-purple-500 transition-all duration-300 text-lg hover:border-gray-300 shadow-sm"
                  required
                />
              </div>
            </div>
            
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white py-5 rounded-xl hover:from-blue-700 hover:via-purple-700 hover:to-pink-700 transition-all duration-500 font-bold text-xl shadow-2xl hover:shadow-blue-500/50 transform hover:scale-[1.02] press-effect disabled:opacity-50 disabled:cursor-not-allowed relative overflow-hidden group"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
              <span className="relative z-10 flex items-center justify-center space-x-3">
                <Sparkles className="w-6 h-6" />
                <span>{loading ? 'Running Analysis...' : 'Start Comprehensive Analysis'}</span>
              </span>
            </button>
          </form>
        </div>

        {/* Feature Cards with Expandable Panels */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center gradient-text mb-10 animate-fadeIn">
            AI-Powered Intelligence Modules
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              const isExpanded = selectedCardId === feature.id;
              const colors = colorClasses[feature.color];
              
              return (
                <div key={index} className="animate-slideUp" style={{ animationDelay: `${index * 100}ms` }}>
                  <div
                    onClick={() => toggleCard(feature.id)}
                    className={`premium-card p-6 cursor-pointer transition-all duration-500 transform hover:scale-105 press-effect tilt-card ${colors.glow} ${
                      isExpanded ? 'ring-4 ring-offset-2 ring-' + feature.color + '-500/50' : ''
                    }`}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className={`w-14 h-14 bg-gradient-to-r ${colors.bg} rounded-2xl flex items-center justify-center shadow-lg`}>
                        <Icon className="w-7 h-7 text-white" />
                      </div>
                      <div className={`transition-transform duration-300 ${isExpanded ? 'rotate-180' : ''}`}>
                        <ChevronDown className="w-6 h-6 text-gray-400" />
                      </div>
                    </div>
                    <h3 className="text-xl font-bold text-gray-800 mb-2">{feature.label}</h3>
                    <p className="text-gray-600 text-sm mb-3">{feature.desc}</p>
                    
                    {/* Expandable Content */}
                    <div className={`overflow-hidden transition-all duration-500 ${
                      isExpanded ? 'max-h-[600px] opacity-100' : 'max-h-0 opacity-0'
                    }`}>
                      <div className={`mt-4 pt-4 border-t-2 ${colors.border} space-y-4 animate-slideDown`}>
                        <p className="text-gray-700 text-sm leading-relaxed">
                          {feature.fullDesc}
                        </p>
                        
                        <div className="space-y-2">
                          <p className="font-semibold text-gray-800 text-sm">Key Capabilities:</p>
                          <ul className="space-y-2">
                            {feature.bullets.map((bullet, idx) => (
                              <li key={idx} className="flex items-start space-x-2 text-sm text-gray-600">
                                <div className={`w-1.5 h-1.5 rounded-full bg-gradient-to-r ${colors.bg} mt-1.5 flex-shrink-0`}></div>
                                <span>{bullet}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                        
                        <button 
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedFeature(feature);
                            setShowModal(true);
                          }}
                          className={`flex items-center space-x-2 text-sm font-semibold bg-gradient-to-r ${colors.bg} text-white px-4 py-2 rounded-lg ${colors.hover} transition-all duration-300 shadow-md hover:shadow-lg group`}
                        >
                          <span>Learn More</span>
                          <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Stats Section */}
        <div className="premium-card p-12 animate-fadeIn hover-lift">
          <h2 className="text-4xl font-bold mb-12 text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Why Choose Our Platform?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center transform hover:scale-105 transition-all duration-300 bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-8 border-2 border-blue-200 hover:border-blue-400 hover:shadow-xl">
              <div className="text-6xl font-bold mb-4 text-blue-600">
                6
              </div>
              <div className="text-gray-700 text-lg font-semibold">
                Specialized AI Agents
              </div>
            </div>
            <div className="text-center transform hover:scale-105 transition-all duration-300 bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-8 border-2 border-purple-200 hover:border-purple-400 hover:shadow-xl">
              <div className="text-6xl font-bold mb-4 text-purple-600">
                &lt;2min
              </div>
              <div className="text-gray-700 text-lg font-semibold">
                Analysis Time
              </div>
            </div>
            <div className="text-center transform hover:scale-105 transition-all duration-300 bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-2xl p-8 border-2 border-emerald-200 hover:border-emerald-400 hover:shadow-xl">
              <div className="text-6xl font-bold mb-4 text-emerald-600">
                100%
              </div>
              <div className="text-gray-700 text-lg font-semibold">
                Comprehensive Coverage
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Documentation Modal */}
      {showModal && selectedFeature && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fadeIn" onClick={() => setShowModal(false)}>
          <div className="bg-white rounded-3xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto animate-scaleIn" onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className={`bg-gradient-to-r ${colorClasses[selectedFeature.color].bg} p-8 text-white relative`}>
              <button 
                onClick={() => setShowModal(false)}
                className="absolute top-6 right-6 p-2 hover:bg-white/20 rounded-full transition-all duration-300"
              >
                <X className="w-6 h-6" />
              </button>
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center">
                  {selectedFeature.icon && <selectedFeature.icon className="w-8 h-8" />}
                </div>
                <div>
                  <h2 className="text-4xl font-bold">{selectedFeature.label}</h2>
                  <p className="text-white/90 text-lg mt-1">{selectedFeature.desc}</p>
                </div>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-8 space-y-8">
              {/* Overview */}
              <div>
                <h3 className="text-2xl font-bold text-gray-800 mb-3 flex items-center space-x-2">
                  <FileText className="w-6 h-6 text-blue-600" />
                  <span>Overview</span>
                </h3>
                <p className="text-gray-700 leading-relaxed text-lg">
                  {featureDocumentation[selectedFeature.id]?.overview}
                </p>
              </div>

              {/* Data Sources */}
              <div>
                <h3 className="text-2xl font-bold text-gray-800 mb-3 flex items-center space-x-2">
                  <Database className="w-6 h-6 text-purple-600" />
                  <span>Data Sources</span>
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {featureDocumentation[selectedFeature.id]?.dataSources.map((source, idx) => (
                    <div key={idx} className="flex items-center space-x-2 bg-purple-50 p-3 rounded-lg border border-purple-200">
                      <CheckCircle className="w-5 h-5 text-purple-600 flex-shrink-0" />
                      <span className="text-gray-700 font-medium">{source}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Key Metrics */}
              <div>
                <h3 className="text-2xl font-bold text-gray-800 mb-3 flex items-center space-x-2">
                  <BarChart3 className="w-6 h-6 text-green-600" />
                  <span>Key Metrics Analyzed</span>
                </h3>
                <div className="flex flex-wrap gap-2">
                  {featureDocumentation[selectedFeature.id]?.keyMetrics.map((metric, idx) => (
                    <span key={idx} className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-semibold border border-green-300">
                      {metric}
                    </span>
                  ))}
                </div>
              </div>

              {/* Use Cases */}
              <div>
                <h3 className="text-2xl font-bold text-gray-800 mb-3 flex items-center space-x-2">
                  <Clock className="w-6 h-6 text-orange-600" />
                  <span>Common Use Cases</span>
                </h3>
                <ul className="space-y-3">
                  {featureDocumentation[selectedFeature.id]?.useCases.map((useCase, idx) => (
                    <li key={idx} className="flex items-start space-x-3 bg-orange-50 p-4 rounded-lg border border-orange-200">
                      <div className="w-6 h-6 bg-orange-500 text-white rounded-full flex items-center justify-center flex-shrink-0 font-bold text-sm mt-0.5">
                        {idx + 1}
                      </div>
                      <span className="text-gray-700 leading-relaxed">{useCase}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Output Format */}
              <div>
                <h3 className="text-2xl font-bold text-gray-800 mb-3 flex items-center space-x-2">
                  <Sparkles className="w-6 h-6 text-pink-600" />
                  <span>Output Format</span>
                </h3>
                <div className="bg-gradient-to-br from-pink-50 to-purple-50 p-6 rounded-xl border-2 border-pink-200">
                  <p className="text-gray-700 leading-relaxed">
                    {featureDocumentation[selectedFeature.id]?.outputFormat}
                  </p>
                </div>
              </div>

              {/* Close Button */}
              <div className="flex justify-end pt-4">
                <button
                  onClick={() => setShowModal(false)}
                  className={`bg-gradient-to-r ${colorClasses[selectedFeature.color].bg} text-white px-8 py-3 rounded-xl font-semibold ${colorClasses[selectedFeature.color].hover} transition-all duration-300 shadow-lg hover:shadow-xl`}
                >
                  Got it!
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;

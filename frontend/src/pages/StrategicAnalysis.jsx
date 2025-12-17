import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Download, ArrowLeft, AlertCircle, CheckCircle, TrendingUp, Shield, Beaker } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import Navbar from '../components/Navbar';
import api from '../api';

function StrategicAnalysis({ setAuth }) {
  const location = useLocation();
  const navigate = useNavigate();
  const analysisData = location.state?.analysisData;
  
  const [expandedSection, setExpandedSection] = useState(null);

  if (!analysisData) {
    navigate('/dashboard');
    return null;
  }

  const results = analysisData.results;

  // Handle clarification needed
  if (results.status === 'clarification_needed') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
        <Toaster position="top-right" />
        <Navbar setAuth={setAuth} />
        
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="premium-card p-8">
            <div className="flex items-start space-x-4 mb-6">
              <AlertCircle className="w-8 h-8 text-amber-500 flex-shrink-0 mt-1" />
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-4">Need More Information</h2>
                <p className="text-gray-700 whitespace-pre-line">{results.message}</p>
              </div>
            </div>
            
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-semibold"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Refine Query</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Classification badge colors
  const getClassificationColor = (classification) => {
    if (classification === 'High' || classification === 'Strong' || classification === 'Mechanistically Supported') {
      return 'bg-emerald-100 text-emerald-800 border-emerald-300';
    } else if (classification === 'Moderate' || classification === 'Promising' || classification === 'Hypothesis-Level' || classification === 'Medium') {
      return 'bg-blue-100 text-blue-800 border-blue-300';
    } else {
      return 'bg-amber-100 text-amber-800 border-amber-300';
    }
  };

  const getRecommendationColor = (classification) => {
    if (classification === 'Worth Pursuing') {
      return 'bg-emerald-50 border-emerald-300 text-emerald-900';
    } else if (classification === 'Requires Validation') {
      return 'bg-blue-50 border-blue-300 text-blue-900';
    } else {
      return 'bg-amber-50 border-amber-300 text-amber-900';
    }
  };

  // Render intelligence data in a professional format
  const renderIntelligenceData = (data) => {
    if (!data || typeof data !== 'object') {
      return <p className="text-gray-600">No data available</p>;
    }

    return (
      <div className="space-y-4">
        {Object.entries(data).map(([key, value]) => {
          // Skip internal/meta fields
          if (key.startsWith('_') || key === 'timestamp') return null;

          return (
            <div key={key} className="border-l-4 border-blue-200 pl-4 py-2">
              <div className="font-semibold text-gray-900 mb-1">
                {key.replace(/_/g, ' ').split(' ').map(word => 
                  word.charAt(0).toUpperCase() + word.slice(1)
                ).join(' ')}
              </div>
              <div className="text-gray-700">
                {typeof value === 'object' && value !== null ? (
                  Array.isArray(value) ? (
                    <ul className="list-disc list-inside space-y-1 ml-2">
                      {value.slice(0, 10).map((item, idx) => (
                        <li key={idx} className="text-sm">
                          {typeof item === 'object' ? JSON.stringify(item) : String(item)}
                        </li>
                      ))}
                      {value.length > 10 && (
                        <li className="text-sm text-gray-500 italic">
                          ... and {value.length - 10} more items
                        </li>
                      )}
                    </ul>
                  ) : (
                    <div className="space-y-2 ml-2">
                      {Object.entries(value).slice(0, 8).map(([subKey, subValue]) => (
                        <div key={subKey} className="text-sm">
                          <span className="font-medium text-gray-600">{subKey}:</span>{' '}
                          <span className="text-gray-800">
                            {typeof subValue === 'object' ? JSON.stringify(subValue).slice(0, 100) : String(subValue)}
                          </span>
                        </div>
                      ))}
                      {Object.keys(value).length > 8 && (
                        <div className="text-sm text-gray-500 italic">
                          ... and {Object.keys(value).length - 8} more fields
                        </div>
                      )}
                    </div>
                  )
                ) : (
                  <span className="text-gray-800">{String(value)}</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      <Toaster position="top-right" />
      <Navbar setAuth={setAuth} />
      
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>New Query</span>
          </button>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Strategic Intelligence Report</h1>
          <p className="text-gray-600">{results.original_prompt}</p>
        </div>

        {/* Strategic Classifications */}
        <div className="premium-card p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Strategic Assessment</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div>
              <p className="text-sm text-gray-600 mb-2">Evidence Strength</p>
              <span className={`inline-block px-4 py-2 rounded-lg border-2 font-semibold ${getClassificationColor(results.evidence_strength)}`}>
                {results.evidence_strength}
              </span>
            </div>
            
            <div>
              <p className="text-sm text-gray-600 mb-2">Scientific Plausibility</p>
              <span className={`inline-block px-4 py-2 rounded-lg border-2 font-semibold ${getClassificationColor(results.scientific_plausibility)}`}>
                {results.scientific_plausibility}
              </span>
            </div>
            
            <div>
              <p className="text-sm text-gray-600 mb-2">Innovation Attractiveness</p>
              <span className={`inline-block px-4 py-2 rounded-lg border-2 font-semibold ${getClassificationColor(results.innovation_attractiveness)}`}>
                {results.innovation_attractiveness}
              </span>
            </div>
            
            <div>
              <p className="text-sm text-gray-600 mb-2">Commercial Feasibility</p>
              <span className={`inline-block px-4 py-2 rounded-lg border-2 font-semibold ${getClassificationColor(results.commercial_feasibility)}`}>
                {results.commercial_feasibility}
              </span>
            </div>
          </div>

          {/* Executive Summary */}
          <div className="prose max-w-none">
            <div className="whitespace-pre-line text-gray-700 leading-relaxed">
              {results.executive_summary}
            </div>
          </div>
        </div>

        {/* Strategic Recommendation */}
        {results.strategic_recommendation && (
          <div className={`premium-card p-8 mb-8 border-2 ${getRecommendationColor(results.strategic_recommendation.classification)}`}>
            <div className="flex items-start space-x-4">
              <CheckCircle className="w-8 h-8 flex-shrink-0 mt-1" />
              <div className="flex-1">
                <h3 className="text-2xl font-bold mb-2">{results.strategic_recommendation.classification}</h3>
                <p className="text-lg mb-4">{results.strategic_recommendation.rationale}</p>
                <p className="text-sm font-semibold">Confidence Band: {results.strategic_recommendation.confidence_band}</p>
              </div>
            </div>
          </div>
        )}

        {/* Key Insights */}
        {results.key_insights && results.key_insights.length > 0 && (
          <div className="premium-card p-8 mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Key Insights</h3>
            <ul className="space-y-3">
              {results.key_insights.map((insight, idx) => (
                <li key={idx} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-600 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-gray-700">{insight}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Risks and Unknowns */}
        {results.risks_and_unknowns && results.risks_and_unknowns.length > 0 && (
          <div className="premium-card p-8 mb-8 bg-amber-50 border-2 border-amber-200">
            <div className="flex items-start space-x-3 mb-4">
              <AlertCircle className="w-6 h-6 text-amber-600 flex-shrink-0 mt-1" />
              <h3 className="text-xl font-bold text-amber-900">Risks & Knowledge Gaps</h3>
            </div>
            <ul className="space-y-3">
              {results.risks_and_unknowns.map((risk, idx) => (
                <li key={idx} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-amber-600 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-amber-900">{risk}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Suggested Next Steps */}
        {results.suggested_next_steps && results.suggested_next_steps.length > 0 && (
          <div className="premium-card p-8 mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Suggested Next Steps</h3>
            <ol className="space-y-3">
              {results.suggested_next_steps.map((step, idx) => (
                <li key={idx} className="flex items-start space-x-3">
                  <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    {idx + 1}
                  </span>
                  <span className="text-gray-700 pt-0.5">{step}</span>
                </li>
              ))}
            </ol>
          </div>
        )}

        {/* Detailed Intelligence (Collapsible) */}
        {results.detailed_intelligence && Object.keys(results.detailed_intelligence).length > 0 && (
          <div className="premium-card p-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Detailed Intelligence by Agent</h3>
            <p className="text-sm text-gray-600 mb-6">
              Expand any section to view detailed findings from each AI agent
            </p>
            
            <div className="space-y-3">
              {Object.entries(results.detailed_intelligence).map(([key, value]) => (
                <div key={key} className="border-2 border-gray-200 rounded-xl overflow-hidden hover:border-blue-300 transition-colors">
                  <button
                    onClick={() => setExpandedSection(expandedSection === key ? null : key)}
                    className="w-full px-6 py-4 bg-gradient-to-r from-gray-50 to-white hover:from-blue-50 hover:to-white transition-all text-left flex items-center justify-between group"
                  >
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                        expandedSection === key ? 'bg-blue-600' : 'bg-gray-200 group-hover:bg-blue-100'
                      } transition-colors`}>
                        <span className={`text-lg font-bold ${
                          expandedSection === key ? 'text-white' : 'text-gray-600 group-hover:text-blue-600'
                        }`}>
                          {key.charAt(0).toUpperCase()}
                        </span>
                      </div>
                      <span className="font-semibold text-gray-900 text-lg">
                        {key.replace(/_/g, ' ').split(' ').map(word => 
                          word.charAt(0).toUpperCase() + word.slice(1)
                        ).join(' ')}
                      </span>
                    </div>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      expandedSection === key ? 'bg-blue-600' : 'bg-gray-200 group-hover:bg-blue-100'
                    } transition-colors`}>
                      <span className={`text-xl font-bold ${
                        expandedSection === key ? 'text-white' : 'text-gray-600 group-hover:text-blue-600'
                      }`}>
                        {expandedSection === key ? '−' : '+'}
                      </span>
                    </div>
                  </button>
                  
                  {expandedSection === key && (
                    <div className="p-6 bg-white border-t-2 border-gray-100">
                      {renderIntelligenceData(value)}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex justify-center space-x-4 mt-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-3 bg-white border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-all duration-300 font-semibold"
          >
            New Query
          </button>
          
          <button
            onClick={async () => {
              try {
                const toastId = toast.loading('Generating PDF report...');
                const response = await api.post('/generate-strategic-pdf', {
                  prompt: results.original_prompt,
                  results: results
                });
                toast.success('PDF ready! Click to download.', { 
                  id: toastId,
                  duration: 5000
                });
                
                // Download the PDF using a download link (doesn't auto-open)
                const filename = response.data.filename;
                const link = document.createElement('a');
                link.href = `http://localhost:8000/download-report/${filename}`;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
              } catch (error) {
                toast.error('Failed to generate PDF');
              }
            }}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all duration-300 font-semibold flex items-center space-x-2"
          >
            <Download className="w-5 h-5" />
            <span>Generate PDF Report</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default StrategicAnalysis;

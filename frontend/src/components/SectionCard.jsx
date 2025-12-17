import { useState } from 'react';
import { ChevronDown, ChevronUp, Edit2, Save, X, Award, TrendingUp } from 'lucide-react';

function SectionCard({ title, content, onUpdate }) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(
    typeof content === 'object' ? JSON.stringify(content, null, 2) : content
  );

  const handleSave = () => {
    try {
      const parsed = JSON.parse(editedContent);
      onUpdate(parsed);
      setIsEditing(false);
    } catch (error) {
      onUpdate(editedContent);
      setIsEditing(false);
    }
  };

  const getGradientColor = (title) => {
    const colors = {
      'Clinical': 'from-blue-500 to-blue-600',
      'Literature': 'from-cyan-500 to-cyan-600',
      'Market': 'from-green-500 to-green-600',
      'Patent': 'from-purple-500 to-purple-600',
      'Regulatory': 'from-indigo-500 to-indigo-600',
      'Safety': 'from-orange-500 to-orange-600',
      'Internal': 'from-pink-500 to-pink-600'
    };
    return colors[title] || 'from-gray-500 to-gray-600';
  };

  const renderContent = () => {
    if (typeof content !== 'object') {
      return <p className="text-gray-600 leading-relaxed">{content}</p>;
    }

    return (
      <div className="space-y-6">
        {/* Summary */}
        {content.summary && (
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-l-4 border-blue-500 p-5 rounded-xl shadow-sm animate-slideInLeft">
            <p className="text-sm font-medium text-blue-900 leading-relaxed">{content.summary}</p>
          </div>
        )}

        {/* Confidence Score */}
        {(content.confidence_score || content.confidence) && (
          <div className="flex items-center space-x-3 bg-gradient-to-r from-yellow-50 to-orange-50 p-4 rounded-xl animate-slideInRight">
            <Award className="w-6 h-6 text-yellow-600 animate-pulse" />
            <span className="text-sm font-semibold text-gray-700">Confidence Score:</span>
            <div className="flex-1 bg-gray-200 rounded-full h-3 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-yellow-500 to-orange-500 h-full rounded-full transition-all duration-1000 ease-out"
                style={{ width: `${(content.confidence_score || content.confidence / 100) * 100}%` }}
              ></div>
            </div>
            <span className="text-sm font-bold text-orange-600">
              {((content.confidence_score || content.confidence / 100) * 100).toFixed(1)}%
            </span>
          </div>
        )}

        {/* Text/Narrative */}
        {(content.text || content.narrative) && (
          <div className="prose prose-sm max-w-none">
            <div className="bg-white p-6 rounded-xl border-2 border-gray-100 shadow-sm">
              <p className="text-gray-700 text-sm leading-relaxed whitespace-pre-line">
                {content.text || content.narrative}
              </p>
            </div>
          </div>
        )}

        {/* Key Findings */}
        {content.key_findings && content.key_findings.length > 0 && (
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-5 rounded-xl border-l-4 border-green-500 animate-slideInLeft">
            <h4 className="text-sm font-bold text-green-900 mb-3 flex items-center space-x-2">
              <TrendingUp className="w-5 h-5" />
              <span>Key Findings</span>
            </h4>
            <ul className="space-y-2">
              {content.key_findings.map((finding, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-sm text-green-900">
                  <div className="w-2 h-2 rounded-full bg-green-500 mt-1.5 flex-shrink-0 animate-pulse"></div>
                  <span>{finding}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Tables */}
        {Object.entries(content).map(([key, value]) => {
          if (Array.isArray(value) && value.length > 0 && typeof value[0] === 'object') {
            return (
              <div key={key} className="overflow-hidden rounded-xl border-2 border-gray-100 shadow-sm animate-fadeIn">
                <h4 className="text-sm font-bold text-gray-700 mb-0 capitalize bg-gradient-to-r from-gray-50 to-gray-100 px-4 py-3 border-b-2 border-gray-200">
                  {key.replace(/_/g, ' ')}
                </h4>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200 text-sm">
                    <thead className="bg-gradient-to-r from-blue-50 to-purple-50">
                      <tr>
                        {Object.keys(value[0]).map((header) => (
                          <th
                            key={header}
                            className="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                          >
                            {header}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-100">
                      {value.slice(0, 10).map((row, idx) => (
                        <tr key={idx} className="hover:bg-blue-50 transition-colors duration-200">
                          {Object.values(row).map((cell, cellIdx) => (
                            <td key={cellIdx} className="px-4 py-3 text-sm text-gray-700">
                              {String(cell)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            );
          }
          return null;
        })}

        {/* Citations */}
        {content.citations && content.citations.length > 0 && (
          <div className="mt-6 pt-6 border-t-2 border-gray-200 animate-fadeIn">
            <h4 className="text-sm font-bold text-gray-700 mb-3">References & Citations</h4>
            <ul className="space-y-2">
              {content.citations.slice(0, 5).map((citation, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-xs text-gray-600 bg-gray-50 p-3 rounded-lg hover:bg-gray-100 transition-colors">
                  <span className="font-bold text-blue-600">[{idx + 1}]</span>
                  <span>{citation}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const gradientColor = getGradientColor(title);

  return (
    <div className="premium-card overflow-hidden animate-slideUp hover-lift tilt-card group">
      {/* Header */}
      <div className={`bg-gradient-to-r ${gradientColor} px-6 py-5 relative overflow-hidden`}>
        <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/10 to-white/0 transform -skew-x-12 translate-x-full group-hover:translate-x-[-200%] transition-transform duration-1000"></div>
        <div className="flex justify-between items-center relative z-10">
          <h3 className="text-2xl font-bold text-white drop-shadow-lg">{title}</h3>
          <div className="flex items-center space-x-2">
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="text-white hover:text-blue-100 transition-all duration-300 transform hover:scale-110 press-effect p-2 rounded-lg hover:bg-white/20"
                title="Edit"
              >
                <Edit2 className="w-5 h-5" />
              </button>
            )}
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-white hover:text-blue-100 transition-all duration-300 transform hover:scale-110 press-effect p-2 rounded-lg hover:bg-white/20"
            >
              {isExpanded ? <ChevronUp className="w-6 h-6" /> : <ChevronDown className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>
      
      {/* Content */}
      <div className={`transition-all duration-500 ease-in-out ${
        isExpanded ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'
      }`}>
        <div className="p-6">
          {isEditing ? (
            <div className="space-y-4 animate-fadeIn">
              <textarea
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
                className="w-full h-96 px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 font-mono text-xs transition-all duration-300 shadow-sm"
              />
              <div className="flex space-x-3">
                <button
                  onClick={handleSave}
                  className="flex items-center space-x-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white px-5 py-3 rounded-xl hover:from-green-700 hover:to-emerald-700 transition-all duration-300 shadow-lg hover:shadow-green-500/50 transform hover:scale-105 press-effect font-medium"
                >
                  <Save className="w-5 h-5" />
                  <span>Save Changes</span>
                </button>
                <button
                  onClick={() => setIsEditing(false)}
                  className="flex items-center space-x-2 bg-gradient-to-r from-gray-600 to-gray-700 text-white px-5 py-3 rounded-xl hover:from-gray-700 hover:to-gray-800 transition-all duration-300 shadow-lg transform hover:scale-105 press-effect font-medium"
                >
                  <X className="w-5 h-5" />
                  <span>Cancel</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="animate-fadeIn">
              {renderContent()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SectionCard;

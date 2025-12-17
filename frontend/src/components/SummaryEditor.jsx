import { FileText, Sparkles } from 'lucide-react';

function SummaryEditor({ sections }) {
  const generateSummary = () => {
    const summaryParts = [];
    
    Object.entries(sections).forEach(([sectionName, content]) => {
      if (typeof content === 'object' && content.summary) {
        summaryParts.push(`**${sectionName}:** ${content.summary}`);
      }
    });
    
    return summaryParts.join('\n\n');
  };

  const summary = generateSummary();

  if (!summary) return null;

  return (
    <div className="premium-card p-8 animate-fadeIn hover-lift">
      <div className="flex items-center space-x-3 mb-6">
        <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
          <FileText className="w-6 h-6 text-white" />
        </div>
        <div>
          <h3 className="text-2xl font-bold gradient-text">Section Summaries</h3>
          <p className="text-sm text-gray-500">Comprehensive overview of all analyses</p>
        </div>
      </div>
      
      <div className="relative">
        <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-2xl blur opacity-20"></div>
        <div className="relative bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 p-8 rounded-2xl border-l-4 border-blue-500 shadow-lg">
          <div className="flex items-start space-x-3 mb-4">
            <Sparkles className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1 animate-pulse" />
            <p className="text-gray-700 whitespace-pre-line leading-relaxed text-sm font-medium">
              {summary}
            </p>
          </div>
        </div>
      </div>
      
      {/* Decorative elements */}
      <div className="mt-6 flex items-center justify-center space-x-2 text-xs text-gray-400">
        <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></div>
        <span>AI-Generated Summary</span>
        <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse" style={{ animationDelay: '0.5s' }}></div>
      </div>
    </div>
  );
}

export default SummaryEditor;

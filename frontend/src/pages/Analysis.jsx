import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Download, FileText, Lock, Sparkles, TrendingUp, Award } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import { useSubscription } from '../App';
import Navbar from '../components/Navbar';
import SectionCard from '../components/SectionCard';
import api from '../api';

function Analysis({ setAuth }) {
  const location = useLocation();
  const navigate = useNavigate();
  const analysisData = location.state?.analysisData;
  const { subscription } = useSubscription();
  
  const [sections, setSections] = useState(analysisData?.sections || {});
  const [loading, setLoading] = useState(false);
  const [animatedMetrics, setAnimatedMetrics] = useState({
    trials: 0,
    patents: 0,
    signals: 0
  });

  if (!analysisData) {
    navigate('/dashboard');
    return null;
  }

  // Animated counter effect
  useEffect(() => {
    const targetTrials = sections.highlights?.total_trials || 0;
    const targetPatents = sections.highlights?.total_patents || 0;
    const targetSignals = sections.highlights?.safety_signals || 0;

    const duration = 2000;
    const steps = 60;
    const interval = duration / steps;

    let step = 0;
    const timer = setInterval(() => {
      step++;
      const progress = step / steps;
      
      setAnimatedMetrics({
        trials: Math.floor(targetTrials * progress),
        patents: Math.floor(targetPatents * progress),
        signals: Math.floor(targetSignals * progress)
      });

      if (step >= steps) {
        clearInterval(timer);
        setAnimatedMetrics({
          trials: targetTrials,
          patents: targetPatents,
          signals: targetSignals
        });
      }
    }, interval);

    return () => clearInterval(timer);
  }, [sections.highlights]);

  const handleSectionUpdate = (sectionName, newContent) => {
    setSections(prev => ({
      ...prev,
      [sectionName]: newContent
    }));
    toast.success(`${sectionName} section updated`, {
      icon: '✨',
      style: { borderRadius: '12px' }
    });
  };

  const handleGenerateReport = async () => {
    if (!subscription?.can_generate_pdf) {
      toast.error(
        <div>
          <p className="font-bold">PDF generation is a PRO feature</p>
          <p className="text-sm">Upgrade to PRO to download reports.</p>
        </div>,
        { duration: 5000 }
      );
      setTimeout(() => navigate('/pricing'), 1500);
      return;
    }

    setLoading(true);
    const toastId = toast.loading('Generating comprehensive PDF report...', {
      style: { borderRadius: '12px' }
    });
    
    try {
      await api.post('/finalize-report', {
        report_id: analysisData.report_id,
        sections: sections
      });
      
      const response = await api.get(`/download-report/${analysisData.report_id}`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `analysis_report_${analysisData.report_id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('Report generated and downloaded successfully!', { 
        id: toastId,
        icon: '🎉',
        style: { borderRadius: '12px' }
      });
    } catch (error) {
      toast.error('Failed to generate report. Please try again.', { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  const sectionOrder = ["Clinical", "Literature", "Market", "Patent", "Regulatory", "Safety", "Internal"];
  const displaySections = sectionOrder.filter(name => sections[name]);

  return (
    <div className="min-h-screen particles-bg bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50 page-transition">
      <Toaster position="top-right" />
      <Navbar setAuth={setAuth} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="premium-card p-8 mb-8 animate-slideDown hover-lift">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div className="flex-1">
              <h1 className="text-4xl font-bold gradient-text mb-3">Analysis Results</h1>
              <div className="space-y-1 text-gray-600">
                <p className="flex items-center space-x-2">
                  <span className="font-semibold text-blue-600">Drug:</span>
                  <span className="text-lg">{analysisData.drug_name}</span>
                </p>
                <p className="flex items-center space-x-2">
                  <span className="font-semibold text-purple-600">Indication:</span>
                  <span className="text-lg">{analysisData.indication}</span>
                </p>
              </div>
            </div>
            <div className="mt-4 md:mt-0">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-3xl flex items-center justify-center shadow-2xl animate-float">
                <FileText className="w-10 h-10 text-white" />
              </div>
            </div>
          </div>
        </div>
        
        {/* Animated Metrics */}
        {sections.highlights && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="premium-card p-6 text-center hover-lift animate-slideUp">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                <TrendingUp className="w-8 h-8 text-white" />
              </div>
              <div className="text-4xl font-bold gradient-text mb-2">{animatedMetrics.trials}</div>
              <div className="text-gray-600 font-medium">Clinical Trials</div>
            </div>
            
            <div className="premium-card p-6 text-center hover-lift animate-slideUp" style={{ animationDelay: '100ms' }}>
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                <Award className="w-8 h-8 text-white" />
              </div>
              <div className="text-4xl font-bold gradient-text mb-2">{animatedMetrics.patents}</div>
              <div className="text-gray-600 font-medium">Patents Identified</div>
            </div>
            
            <div className="premium-card p-6 text-center hover-lift animate-slideUp" style={{ animationDelay: '200ms' }}>
              <div className="w-16 h-16 bg-gradient-to-r from-orange-500 to-orange-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
              <div className="text-4xl font-bold gradient-text mb-2">{animatedMetrics.signals}</div>
              <div className="text-gray-600 font-medium">Safety Signals</div>
            </div>
          </div>
        )}
        
        {/* Executive Summary */}
        {sections.executive_summary && (
          <div className="premium-card p-8 mb-8 animate-fadeIn hover-lift">
            <h2 className="text-3xl font-bold gradient-text mb-6 flex items-center space-x-3">
              <Sparkles className="w-8 h-8 text-blue-600" />
              <span>Executive Summary</span>
            </h2>
            <div className="prose prose-lg max-w-none">
              <div className="bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 p-6 rounded-2xl border-l-4 border-blue-500">
                <p className="text-gray-700 leading-relaxed whitespace-pre-line font-mono text-sm">
                  {sections.executive_summary}
                </p>
              </div>
            </div>
          </div>
        )}
        
        {/* Section Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {displaySections.map((sectionName, index) => (
            <div 
              key={sectionName}
              className="animate-slideUp"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <SectionCard
                title={sectionName}
                content={sections[sectionName]}
                onUpdate={(newContent) => handleSectionUpdate(sectionName, newContent)}
              />
            </div>
          ))}
        </div>
        
        {/* Download Button */}
        <div className={`premium-card p-8 animate-fadeIn hover-lift ${
          subscription?.can_generate_pdf 
            ? 'bg-gradient-to-r from-green-500 to-emerald-600' 
            : 'bg-gradient-to-r from-gray-400 to-gray-500'
        }`}>
          {!subscription?.can_generate_pdf && (
            <div className="mb-6 flex items-center justify-center space-x-3 text-white">
              <Lock className="w-6 h-6" />
              <span className="font-bold text-lg">PDF generation is a PRO feature</span>
            </div>
          )}
          <button
            onClick={handleGenerateReport}
            disabled={loading || !subscription?.can_generate_pdf}
            className={`w-full py-5 rounded-xl transition-all duration-300 font-bold text-xl flex items-center justify-center space-x-4 relative overflow-hidden group ${
              subscription?.can_generate_pdf
                ? 'bg-white text-green-700 hover:bg-gray-50 shadow-2xl hover:shadow-green-500/50 transform hover:scale-[1.02] press-effect'
                : 'bg-white text-gray-500 cursor-not-allowed'
            } disabled:bg-gray-200 disabled:text-gray-500`}
          >
            {subscription?.can_generate_pdf && (
              <div className="absolute inset-0 bg-gradient-to-r from-green-500/0 via-green-500/20 to-green-500/0 transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
            )}
            {subscription?.can_generate_pdf ? (
              <>
                <Download className="w-7 h-7 relative z-10" />
                <span className="relative z-10">{loading ? 'Generating Report...' : 'Generate & Download PDF Report'}</span>
              </>
            ) : (
              <>
                <Lock className="w-7 h-7" />
                <span>Upgrade to PRO to Download PDF</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Analysis;

import { TrendingUp, Users, Shield, DollarSign, FileCheck, AlertTriangle, Target, Award } from 'lucide-react';

function HighlightsPanel({ highlights }) {
  if (!highlights) return null;

  const metrics = [
    {
      icon: FileCheck,
      label: "Clinical Trials",
      value: highlights.total_trials || 0,
      color: "blue"
    },
    {
      icon: Users,
      label: "Patients Enrolled",
      value: highlights.total_patients || 0,
      color: "green"
    },
    {
      icon: Shield,
      label: "Patents",
      value: highlights.total_patents || 0,
      color: "purple"
    },
    {
      icon: AlertTriangle,
      label: "Safety Signals",
      value: highlights.safety_signals || 0,
      color: "orange"
    },
    {
      icon: DollarSign,
      label: "Peak Sales",
      value: highlights.market_size || "N/A",
      color: "emerald"
    },
    {
      icon: Target,
      label: "Approval Probability",
      value: highlights.approval_probability || "N/A",
      color: "indigo"
    },
    {
      icon: TrendingUp,
      label: "Investment",
      value: highlights.investment_required || "N/A",
      color: "pink"
    },
    {
      icon: Award,
      label: "Avg Confidence",
      value: `${(highlights.avg_confidence * 100).toFixed(0)}%`,
      color: "cyan"
    }
  ];

  const colorClasses = {
    blue: "bg-blue-50 text-blue-600 border-blue-200",
    green: "bg-green-50 text-green-600 border-green-200",
    purple: "bg-purple-50 text-purple-600 border-purple-200",
    orange: "bg-orange-50 text-orange-600 border-orange-200",
    emerald: "bg-emerald-50 text-emerald-600 border-emerald-200",
    indigo: "bg-indigo-50 text-indigo-600 border-indigo-200",
    pink: "bg-pink-50 text-pink-600 border-pink-200",
    cyan: "bg-cyan-50 text-cyan-600 border-cyan-200"
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6 animate-fadeIn">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Key Highlights</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <div
              key={index}
              className={`${colorClasses[metric.color]} border-2 rounded-lg p-4 transition-all duration-300 hover:scale-105 hover:shadow-md animate-slideUp`}
              style={{ animationDelay: `${index * 50}ms` }}
            >
              <Icon className="w-6 h-6 mb-2" />
              <div className="text-2xl font-bold mb-1">{metric.value}</div>
              <div className="text-sm font-medium opacity-80">{metric.label}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default HighlightsPanel;


import React, { useState, useEffect } from 'react';
import ReportIngestForm from './components/ReportIngestForm';
import EmergencyMap from './components/EmergencyMap';

export default function App() {
  const [incidents, setIncidents] = useState([]);
  const [resources, setResources] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');

  // 1. Fetch live incidents and resources from backend database
  const fetchAllData = async () => {
    try {
      const [incRes, resRes] = await Promise.all([
        fetch('http://127.0.0.1:8000/incidents'),
        fetch('http://127.0.0.1:8000/resources/').catch(() => ({ ok: false })),
      ]);

      if (incRes.ok) {
        const incData = await incRes.json();
        setIncidents(Array.isArray(incData) ? incData : []);
      }

      if (resRes.ok && resRes.json) {
        const resData = await resRes.json();
        setResources(Array.isArray(resData) ? resData : []);
      }
    } catch (err) {
      console.error('Failed to fetch initial state:', err);
    }
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  const handleReportSubmitted = () => {
    fetchAllData();
  };

  const handleRecalculate = async () => {
    setLoading(true);
    setStatusMsg('');

    try {
      const res = await fetch('http://127.0.0.1:8000/allocations/recalculate', {
        method: 'POST',
      });
      const data = await res.json();

      if (data.status === 'success') {
        setAssignments(data.assignments || []);
        setStatusMsg('Optimization completed successfully!');
      } else {
        setStatusMsg('Recalculation failed');
      }
    } catch (err) {
      console.error('Recalculation error:', err);
      setStatusMsg('Recalculation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-4 font-sans">
      {/* Top Header Bar */}
      <div className="flex justify-between items-center mb-4 pb-3 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-red-500 flex items-center gap-2">
            <span>🚨</span> FloodMesh AI
          </h1>
          <p className="text-xs text-slate-400">Emergency Resource Allocation Command Center</p>
        </div>

        <div className="flex items-center gap-3">
          {statusMsg && (
            <span className="text-xs bg-slate-800 text-blue-400 px-3 py-1.5 rounded border border-slate-700">
              {statusMsg}
            </span>
          )}
          <button
            onClick={handleRecalculate}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-700 text-white text-xs font-semibold px-4 py-2 rounded shadow transition-all flex items-center gap-2"
          >
            {loading ? (
              <>
                <span className="animate-spin h-3 w-3 border-2 border-white border-t-transparent rounded-full"></span>
                <span>Solving MILP...</span>
              </>
            ) : (
              '🔄 Recalculate OR-Tools Optimization'
            )}
          </button>
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Left Panel: SOS Form & Prioritized Queue */}
        <div className="lg:col-span-4 space-y-4">
          <ReportIngestForm onReportSubmitted={handleReportSubmitted} />

          <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
            <h3 className="font-bold text-sm text-slate-200 mb-3 flex justify-between items-center">
              <span>📈 Prioritized Incidents ({incidents.length})</span>
              <button
                onClick={fetchAllData}
                className="text-[10px] text-slate-400 hover:text-slate-200 underline"
              >
                Refresh Queue
              </button>
            </h3>

            {/* Step 3: Updated Incident Card Rendering */}
            <div className="space-y-2 max-h-[320px] overflow-y-auto pr-1">
              {incidents.length === 0 ? (
                <p className="text-xs text-slate-500 italic py-2">No pending incidents reported.</p>
              ) : (
                incidents.map((inc, i) => {
                  const incId = inc.id || inc.incident_id || `INC-${i + 1}`;
                  const incText = inc.raw_report_text || inc.description || 'Emergency SOS Report';
                  const score = inc.priority_score || 40;

                  return (
                    <div
                      key={incId}
                      className="bg-slate-900 p-3 rounded-lg border border-slate-800 text-xs space-y-1.5 shadow-sm"
                    >
                      <div className="flex justify-between items-center font-bold">
                        <span className="text-red-400">#{incId}</span>
                        <span className="bg-red-950/90 text-red-300 px-2 py-0.5 rounded text-[10px] border border-red-800">
                          Score: {score}/100
                        </span>
                      </div>
                      <p className="text-slate-200 text-xs font-normal line-clamp-2">
                        {incText}
                      </p>
                      <div className="flex justify-between text-[10px] text-slate-400 pt-1 border-t border-slate-800/60">
                        <span>📍 {Number(inc.latitude).toFixed(4)}, {Number(inc.longitude).toFixed(4)}</span>
                        <span className="text-amber-400 font-medium capitalize">{inc.status || 'pending'}</span>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>

        {/* Right Panel: Interactive GPS Map & Active Allocations */}
        <div className="lg:col-span-8 space-y-4">
          <EmergencyMap
            incidents={incidents}
            resources={resources}
            assignments={assignments}
          />

          <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl">
            <h3 className="font-bold text-sm text-slate-200 mb-2">
              🛡️ OR-Tools Recommended Resource Allocations ({assignments.length})
            </h3>
            {assignments.length === 0 ? (
              <p className="text-xs text-slate-500 italic py-1">
                No active assignments. Click "Recalculate OR-Tools Optimization" to solve allocations.
              </p>
            ) : (
              <div className="space-y-2">
                {assignments.map((asgn, idx) => (
                  <div
                    key={idx}
                    className="bg-slate-800 p-3 rounded-lg border border-slate-700 text-xs flex flex-wrap justify-between items-center gap-2"
                  >
                    <div>
                      <div className="font-semibold text-slate-200">
                        <span className="text-green-400">{asgn.resource_name}</span> ➔{' '}
                        <span className="text-red-400">Incident #{asgn.incident_id}</span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-0.5">{asgn.match_reason}</p>
                    </div>
                    <span className="bg-blue-900/60 text-blue-300 px-2.5 py-1 rounded text-[10px] font-semibold border border-blue-700">
                      ETA: {asgn.eta_minutes} mins ({asgn.distance_km} km)
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

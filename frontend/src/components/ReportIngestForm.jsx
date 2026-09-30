import React, { useState, useEffect } from 'react';

export default function ReportIngestForm({ onReportSubmitted }) {
  const [reportText, setReportText] = useState('');
  const [liveLocation, setLiveLocation] = useState(null);
  const [isLocating, setIsLocating] = useState(true);
  const [locationError, setLocationError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  const acquireLiveLocation = () => {
    setIsLocating(true);
    setLocationError(null);

    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLiveLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
          setIsLocating(false);
        },
        (error) => {
          console.warn('Geolocation access failed:', error.message);
          setLocationError(error.message);
          setIsLocating(false);
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      );
    } else {
      setLocationError('Geolocation is not supported by your browser.');
      setIsLocating(false);
    }
  };

  useEffect(() => {
    acquireLiveLocation();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!reportText.trim()) return;

    setLoading(true);
    setStatusMessage('');

    const payload = {
      report_text: reportText,
      raw_report_text: reportText,
      source: 'web_live_gps',
      latitude: liveLocation ? liveLocation.lat : null,
      longitude: liveLocation ? liveLocation.lng : null,
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/incidents/ingest-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setReportText('');
      setStatusMessage('✅ Incident reported successfully!');
      if (onReportSubmitted) {
        onReportSubmitted(data);
      }
    } catch (err) {
      console.error('Failed to submit report:', err);
      setStatusMessage(`❌ Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 p-4 rounded-xl shadow-md border border-slate-800 w-full text-slate-100">
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-bold text-sm text-slate-100 flex items-center gap-1.5">
          <span>🚨</span> Report Live Emergency SOS
        </h3>
        <button
          type="button"
          onClick={acquireLiveLocation}
          className="text-[10px] bg-slate-800 hover:bg-slate-700 text-slate-300 px-2 py-1 rounded border border-slate-700 transition-all"
        >
          🔄 Refresh GPS
        </button>
      </div>

      {/* GPS Status Indicator */}
      <div className="text-[11px] mb-3 p-2 bg-slate-950 rounded-md border border-slate-800">
        <div className="flex items-center gap-1.5 text-slate-300">
          <span className="font-semibold">Live GPS Position:</span>
          {isLocating ? (
            <span className="text-amber-400 font-medium animate-pulse">Acquiring coordinates...</span>
          ) : liveLocation ? (
            <span className="text-emerald-400 font-semibold">
              📍 {liveLocation.lat.toFixed(5)}, {liveLocation.lng.toFixed(5)}
            </span>
          ) : (
            <span className="text-rose-400 font-medium">GPS Unavailable</span>
          )}
        </div>
        {locationError && (
          <p className="text-[10px] text-rose-400 mt-1">Notice: {locationError}</p>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        {/* Explicit text-slate-900 and bg-white prevents white-on-white text */}
        <textarea
          value={reportText}
          onChange={(e) => setReportText(e.target.value)}
          placeholder="Describe emergency (e.g., '10 people trapped on roof, need boat urgently')"
          className="w-full h-24 p-2.5 text-xs text-slate-900 bg-white font-medium border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all resize-none placeholder:text-slate-400"
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-rose-600 hover:bg-rose-700 disabled:bg-rose-900 text-white font-semibold text-xs py-2.5 rounded-lg transition-all shadow flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <span className="animate-spin h-3.5 w-3.5 border-2 border-white border-t-transparent rounded-full"></span>
              <span>Processing with Gemini...</span>
            </>
          ) : (
            'Submit SOS with Live GPS'
          )}
        </button>
      </form>

      {statusMessage && (
        <p className="text-[11px] font-medium text-center mt-2.5 p-1.5 rounded bg-slate-950 border border-slate-800 text-slate-300">
          {statusMessage}
        </p>
      )}
    </div>
  );
}

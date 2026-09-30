import React, { useState, useEffect } from 'react';
import { 
  MapContainer, 
  TileLayer, 
  Marker, 
  Popup, 
  Polyline, 
  Tooltip,
  Circle, 
  useMap 
} from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet default icon asset paths
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Clean DivIcon pin generator without background box clipping
const createCustomIcon = (bgColor, emoji) => L.divIcon({
  className: 'custom-pin-reset',
  html: `
    <div style="
      background-color: ${bgColor};
      width: 38px;
      height: 38px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
      border: 3px solid white;
      font-size: 19px;
      cursor: pointer;
    ">
      ${emoji}
    </div>
  `,
  iconSize: [38, 38],
  iconAnchor: [19, 38],
  popupAnchor: [0, -38],
});

const icons = {
  userLocation: createCustomIcon('#2563eb', '📍'),
  incidentHigh: createCustomIcon('#dc2626', '🚨'),
  incidentMed: createCustomIcon('#f59e0b', '⚠'),
  incidentLow: createCustomIcon('#3b82f6', 'ℹ️'),
  boat: createCustomIcon('#0284c7', '🚤'),
  police: createCustomIcon('#1e40af', '🚓'),
  ambulance: createCustomIcon('#16a34a', '🚑'),
  camp: createCustomIcon('#9333ea', '⛺'),
};

function LiveLocationController({ onLocationFound, onLocationError }) {
  const map = useMap();

  useEffect(() => {
    map.locate({ setView: true, maxZoom: 13, enableHighAccuracy: true });

    const handleLocationFound = (e) => {
      onLocationFound(e.latlng, e.accuracy);
      map.flyTo(e.latlng, 13, { animate: true, duration: 1.5 });
    };

    const handleLocationError = (e) => {
      onLocationError(e.message);
    };

    map.on('locationfound', handleLocationFound);
    map.on('locationerror', handleLocationError);

    return () => {
      map.off('locationfound', handleLocationFound);
      map.off('locationerror', handleLocationError);
    };
  }, [map]);

  return null;
}

export default function EmergencyMap({ incidents = [], resources = [], assignments = [] }) {
  const [userLocation, setUserLocation] = useState(null);
  const [accuracyRadius, setAccuracyRadius] = useState(null);
  const [statusMessage, setStatusMessage] = useState('Acquiring live GPS location...');

  const INDIA_CENTER = [20.5937, 78.9629];

  // Helper to choose proper icon by name or type
  const getResourceIcon = (name = '', type = '') => {
    const n = name.toLowerCase();
    const t = type.toLowerCase();
    if (n.includes('police') || t.includes('police')) return icons.police;
    if (n.includes('ambulance') || t.includes('ambulance') || n.includes('medical')) return icons.ambulance;
    if (n.includes('camp') || t.includes('camp')) return icons.camp;
    return icons.boat;
  };

  // Build a consolidated list of resources from props + active assignments
  const consolidatedResources = () => {
    const mapByResId = new Map();

    // 1. Add items from resources prop
    resources.forEach((r) => {
      const id = r.resource_id || r.id;
      const lat = floatOrNull(r.latitude);
      const lng = floatOrNull(r.longitude);
      if (id && lat !== null && lng !== null) {
        mapByResId.set(id, {
          id,
          name: r.name || `Unit #${id}`,
          type: r.resource_type || r.type || 'rescue_boat',
          lat,
          lng,
          capacity: r.capacity || 10,
          status: r.status || 'available',
        });
      }
    });

    // 2. Merge items from assignments (guarantees assigned units render even if resources prop is empty)
    assignments.forEach((a) => {
      const id = a.resource_id;
      const lat = floatOrNull(a.resource_lat);
      const lng = floatOrNull(a.resource_lng);
      if (id && lat !== null && lng !== null && !mapByResId.has(id)) {
        mapByResId.set(id, {
          id,
          name: a.resource_name || `Unit #${id}`,
          type: a.resource_type || 'rescue_boat',
          lat,
          lng,
          capacity: 10,
          status: 'assigned',
        });
      }
    });

    return Array.from(mapByResId.values());
  };

  const activeUnits = consolidatedResources();

  return (
    <div className="relative w-full h-[550px] rounded-xl overflow-hidden border border-slate-800 shadow-xl">
      
      {/* Live GPS Status Badge */}
      <div className="absolute top-4 left-4 z-[1000] bg-slate-900/90 text-slate-100 text-xs px-3.5 py-2 rounded-lg shadow-md backdrop-blur-sm flex items-center gap-2 border border-slate-700">
        <span className="relative flex h-2.5 w-2.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-blue-500"></span>
        </span>
        {statusMessage}
      </div>

      {/* Map Legend */}
      <div className="absolute bottom-6 right-4 z-[1000] bg-slate-900/95 text-slate-100 text-xs p-3 rounded-lg border border-slate-700 shadow-2xl backdrop-blur-md space-y-1.5 min-w-[180px]">
        <div className="font-bold text-slate-200 border-b border-slate-700 pb-1 mb-1.5">
          🗺️ Map Legend
        </div>
        <div className="flex items-center gap-2 text-slate-300">
          <span className="text-base">🚨</span> <span>Disaster Incident</span>
        </div>
        <div className="flex items-center gap-2 text-slate-300">
          <span className="text-base">🚤</span> <span>NDRF Rescue Boat</span>
        </div>
        <div className="flex items-center gap-2 text-slate-300">
          <span className="text-base">🚓</span> <span>Assam Police Rescue</span>
        </div>
        <div className="flex items-center gap-2 text-slate-300 pt-1 border-t border-slate-800">
          <span className="w-5 h-0.5 bg-blue-500 border-b-2 border-dashed border-blue-400 inline-block"></span>
          <span className="font-medium text-blue-400">Dispatch Route</span>
        </div>
      </div>

      <MapContainer
        center={INDIA_CENTER}
        zoom={5}
        scrollWheelZoom={true}
        className="w-full h-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <LiveLocationController
          onLocationFound={(latlng, accuracy) => {
            setUserLocation(latlng);
            setAccuracyRadius(accuracy);
            setStatusMessage(`Live GPS Connected (±${Math.round(accuracy)}m accuracy)`);
          }}
          onLocationError={(msg) => {
            setStatusMessage(`GPS Notice: ${msg}. Enable location in browser.`);
          }}
        />

        {/* User GPS Location */}
        {userLocation && (
          <>
            <Marker position={userLocation} icon={icons.userLocation}>
              <Popup>
                <div className="p-1">
                  <h4 className="font-bold text-sm text-blue-600">Your Live GPS Position</h4>
                  <p className="text-xs text-slate-700 mt-1">
                    Lat: {userLocation.lat.toFixed(5)}<br />
                    Lng: {userLocation.lng.toFixed(5)}
                  </p>
                </div>
              </Popup>
            </Marker>
            <Circle
              center={userLocation}
              radius={accuracyRadius || 100}
              pathOptions={{ color: '#2563eb', fillColor: '#3b82f6', fillOpacity: 0.15, weight: 1.5 }}
            />
          </>
        )}

        {/* Incidents Markers */}
        {incidents.map((inc, idx) => {
          const lat = floatOrNull(inc.latitude);
          const lng = floatOrNull(inc.longitude);
          if (lat === null || lng === null) return null;

          const pScore = Number(inc.priority_score || 50);
          const iconType =
            pScore >= 70
              ? icons.incidentHigh
              : pScore >= 40
              ? icons.incidentMed
              : icons.incidentLow;

          const incId = inc.id || inc.incident_id || `INC-${idx + 1}`;

          return (
            <Marker key={`inc-${incId}-${idx}`} position={[lat, lng]} icon={iconType}>
              <Popup>
                <div className="p-1 max-w-[200px]">
                  <span className="text-xs font-bold text-red-600">
                    INCIDENT #{incId}
                  </span>
                  <p className="text-xs text-slate-800 font-medium mt-1">
                    {inc.raw_report_text || inc.description}
                  </p>
                  <div className="mt-2 text-[11px] text-slate-600 border-t pt-1">
                    <p><strong>Priority Score:</strong> {pScore}/100</p>
                    <p><strong>Status:</strong> {inc.status || 'pending'}</p>
                  </div>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {/* Rescue Team Unit Markers (NDRF Boat Alpha, Assam Police Rescue 2, etc.) */}
        {activeUnits.map((res, idx) => {
          const resIcon = getResourceIcon(res.name, res.type);

          return (
            <Marker 
              key={`unit-${res.id}-${idx}`} 
              position={[res.lat, res.lng]} 
              icon={resIcon} 
              zIndexOffset={1000}
            >
              {/* Permanent badge label under the icon */}
              <Tooltip 
                permanent 
                direction="bottom" 
                offset={[0, 10]} 
                className="bg-emerald-950 text-emerald-300 border-emerald-700 text-[10px] font-bold py-0.5 px-1.5 rounded shadow-lg border"
              >
                {res.name}
              </Tooltip>
              <Popup>
                <div className="p-1">
                  <span className="text-xs font-bold text-green-700">{res.name}</span>
                  <p className="text-xs text-slate-600 mt-1">Type: {res.type}</p>
                  <p className="text-xs text-slate-600">Capacity: {res.capacity} persons</p>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {/* Dispatch Routes */}
        {assignments.map((asgn, idx) => {
          const incLat = floatOrNull(asgn.incident_lat);
          const incLng = floatOrNull(asgn.incident_lng);
          const resLat = floatOrNull(asgn.resource_lat);
          const resLng = floatOrNull(asgn.resource_lng);

          if (incLat === null || incLng === null || resLat === null || resLng === null) {
            return null;
          }

          return (
            <Polyline
              key={`route-${idx}`}
              positions={[
                [incLat, incLng],
                [resLat, resLng],
              ]}
              pathOptions={{ color: '#2563eb', weight: 3, dashArray: '6, 6' }}
            >
              <Tooltip sticky className="bg-slate-900 text-white border-blue-500 text-[11px] font-medium py-1 px-2 rounded shadow-lg border">
                <span className="text-green-400 font-bold">{asgn.resource_name}</span> ➔ <span className="text-red-400 font-bold">#{asgn.incident_id}</span> ({asgn.eta_minutes} mins, {asgn.distance_km} km)
              </Tooltip>
            </Polyline>
          );
        })}
      </MapContainer>
    </div>
  );
}

function floatOrNull(val) {
  if (val === undefined || val === null) return null;
  const num = parseFloat(val);
  return isNaN(num) ? null : num;
}

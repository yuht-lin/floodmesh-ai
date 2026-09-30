import React, { useState, useEffect } from 'react';
import { 
  MapContainer, 
  TileLayer, 
  Marker, 
  Popup, 
  Polyline, 
  Circle, 
  useMap 
} from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix default Leaflet icon assets
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom Marker Pin Generator
const createCustomIcon = (color, emoji) => L.divIcon({
  className: 'custom-map-pin',
  html: `
    <div style="
      background-color: ${color};
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 8px rgba(0,0,0,0.4);
      border: 3px solid white;
      font-size: 18px;
    ">
      ${emoji}
    </div>
  `,
  iconSize: [36, 36],
  iconAnchor: [18, 36],
  popupAnchor: [0, -36],
});

// Map Pin Icons
const icons = {
  userLocation: createCustomIcon('#2563eb', '📍'),
  incidentHigh: createCustomIcon('#dc2626', '🚨'),
  incidentMed: createCustomIcon('#f59e0b', '⚠️'),
  incidentLow: createCustomIcon('#3b82f6', 'ℹ️'),
  boat: createCustomIcon('#0284c7', '🚤'),
  ambulance: createCustomIcon('#16a34a', '🚑'),
  camp: createCustomIcon('#9333ea', '⛺'),
};

// Map controller to automatically center on user's live GPS coordinates
function LiveLocationController({ onLocationFound, onLocationError }) {
  const map = useMap();

  useEffect(() => {
    // Request live GPS location immediately on mount
    map.locate({ setView: true, maxZoom: 14, enableHighAccuracy: true });

    const handleLocationFound = (e) => {
      onLocationFound(e.latlng, e.accuracy);
      map.flyTo(e.latlng, 14, { animate: true, duration: 1.5 });
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

export default function FloodMeshMap({ incidents = [], resources = [], assignments = [] }) {
  const [userLocation, setUserLocation] = useState(null);
  const [accuracyRadius, setAccuracyRadius] = useState(null);
  const [statusMessage, setStatusMessage] = useState('Acquiring live GPS location...');

  // Fallback initial view centered on India if GPS permission is pending/denied
  const INDIA_CENTER = [20.5937, 78.9629];

  return (
    <div className="relative w-full h-[550px] rounded-xl overflow-hidden border border-gray-300 shadow-lg">
      
      {/* Live Status Bar */}
      <div className="absolute top-4 left-4 z-[1000] bg-gray-900/90 text-white text-xs px-3.5 py-2 rounded-md shadow-md backdrop-blur-sm flex items-center gap-2 border border-gray-700">
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
        </span>
        {statusMessage}
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

        {/* Live Geolocation Controller */}
        <LiveLocationController
          onLocationFound={(latlng, accuracy) => {
            setUserLocation(latlng);
            setAccuracyRadius(accuracy);
            setStatusMessage(`Live GPS Connected (±${Math.round(accuracy)}m accuracy)`);
          }}
          onLocationError={(msg) => {
            setStatusMessage(`GPS Warning: ${msg}. Click 'Allow Location' in browser.`);
          }}
        />

        {/* Live User Location Pin & Radius */}
        {userLocation && (
          <>
            <Marker position={userLocation} icon={icons.userLocation}>
              <Popup>
                <div className="p-1">
                  <h4 className="font-bold text-sm text-blue-600">Your Current Location</h4>
                  <p className="text-xs text-gray-600 mt-1">
                    Latitude: {userLocation.lat.toFixed(5)}<br />
                    Longitude: {userLocation.lng.toFixed(5)}
                  </p>
                  <p className="text-[10px] text-gray-400 mt-1">Accuracy: ±{Math.round(accuracyRadius)} meters</p>
                </div>
              </Popup>
            </Marker>
            <Circle
              center={userLocation}
              radius={accuracyRadius || 100}
              pathOptions={{ color: '#2563eb', fillColor: '#3b82f6', fillOpacity: 0.18, weight: 1.5 }}
            />
          </>
        )}

        {/* Incidents (Only rendered if passed in from backend) */}
        {incidents.map((inc) => {
          const iconType =
            inc.priority_score > 70
              ? icons.incidentHigh
              : inc.priority_score > 40
              ? icons.incidentMed
              : icons.incidentLow;

          return (
            <Marker key={`inc-${inc.id}`} position={[inc.latitude, inc.longitude]} icon={iconType}>
              <Popup>
                <div className="p-1">
                  <span className="text-xs font-bold text-red-600">INCIDENT #{inc.id}</span>
                  <p className="text-xs font-semibold mt-1">{inc.raw_report_text}</p>
                  <div className="mt-2 text-[11px] text-gray-600">
                    <p><strong>Priority Score:</strong> {inc.priority_score}/100</p>
                    <p><strong>Affected:</strong> {inc.people_affected || 'N/A'}</p>
                  </div>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {/* Active Resources */}
        {resources.map((res) => {
          const resIcon =
            res.type === 'rescue_boat'
              ? icons.boat
              : res.type === 'ambulance'
              ? icons.ambulance
              : icons.camp;

          return (
            <Marker key={`res-${res.id}`} position={[res.latitude, res.longitude]} icon={resIcon}>
              <Popup>
                <div className="p-1">
                  <span className="text-xs font-bold text-green-700">{res.name}</span>
                  <p className="text-xs text-gray-600 mt-1">Type: {res.type}</p>
                </div>
              </Popup>
            </Marker>
          );
        })}

        {/* Dynamic Assignment Polyline Routes */}
        {assignments.map((asgn, idx) => {
          if (!asgn.incident_lat || !asgn.resource_lat) return null;
          return (
            <Polyline
              key={`route-${idx}`}
              positions={[
                [asgn.incident_lat, asgn.incident_lng],
                [asgn.resource_lat, asgn.resource_lng],
              ]}
              pathOptions={{ color: '#2563eb', weight: 3, dashArray: '6, 6' }}
            />
          );
        })}
      </MapContainer>
    </div>
  );
}

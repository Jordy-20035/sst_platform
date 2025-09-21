import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix default marker icon for Vite + React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

// Google Maps-style user location icon
const userIcon = new L.Icon({
  iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

// Colored markers for incidents
const statusColors = {
  reported: "yellow",
  active: "red",
  resolved: "green",
};
const createColoredIcon = (color) =>
  new L.Icon({
    iconUrl: `https://maps.google.com/mapfiles/ms/icons/${color}-dot.png`,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
  });

// Component to handle map clicks
const AddIncidentMarker = ({ addIncident }) => {
  useMapEvents({
    click(e) {
      const title = prompt("Enter incident title:");
      if (!title) return;
      const description = prompt("Enter description (optional):");
      const newIncident = {
        id: Date.now(),
        title,
        description,
        latitude: e.latlng.lat,
        longitude: e.latlng.lng,
        status: "reported",
      };
      // POST to backend
      fetch("http://localhost:8000/api/v1/incidents", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newIncident),
      }).then(res => res.json())
        .then(data => addIncident(data))
        .catch(err => console.error(err));
    },
  });
  return null;
};

export default function IncidentMap() {
  const [incidents, setIncidents] = useState([]);
  const [userPos, setUserPos] = useState(null);

  // Fetch incidents from backend on mount
  useEffect(() => {
    fetch("http://localhost:8000/api/v1/incidents")
      .then(res => res.json())
      .then(setIncidents)
      .catch(err => console.error(err));
  }, []);

  // SSE for live updates
  useEffect(() => {
    const es = new EventSource("http://localhost:8000/api/v1/stream");
    es.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        if (parsed.type === "incident.created") {
          setIncidents(prev => [parsed.data, ...prev]);
        }
      } catch (err) {
        console.error("SSE parse error:", err);
      }
    };
    es.onerror = () => es.close();
    return () => es.close();
  }, []);

  // Get user location
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => setUserPos({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        (err) => console.warn("Geolocation error:", err)
      );
    }
  }, []);

  return (
    <div className="w-full h-[600px] rounded-lg shadow-lg overflow-hidden">
      <MapContainer
        center={[54.786, 32.049]}
        zoom={13}
        style={{ width: "100%", height: "100%" }}
        attributionControl={false}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
          attribution=""
        />

        <AddIncidentMarker addIncident={(inc) => setIncidents(prev => [inc, ...prev])} />

        {userPos && (
          <Marker position={[userPos.lat, userPos.lng]} icon={userIcon}>
            <Popup>Your location 📍</Popup>
          </Marker>
        )}

        {incidents.map((inc) => (
          <Marker
            key={inc.id}
            position={[inc.latitude, inc.longitude]}
            icon={createColoredIcon(statusColors[inc.status] || "blue")}
          >
            <Popup className="text-sm">
              <div className="font-bold">{inc.title}</div>
              <div className="text-gray-600">Status: {inc.status}</div>
              {inc.description && <div className="mt-1 text-gray-800">{inc.description}</div>}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}


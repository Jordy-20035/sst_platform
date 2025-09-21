import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

// Fix default marker icon issue in React-Leaflet
import L from "leaflet";
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

export default function IncidentMap() {
  const [incidents, setIncidents] = useState([]);

  // Fetch initial incidents
  useEffect(() => {
    fetch("http://localhost:8000/api/v1/incidents")
      .then((res) => res.json())
      .then(setIncidents)
      .catch(console.error);
  }, []);

  // Setup SSE listener
  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/api/v1/stream");
    eventSource.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      if (parsed.type === "incident.created") {
        setIncidents((prev) => [parsed.data, ...prev]);
      }
    };
    return () => eventSource.close();
  }, []);

  return (
    <div className="w-full h-[600px]">
      <MapContainer center={[54.786, 32.049]} zoom={13} className="w-full h-full">
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a>'
        />
        {incidents.map((inc) => (
          <Marker
            key={inc.id}
            position={[inc.latitude || 54.786, inc.longitude || 32.049]}
          >
            <Popup>
              <strong>{inc.title}</strong>
              <br />
              Status: {inc.status}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}

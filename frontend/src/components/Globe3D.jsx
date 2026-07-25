import { useRef, useEffect, useMemo, useState } from 'react';
import Globe from 'react-globe.gl';
import { feature } from 'topojson-client';
import { CATEGORIES } from '../lib/history';

const GLOBE_TEXTURE = 'https://unpkg.com/three-globe/example/img/earth-night.jpg';
const BUMP_TEXTURE = 'https://unpkg.com/three-globe/example/img/earth-topology.png';
const COUNTRIES_URL = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json';

export default function Globe3D({
  visibleEvents,
  arcs,
  empires,
  year,
  onSelect,
  focusEvent,
  autoRotate,
}) {
  const globeRef = useRef();
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    fetch(COUNTRIES_URL)
      .then((r) => r.json())
      .then((topo) => {
        const geo = feature(topo, topo.objects.countries);
        setCountries(geo.features);
      })
      .catch(() => setCountries([]));
  }, []);

  useEffect(() => {
    const g = globeRef.current;
    if (!g) return;
    g.controls().autoRotate = !!autoRotate;
    g.controls().autoRotateSpeed = 0.35;
    g.controls().enableZoom = true;
    g.controls().minDistance = 180;
    g.controls().maxDistance = 500;
    g.pointOfView({ lat: 20, lng: 0, altitude: 2.4 }, 0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    const g = globeRef.current;
    if (g) g.controls().autoRotate = !!autoRotate;
  }, [autoRotate]);

  useEffect(() => {
    if (!focusEvent || !globeRef.current) return;
    globeRef.current.pointOfView(
      { lat: focusEvent.lat, lng: focusEvent.lng, altitude: 1.6 },
      1400
    );
  }, [focusEvent]);

  // Active arcs at current year
  const activeArcs = useMemo(
    () => (arcs || []).filter((a) => year >= a.start_year && year <= a.end_year),
    [arcs, year]
  );

  // Active empires + fade opacity (0 → 1 near start, hold, 1 → 0 near end)
  const empirePolygons = useMemo(() => {
    if (!countries.length || !empires) return [];
    const activeCountryOpacity = new Map();
    for (const emp of empires) {
      if (year < emp.start_year - 50 || year > emp.end_year + 50) continue;
      const fadeIn = 100;
      const fadeOut = 100;
      let op = 0.55;
      if (year < emp.start_year) op = 0.55 * (1 - (emp.start_year - year) / fadeIn);
      else if (year > emp.end_year) op = 0.55 * (1 - (year - emp.end_year) / fadeOut);
      if (op <= 0.02) continue;
      for (const name of emp.countries) {
        const prev = activeCountryOpacity.get(name) || 0;
        if (op > prev) activeCountryOpacity.set(name, op);
      }
    }
    return countries
      .map((f) => {
        const nm = f.properties?.name;
        const op = activeCountryOpacity.get(nm);
        if (!op) return null;
        return { ...f, __opacity: op, __name: nm };
      })
      .filter(Boolean);
  }, [countries, empires, year]);

  const markers = useMemo(
    () => visibleEvents.map((e) => ({ ...e, size: 0.55 })),
    [visibleEvents]
  );

  return (
    <div className="absolute inset-0" data-testid="globe-3d">
      <Globe
        ref={globeRef}
        globeImageUrl={GLOBE_TEXTURE}
        bumpImageUrl={BUMP_TEXTURE}
        backgroundColor="rgba(0,0,0,0)"
        atmosphereColor="#D4AF37"
        atmosphereAltitude={0.18}
        polygonsData={empirePolygons}
        polygonAltitude={0.008}
        polygonCapColor={(d) => `rgba(212, 175, 55, ${d.__opacity * 0.35})`}
        polygonSideColor={() => 'rgba(212, 175, 55, 0.05)'}
        polygonStrokeColor={(d) => `rgba(212, 175, 55, ${Math.min(1, d.__opacity + 0.2)})`}
        polygonLabel={(d) => `<div style="font-family:'Cormorant Garamond',serif;color:#D4AF37;padding:4px 8px;background:rgba(10,10,12,0.85);border:1px solid rgba(212,175,55,0.5);border-radius:4px;">${d.__name}</div>`}
        arcsData={activeArcs}
        arcStartLat="start_lat"
        arcStartLng="start_lng"
        arcEndLat="end_lat"
        arcEndLng="end_lng"
        arcColor={(a) => [`rgba(255,255,255,0.05)`, a.color, `rgba(255,255,255,0.05)`]}
        arcStroke={0.4}
        arcAltitude={0.28}
        arcDashLength={0.5}
        arcDashGap={0.15}
        arcDashInitialGap={() => Math.random()}
        arcDashAnimateTime={3500}
        arcLabel={(a) => `<div style="font-family:'Cormorant Garamond',serif;color:#F7F5F0;padding:4px 8px;background:rgba(10,10,12,0.85);border:1px solid ${a.color};border-radius:4px;">${a.label}</div>`}
        htmlElementsData={markers}
        htmlLat="lat"
        htmlLng="lng"
        htmlAltitude={0.01}
        htmlElement={(d) => {
          const cat = CATEGORIES[d.category];
          const el = document.createElement('div');
          el.className = `globe-marker ${cat.markerClass}`;
          el.setAttribute('data-testid', `marker-${d.id}`);
          el.title = d.title;
          el.style.pointerEvents = 'auto';
          el.onclick = (ev) => {
            ev.stopPropagation();
            onSelect(d);
          };
          return el;
        }}
      />
    </div>
  );
}

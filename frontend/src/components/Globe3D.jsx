import { useRef, useEffect, useMemo } from 'react';
import Globe from 'react-globe.gl';
import { CATEGORIES } from '../lib/history';

const GLOBE_TEXTURE = 'https://unpkg.com/three-globe/example/img/earth-night.jpg';
const BUMP_TEXTURE = 'https://unpkg.com/three-globe/example/img/earth-topology.png';

export default function Globe3D({ events, visibleEvents, onSelect, focusEvent, autoRotate }) {
  const globeRef = useRef();
  const containerRef = useRef();

  // Setup: controls, initial POV
  useEffect(() => {
    const g = globeRef.current;
    if (!g) return;
    g.controls().autoRotate = !!autoRotate;
    g.controls().autoRotateSpeed = 0.35;
    g.controls().enableZoom = true;
    g.controls().minDistance = 180;
    g.controls().maxDistance = 500;
    g.pointOfView({ lat: 20, lng: 0, altitude: 2.4 }, 0);
  }, []);

  useEffect(() => {
    const g = globeRef.current;
    if (!g) return;
    g.controls().autoRotate = !!autoRotate;
  }, [autoRotate]);

  useEffect(() => {
    if (!focusEvent || !globeRef.current) return;
    globeRef.current.pointOfView(
      { lat: focusEvent.lat, lng: focusEvent.lng, altitude: 1.6 },
      1400
    );
  }, [focusEvent]);

  const markers = useMemo(
    () => visibleEvents.map((e) => ({ ...e, size: 0.55 })),
    [visibleEvents]
  );

  return (
    <div ref={containerRef} className="absolute inset-0" data-testid="globe-3d">
      <Globe
        ref={globeRef}
        globeImageUrl={GLOBE_TEXTURE}
        bumpImageUrl={BUMP_TEXTURE}
        backgroundColor="rgba(0,0,0,0)"
        atmosphereColor="#D4AF37"
        atmosphereAltitude={0.18}
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

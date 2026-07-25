import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';
import { CATEGORIES } from '../lib/history';

const GEO_URL = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json';

export default function Map2D({ visibleEvents, onSelect }) {
  return (
    <div className="absolute inset-0 flex items-center justify-center" data-testid="map-2d">
      <ComposableMap
        projectionConfig={{ scale: 165 }}
        width={980}
        height={520}
        style={{ width: '92%', height: 'auto', maxHeight: '82vh' }}
      >
        <Geographies geography={GEO_URL}>
          {({ geographies }) =>
            geographies.map((geo) => (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                fill="#131318"
                stroke="#2A2A30"
                strokeWidth={0.4}
                style={{
                  default: { outline: 'none' },
                  hover: { fill: '#1c1c22', outline: 'none' },
                  pressed: { outline: 'none' },
                }}
              />
            ))
          }
        </Geographies>
        {visibleEvents.map((e) => {
          const c = CATEGORIES[e.category];
          return (
            <Marker
              key={e.id}
              coordinates={[e.lng, e.lat]}
              onClick={() => onSelect(e)}
              data-testid={`marker2d-${e.id}`}
            >
              <circle
                r={4}
                fill={c.color}
                stroke="#F7F5F0"
                strokeOpacity={0.6}
                strokeWidth={0.6}
                style={{ cursor: 'pointer', filter: `drop-shadow(0 0 4px ${c.color})` }}
              />
            </Marker>
          );
        })}
      </ComposableMap>
    </div>
  );
}

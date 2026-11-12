import L from "leaflet";
import { useEffect } from "react";
import { useMap } from "react-leaflet";

type FitBoundsProps = {
  positions: [number, number][];
};

export function FitBounds({ positions }: FitBoundsProps) {
  const map = useMap();
  useEffect(() => {
    if (positions.length === 0) {
      return;
    }
    const bounds = L.latLngBounds(positions);
    map.fitBounds(bounds, { padding: [48, 48] });
  }, [map, positions]);
  return null;
}

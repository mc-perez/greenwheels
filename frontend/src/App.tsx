import { BrowserRouter, Route, Routes } from "react-router-dom";

import { StationMap } from "./components/StationMap";
import { OperatorLayout } from "./layouts/OperatorLayout";
import { RentalsPage } from "./pages/RentalsPage";
import { StationsPage } from "./pages/StationsPage";
import { VehicleTypesPage } from "./pages/VehicleTypesPage";
import { VehiclesPage } from "./pages/VehiclesPage";
import "./leafletSetup";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<OperatorLayout />}>
          <Route path="/" element={<StationMap />} />
          <Route path="/catalogs/types" element={<VehicleTypesPage />} />
          <Route path="/catalogs/stations" element={<StationsPage />} />
          <Route path="/catalogs/vehicles" element={<VehiclesPage />} />
          <Route path="/rentals" element={<RentalsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

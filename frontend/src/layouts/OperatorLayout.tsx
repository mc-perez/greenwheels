import { NavLink, Outlet } from "react-router-dom";

const navClass = ({ isActive }: { isActive: boolean }) =>
  isActive ? "nav-link active" : "nav-link";

export function OperatorLayout() {
  return (
    <div className="operator-shell">
      <nav className="operator-nav" aria-label="Main">
        <span className="nav-brand">GreenWheels</span>
        <NavLink to="/" end className={navClass}>
          Map
        </NavLink>
        <NavLink to="/catalogs/types" className={navClass}>
          Vehicle types
        </NavLink>
        <NavLink to="/catalogs/stations" className={navClass}>
          Stations
        </NavLink>
        <NavLink to="/catalogs/vehicles" className={navClass}>
          Fleet
        </NavLink>
        <NavLink to="/rentals" className={navClass}>
          Rentals
        </NavLink>
      </nav>
      <Outlet />
    </div>
  );
}

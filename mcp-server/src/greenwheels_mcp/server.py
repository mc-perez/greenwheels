from fastmcp import FastMCP

from greenwheels_mcp import tools

mcp = FastMCP("greenwheels")

mcp.tool()(tools.health_check)
mcp.tool()(tools.get_map_stations)
mcp.tool()(tools.list_vehicle_types)
mcp.tool()(tools.list_stations)
mcp.tool()(tools.list_vehicles)
mcp.tool()(tools.list_rentals)
mcp.tool()(tools.get_rental)
mcp.tool()(tools.checkout_rental)
mcp.tool()(tools.return_rental)
mcp.tool()(tools.record_rental_payment)

mcp.tool()(tools.create_vehicle_type)
mcp.tool()(tools.update_vehicle_type)
mcp.tool()(tools.delete_vehicle_type)
mcp.tool()(tools.create_station)
mcp.tool()(tools.update_station)
mcp.tool()(tools.delete_station)
mcp.tool()(tools.create_vehicle)
mcp.tool()(tools.update_vehicle)
mcp.tool()(tools.delete_vehicle)
mcp.tool()(tools.seed_network)

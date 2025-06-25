from obspy.clients.fdsn import Client
from obspy.geodetics import gps2dist_azimuth

def fetch_station_metadata(epi_lat, epi_lon):
    try:
        rs = Client('RASPISHAKE')
        inventory = rs.get_stations(network="AM", latitude=28.0, longitude=84.0, maxradius=2.5, level="station")
        stations = []
        for network in inventory:
            for station in network:
                dist_m, _, _ = gps2dist_azimuth(station.latitude, station.longitude, epi_lat, epi_lon)
                dist_km = dist_m / 1000
                stations.append({
                    "station_code": f"{network.code}.{station.code}",
                    "lat": station.latitude,
                    "lon": station.longitude,
                    "elev": station.elevation,
                    "dist_km": dist_km
                })
        if stations:
            print(f"Fetched {len(stations)} stations from RASPISHAKE")
            return {s["station_code"]: s for s in stations}
        raise ValueError("No stations found")
    except Exception as e:
        print(f"Error fetching station metadata: {e}. Using fallback stations.")
        return {
            "AM.R0BD5": {"lat": 28.18, "lon": 83.60, "elev": 785.0, "dist_km": gps2dist_azimuth(28.18, 83.60, epi_lat, epi_lon)[0] / 1000},
            "AM.R0CEA": {"lat": 28.23, "lon": 83.92, "elev": 787.0, "dist_km": gps2dist_azimuth(28.23, 83.92, epi_lat, epi_lon)[0] / 1000}
        }
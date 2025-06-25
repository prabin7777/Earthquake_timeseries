import os
import obspy
from obspy import read

def process_seismic_data(folder_path, station_metadata):
    traces_with_dist = []
    used_stations = {}
    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith(".mseed"):
            file_path = os.path.join(folder_path, file)
            print(f"Processing file: {file}")
            try:
                st = read(file_path)
                print(f"Found {len(st)} traces in {file}")
                z_traces = [tr for tr in st if tr.stats.channel.endswith("Z")]
                if not z_traces:
                    print(f"No Z-axis traces found in {file}")
                    continue
                for tr in z_traces:
                    station_code = tr.stats.network + "." + tr.stats.station
                    if station_code in station_metadata:
                        dist_km = station_metadata[station_code]['dist_km']
                        traces_with_dist.append((tr, dist_km))
                        used_stations[station_code] = station_metadata[station_code]
                    else:
                        print(f"No metadata for {station_code}, skipping trace")
            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue
    print(f"Collected {len(traces_with_dist)} traces with distance")
    return traces_with_dist, used_stations
import os
import obspy
from obspy import read
from obspy.clients.fdsn import Client
from obspy.geodetics import gps2dist_azimuth
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import matplotlib.lines as mlines

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

def process_data(folder_path, output_csv, output_pdf, map_pdf):
    gain = 1e9
    plots_per_page = 4
    nrows, ncols = 4, 1  # 4 rows, 1 column for A4 portrait layout
    figsize = (8.27, 11.69)  # A4 size in inches (portrait)
    epi_lat, epi_lon, epi_mag = 28.2292, 84.3985, 5.3

    if nrows * ncols != plots_per_page:
        print(f"Error: nrows ({nrows}) * ncols ({ncols}) must equal plots_per_page ({plots_per_page}).")
        return

    if not os.path.isdir(folder_path) or not os.access(folder_path, os.W_OK):
        print(f"Error: Directory '{folder_path}' issue.")
        return

    station_metadata = fetch_station_metadata(epi_lat, epi_lon)
    if station_metadata:
        pd.DataFrame(station_metadata.values()).to_csv(output_csv, index=False)
        print(f"Saved station metadata to {output_csv}")

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
    if not traces_with_dist:
        print("Warning: No valid traces found for plotting.")
        return

    create_map(used_stations, epi_lat, epi_lon, epi_mag, map_pdf)
    create_velocity_plots(traces_with_dist, station_metadata, output_pdf, gain, plots_per_page, nrows, ncols, figsize, epi_mag)

def create_map(used_stations, epi_lat, epi_lon, epi_mag, map_pdf):
    with PdfPages(map_pdf) as pdf:
        fig_map = plt.figure(figsize=(10, 8))
        ax_map = fig_map.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax_map.set_extent([80.0, 88.5, 26.0, 30.5])
        ax_map.add_feature(cfeature.LAND)
        ax_map.add_feature(cfeature.COASTLINE)
        ax_map.add_feature(cfeature.BORDERS, linestyle=':')
        ax_map.add_feature(cfeature.RIVERS)
        ax_map.gridlines(draw_labels=True)
        ax_map.scatter(epi_lon, epi_lat, s=200, c='red', marker='*', label=f'Lamjung M{epi_mag} Epicenter')
        
        # Sort stations by distance and number them accordingly
        sorted_stations = sorted(used_stations.items(), key=lambda x: x[1]['dist_km'])
        for idx, (station_code, station) in enumerate(sorted_stations, 1):
            ax_map.scatter(station['lon'], station['lat'], s=100, c='blue', marker='^')
            ax_map.text(station['lon'] + 0.05, station['lat'], str(idx), fontsize=8, weight='bold')
        ax_map.set_title("Raspberry Shake Stations and Lamjung Earthquake Epicenter")
        pdf.savefig(fig_map)

        fig_legend = plt.figure(figsize=(10, 8))
        ax_legend = fig_legend.add_subplot(1, 1, 1)
        ax_legend.axis('off')
        legend_elements = [
            mlines.Line2D([], [], color='red', marker='*', linestyle='None', markersize=15, label=f'Lamjung M{epi_mag} Epicenter'),
            mlines.Line2D([], [], color='blue', marker='^', linestyle='None', markersize=10, label='Raspberry Shake Station')
        ]
        for idx, (station_code, _) in enumerate(sorted_stations, 1):
            legend_elements.append(mlines.Line2D([], [], marker='None', linestyle='None', label=f"{idx}: {station_code}"))
        ax_legend.legend(handles=legend_elements, loc='center', fontsize=10)
        ax_legend.set_title("Legend")
        pdf.savefig(fig_legend)
        plt.close(fig_map)
        plt.close(fig_legend)
        print(f"Map and legend saved to {map_pdf}")

def create_velocity_plots(traces_with_dist, station_metadata, output_pdf, gain, plots_per_page, nrows, ncols, figsize, epi_mag):
    with PdfPages(output_pdf) as pdf:
        # Sort traces by distance for ascending order
        traces_with_dist.sort(key=lambda x: x[1])
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize, constrained_layout=True)
        axes = axes.flatten()
        plot_idx = 0

        for tr, dist_km in traces_with_dist:
            try:
                tr.detrend("linear")
                tr.detrend("demean")
                tr.data = (tr.data / gain) * 1e6
                times = tr.times("matplotlib")

                if plot_idx >= plots_per_page:
                    pdf.savefig(fig)
                    plt.close(fig)
                    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, constrained_layout=True)
                    axes = axes.flatten()
                    plot_idx = 0

                ax = axes[plot_idx]
                ax.plot_date(times, tr.data, 'k-', linewidth=0.5)
                station_code = tr.stats.network + "." + tr.stats.station
                meta = station_metadata[station_code]
                ax.set_title(f"{tr.id} — {tr.stats.starttime.date}\nDist: {meta['dist_km']:.1f}km (#{plot_idx + 1})", fontsize=8)
                ax.set_ylabel("Velocity (µm/s)", fontsize=6)
                ax.set_xlabel("Time (UTC)", fontsize=6)
                ax.grid(True)
                ax.tick_params(axis='both', which='major', labelsize=5)
                fig.autofmt_xdate()
                plot_idx += 1
                print(f"Plotted trace: {tr.id} at distance {dist_km:.1f}km")
            except Exception as e:
                print(f"Error plotting trace {tr.id}: {e}")
                continue

        if plot_idx > 0:
            for i in range(plot_idx, nrows * ncols):
                axes[i].set_visible(False)
            pdf.savefig(fig)
            plt.close(fig)
        print(f"Plots saved to {output_pdf}")
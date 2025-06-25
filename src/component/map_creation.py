import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.lines as mlines

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
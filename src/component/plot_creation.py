import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def create_velocity_plots(traces_with_dist, station_metadata, output_pdf, gain, plots_per_page, nrows, ncols, figsize, epi_mag):
    with PdfPages(output_pdf) as pdf:
        # Sort traces by distance for ascending order
        traces_with_dist.sort(key=lambda x: x[1])
        # Create a figure and a set of subplots, using constrained_layout for automatic spacing
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize, constrained_layout=True)
        axes = axes.flatten() # Flatten the axes array for easy iteration
        plot_idx = 0

        for tr, dist_km in traces_with_dist:
            try:
                # Pre-processing: remove linear trend and mean
                tr.detrend("linear")
                tr.detrend("demean")
                # Convert data from nm/s to µm/s (micrometers per second)
                # Assuming gain converts raw counts to nm/s, so dividing by gain and multiplying by 1e6 (nm to µm)
                tr.data = (tr.data / gain) * 1e6 
                # Get time values in Matplotlib's date format
                times = tr.times("matplotlib")

                # Check if current page is full, save and start new page if needed
                if plot_idx >= plots_per_page:
                    pdf.savefig(fig) # Save the current page
                    plt.close(fig) # Close the current figure to free memory
                    # Create a new figure and subplots for the next page
                    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, constrained_layout=True)
                    axes = axes.flatten()
                    plot_idx = 0 # Reset plot index for the new page

                # Get the current subplot axis
                ax = axes[plot_idx]
                # Plot the trace data
                ax.plot_date(times, tr.data, 'k-', linewidth=0.5)
                
                # Get station metadata using the station code from the trace ID
                station_code = tr.stats.network + "." + tr.stats.station
                meta = station_metadata[station_code]
                
                # Set subplot title with trace ID, date, distance, and plot number
                ax.set_title(f"{tr.id} — {tr.stats.starttime.date}\nDist: {meta['dist_km']:.1f}km (#{plot_idx + 1})", fontsize=8)
                ax.set_ylabel("Velocity (µm/s)", fontsize=6)
                ax.set_xlabel("Time (UTC)", fontsize=6)
                ax.grid(True) # Add grid lines
                ax.tick_params(axis='both', which='major', labelsize=5) # Adjust tick label size
                
                # Remove fig.autofmt_xdate() as it conflicts with constrained_layout=True
                # fig.autofmt_xdate() 
                
                plot_idx += 1 # Increment plot index
                print(f"Plotted trace: {tr.id} at distance {dist_km:.1f}km")
            except Exception as e:
                print(f"Error plotting trace {tr.id}: {e}")
                continue

        # After the loop, save any remaining plots on the last page
        if plot_idx > 0:
            # Hide any unused subplots on the last page
            for i in range(plot_idx, nrows * ncols):
                axes[i].set_visible(False)
            pdf.savefig(fig) # Save the final page
            plt.close(fig) # Close the figure
        print(f"Plots saved to {output_pdf}")


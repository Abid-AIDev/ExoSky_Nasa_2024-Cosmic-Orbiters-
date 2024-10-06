import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.gaia import Gaia
import matplotlib.colors as mcolors

def fetch_gaia_data(num_stars=100):
    """Fetch star data from the Gaia database."""
    query = f"SELECT TOP {num_stars} ra, dec, parallax, phot_g_mean_mag FROM gaiadr2.gaia_source WHERE parallax IS NOT NULL"
    job = Gaia.launch_job(query)
    return job.get_results()

def convert_parallax_to_distance(parallax):
    """Convert parallax to distance in parsecs."""
    return 1 / (parallax * 1e-3)  # Convert from milliarcseconds to arcseconds

def filter_valid_data(distance, ra, dec, brightness):
    """Filter valid data points with positive distance."""
    valid_mask = distance > 0
    return distance[valid_mask], ra[valid_mask], dec[valid_mask], brightness[valid_mask]

def plot_star_map(x, y, z, colors):
    """Plot the 3D star map with interactive features."""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot for stars with larger markers
    scatter = ax.scatter(x, y, z, c=colors, marker='o', s=10, alpha=0.9)
    
    # Mark the origin as a big blue dot
    ax.scatter(0, 0, 0, c='blue', marker='o', s=100, label='Origin')

    # Set plot limits
    ax.set_xlim([-1000, 1000])
    ax.set_ylim([-1000, 1000])
    ax.set_zlim([-1000, 1000])

    # Label axes
    ax.set_xlabel('X (light years)', fontsize=16)
    ax.set_ylabel('Y (light years)', fontsize=16)
    ax.set_zlabel('Z (light years)', fontsize=16)

    # Dark background for a space-like appearance
    ax.set_facecolor('black')
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 1.0))

    # Add grid lines
    ax.grid(color='gray', linestyle='--', linewidth=1.5)

    # Create a color bar
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Color coded by brightness (phot_g_mean_mag)', fontsize=12)

    # Set title
    plt.title("3D Star Map from Gaia Data", fontsize=20)

    # Full screen settings
    plt.get_current_fig_manager().full_screen_toggle()

    # Show the plot
    plt.legend()
    plt.show()

def main(num_stars=100):
    """Main function to execute the script."""
    try:
        results = fetch_gaia_data(num_stars)
        parallax = results['parallax'].data
        brightness = results['phot_g_mean_mag'].data
        distance = convert_parallax_to_distance(parallax)

        # Get RA and Dec, filtering invalid entries
        ra = results['ra'].data
        dec = results['dec'].data
        distance, ra, dec, brightness = filter_valid_data(distance, ra, dec, brightness)

        # Convert to Cartesian coordinates for 3D plotting
        coords = SkyCoord(ra=ra * u.degree, dec=dec * u.degree, distance=distance * u.pc)
        x = coords.cartesian.x.value
        y = coords.cartesian.y.value
        z = coords.cartesian.z.value

        # Normalize brightness for color mapping
        norm = mcolors.Normalize(vmin=np.min(brightness), vmax=np.max(brightness))
        colors = plt.cm.viridis(norm(brightness))

        # Plot the star map
        plot_star_map(x, y, z, colors)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main(num_stars=100)


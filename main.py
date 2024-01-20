import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import ScalarFormatter, MaxNLocator


def mandlebrot(x, y, max_iters):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the
    Mandlebrot set given a fixed number of iterations.
    """
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z**2 + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return max_iters


def generate_colormap(num_colors=200):
    # Create a colour map of 200 colours
    cols = [
        (0.0, 0.0, 0.5),  # Dark Blue
        (0.0, 0.0, 1.0),  # Blue
        (0.0, 0.5, 1.0),  # Light Blue
        (0.0, 1.0, 1.0),  # Cyan
        (0.5, 1.0, 0.5),  # Light Green
        (1.0, 1.0, 0.0),  # Yellow
        (1.0, 0.5, 0.0),  # Orange
        (1.0, 0.0, 0.0),  # Red
        (0.5, 0.0, 0.0),  # Dark Red
        (0.5, 0.0, 0.5),  # Purple
    ]
    full_repetitions = num_colors // len(cols)
    remaining_elements = num_colors % len(cols)
    repeated_list = cols * full_repetitions + cols[:remaining_elements]
    return colors.ListedColormap(np.array(repeated_list))


def plot(ax, x_centre, y_centre, plot_range, num_iterations=100, resolution=200):
    function = np.vectorize(lambda x, y: mandlebrot(x, y, num_iterations))
    colormap = generate_colormap(num_iterations)

    x_min = x_centre - plot_range / 2
    x_max = x_centre + plot_range / 2
    y_min = y_centre - plot_range / 2
    y_max = y_centre + plot_range / 2
    x_step = (x_max - x_min) / resolution
    y_step = (y_max - y_min) / resolution

    xs = np.arange(x_min, x_max, x_step)
    ys = np.arange(y_max, y_min, -y_step)

    x_grid, y_grid = np.meshgrid(xs, ys)
    value_grid = function(x_grid, y_grid)

    ax.imshow(value_grid, cmap=colormap, vmin=0, vmax=num_iterations-1, extent=(x_min, x_max, y_min, y_max), )

    # Set the axes tick locators to MaxNLocator for better control
    # i.e. put the ticks on nice round numbers
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5, prune='both', integer=False))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5, prune='both', integer=False))

    # Set the x-axis and y-axis tick labels to scientific notation
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False, useLocale=False))
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False, useLocale=False))


# this is the coordinate we zoom in on
interesting_places = {
    'Seahorse Valley': (-0.743643135, 0.131825963),
    'Satellite Bulbs': (-1.25066, -0.02012),
    'Mini Mandlebrots': (0.355, 0.355),
    'Filaments and Bridges': (-1.747, 0.006),
    'Antenna and Spiral Features': (-1.25, 0),
    'Some Place': (-1.251, -0.071)
}

target_x, target_y = interesting_places['Seahorse Valley']
# How many colours to produce
num_iters = 100
# Sharpness of plot
plot_resolution = 400

# create a plot of 10 images in a 2 by 5 grid
fig, axs = plt.subplots(2, 5, figsize=(20, 12))

for i in range(0, 10):
    # get the row and col of this plot
    row, col = int(i / 5), i % 5
    axes = axs[row, col]
    # start with a width of 4 and zoom in by powers of 2
    zoom_range = 4 / (2 ** i)
    # plot the image
    plot(axes, target_x, target_y, zoom_range, resolution=plot_resolution, num_iterations=num_iters)

plt.tight_layout()
plt.show()

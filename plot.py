import matplotlib.pyplot as plt
import numpy as np
import json
import random


# Helper function to extract data for plotting
def extract_lines(data, key):
    lines = []
    for group in ["async", "default", "threaded"]:
        for concurrency in ["1", "4", "8"]:
            values = list(map(float, data[group][concurrency]["1"][concurrency][key]))
            lines.append(values)
    return lines


with open("results/full_results.json") as f:
    data = json.load(f)

# Extract RPS and Latency data for line plots
rps_lines = extract_lines(data, "rps")
lats_lines = extract_lines(data, "lats")

# Prepare x-axis labels (representing the 4 data points)
x_labels = ["1", "50", "100", "150"]
x = np.arange(len(x_labels))

# Define colors for each mode
colors = {"async": "blue", "default": "green", "threaded": "red"}

# Define markers for each concurrency level
markers = {"1": "o", "4": "s", "8": "^"}

# Create the subplots for RPS and Latency
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Plot RPS lines with shared colors and markers
for i, line in enumerate(rps_lines):
    group = ["async", "default", "threaded"][i // 3]
    concurrency = ["1", "4", "8"][i % 3]
    color = colors[group]
    marker = markers[concurrency]
    ax1.plot(x, line, color=color, marker=marker, label=f"{group}-{concurrency}")

ax1.set_xlabel("Concurent requests")
ax1.set_ylabel("Requests Per Second (RPS)")
ax1.set_title("RPS by Concurrency and Group")
ax1.set_xticks(x)
ax1.set_xticklabels(x_labels)
ax1.legend(loc="upper left", fontsize="small")

# Plot Latency lines with shared colors and markers
for i, line in enumerate(lats_lines):
    group = ["async", "default", "threaded"][i // 3]
    concurrency = ["1", "4", "8"][i % 3]
    color = colors[group]
    marker = markers[concurrency]
    ax2.plot(x, line, color=color, marker=marker, label=f"{group}-{concurrency}")

ax2.set_xlabel("Concurrent requests")
ax2.set_ylabel("Latency (ms)")
ax2.set_title("Latency")
ax2.set_xticks(x)
ax2.set_xticklabels(x_labels)
ax2.set_ylim([0, 4000])
ax2.legend(loc="upper left", fontsize="small")

# Adjust layout and save the figures as JPEGs
plt.tight_layout()

fig.savefig("rps_plot_line_with_markers_and_colors.jpeg", format="jpeg")
fig.savefig("latency_plot_line_with_markers_and_colors.jpeg", format="jpeg")

plt.show()

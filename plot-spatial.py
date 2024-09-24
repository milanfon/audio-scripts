import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
from scipy.interpolate import interp1d

def plot_speaker_response(csv_filename, output_filename="speaker_response.png"):
    measured_values = []

    with open(csv_filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  
        for row in csv_reader:
            segment = int(row[0])
            level = float(row[1])
            measured_values.append((segment, level))

    num_segments = len(measured_values)
    positions = [ (segment - 1) * 360 / num_segments for segment, _ in measured_values ]  
    levels = [ level for _, level in measured_values ]

    angles = np.deg2rad(positions)
    levels = np.array(levels)

    angles = np.append(angles, angles[0] + 2 * np.pi)
    levels = np.append(levels, levels[0])

    angles_smooth = np.linspace(angles[0], angles[-1], 360)
    interp_func = interp1d(angles, levels, kind='cubic')
    levels_smooth = interp_func(angles_smooth)
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(20, 10))  
    ax.plot(angles_smooth, levels_smooth, label='Speaker Response')  
    ax.fill(angles_smooth, levels_smooth, alpha=0.3)
    
    ax.set_theta_zero_location('S')  
    ax.set_theta_direction(-1)  

    max_level = max(levels)
    min_level = min(levels)
    r_ticks = np.linspace(min_level, max_level, num=5)
    
    measurement_angles = positions  
    measurement_angles = [angle % 360 for angle in measurement_angles]  
    ax.set_rgrids(r_ticks, angle=0)
    ax.set_thetagrids(measurement_angles)
    
    ax.set_title('Speaker Spatial Response')
    ax.legend(loc='upper right')

    plt.savefig(output_filename, transparent=True, dpi=432)  
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_speaker_response.py <csv_filename>")
        sys.exit(1)

    csv_filename = sys.argv[1]
    plot_speaker_response(csv_filename)

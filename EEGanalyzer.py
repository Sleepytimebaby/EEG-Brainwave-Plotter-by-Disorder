import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Load the dataset
file_path = "PATH-TO-EEG-DATASET"
df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# Define frequency band prefixes as they appear in your columns
band_prefixes = {
    'delta': 'AB.A.delta',
    'theta': 'AB.B.theta',
    'alpha': 'AB.C.alpha',
    'beta': 'AB.D.beta',
    'highbeta': 'AB.E.highbeta',
    'gamma': 'AB.F.gamma'
}

# Predefined electrode order (a typical montage order)
electrode_order = ["FP1", "FP2", "F7", "F3", "Fz", "F4", "F8", 
                   "T3", "C3", "Cz", "C4", "T4", "T5", "P3", "Pz", "P4", "T6", "O1", "O2"]

# Build a mapping for each band: electrode -> column name
band_columns = {}
for band, prefix in band_prefixes.items():
    cols = [col for col in df.columns if col.startswith(prefix)]
    mapping = {}
    for col in cols:
        parts = col.split('.')
        electrode = parts[-1]  # electrode code (e.g., FP1, FP2, etc.)
        mapping[electrode] = col
    sorted_mapping = {elec: mapping[elec] for elec in electrode_order if elec in mapping}
    band_columns[band] = sorted_mapping

# Function to plot the average brainwave curves for multiple disorders
def plot_brainwaves_comparison(disorders):
    if not disorders:
        return  # No disorders selected
        
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f"EEG Waves Comparison Across Disorders", fontsize=16)
    axes = axes.flatten()
    
    # Generate a colormap with distinct colors for each disorder
    colors = plt.cm.tab10.colors[:len(disorders)]
    
    # Loop through each frequency band
    for i, band in enumerate(band_prefixes.keys()):
        ax = axes[i]
        
        # Plot each disorder in this band
        for j, disorder in enumerate(disorders):
            subset = df[df['main.disorder'] == disorder]
            if len(subset) == 0:
                continue  # Skip if no data for this disorder
                
            electrodes = []
            avg_values = []
            for elec, col in band_columns[band].items():
                electrodes.append(elec)
                avg_values.append(subset[col].mean())
                
            ax.plot(electrodes, avg_values, marker='o', linestyle='-', 
                    color=colors[j], label=disorder)
            
        ax.set_title(band.capitalize())
        ax.set_xlabel("Electrode")
        ax.set_ylabel("Amplitude")
        ax.tick_params(axis='x', rotation=45)  # Rotate electrode labels for readability
        ax.grid(True)
        
        # Only add legend to the first plot to avoid redundancy
        if i == 0:
            ax.legend(loc='best')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# Create the Tkinter GUI for multi-selecting disorders
root = tk.Tk()
root.title("EEG Brainwave Comparison Tool")
root.geometry("400x500")  # Larger window to accommodate the listbox

# Get a sorted list of unique disorders
disorder_list = sorted(df['main.disorder'].unique())

# Frame for the listbox and scrollbar
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Label for the listbox
label = ttk.Label(frame, text="Select Disorders to Compare (hold Ctrl for multiple):")
label.pack(padx=5, pady=5, anchor=tk.W)

# Scrollbar for the listbox
scrollbar = ttk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox for multiple disorder selection
disorder_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, 
                              yscrollcommand=scrollbar.set,
                              height=15)
for disorder in disorder_list:
    disorder_listbox.insert(tk.END, disorder)
disorder_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
scrollbar.config(command=disorder_listbox.yview)

# Frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(padx=10, pady=10, fill=tk.X)

# Function to handle color selection
def on_plot_comparison():
    selected_indices = disorder_listbox.curselection()
    if not selected_indices:
        return  # No selections

    selected_disorders = [disorder_listbox.get(i) for i in selected_indices]
    plot_brainwaves_comparison(selected_disorders)

# Button to trigger the comparison plot
plot_button = ttk.Button(button_frame, text="Compare Selected Disorders", 
                         command=on_plot_comparison)
plot_button.pack(side=tk.LEFT, padx=5, pady=5)

# Button to clear selection
def clear_selection():
    disorder_listbox.selection_clear(0, tk.END)

clear_button = ttk.Button(button_frame, text="Clear Selection", 
                          command=clear_selection)
clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Optional: Button to show the original single-disorder view
def show_single_view():
    selected_indices = disorder_listbox.curselection()
    if len(selected_indices) != 1:
        return  # Need exactly one selection
    
    selected_disorder = disorder_listbox.get(selected_indices[0])
    
    # Original plotting function (unchanged)
    subset = df[df['main.disorder'] == selected_disorder]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f"Average EEG Waves by Disorder: {selected_disorder}", fontsize=16)
    axes = axes.flatten()
    
    # Loop through each frequency band and plot its wave
    for i, band in enumerate(band_prefixes.keys()):
        ax = axes[i]
        electrodes = []
        avg_values = []
        for elec, col in band_columns[band].items():
            electrodes.append(elec)
            avg_values.append(subset[col].mean())
        ax.plot(electrodes, avg_values, marker='o', linestyle='-', color='b')
        ax.set_title(band.capitalize())
        ax.set_xlabel("Electrode")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

single_view_button = ttk.Button(button_frame, text="Show Single View", 
                               command=show_single_view)
single_view_button.pack(side=tk.LEFT, padx=5, pady=5)

# Add optional statistical information display
stats_frame = ttk.LabelFrame(root, text="Statistics")
stats_frame.pack(padx=10, pady=5, fill=tk.X)

stats_label = ttk.Label(stats_frame, text="Select disorders to see sample sizes")
stats_label.pack(padx=5, pady=5)

def update_stats():
    selected_indices = disorder_listbox.curselection()
    if not selected_indices:
        stats_label.config(text="Select disorders to see sample sizes")
        return
        
    stats_text = "Sample sizes:\n"
    for idx in selected_indices:
        disorder = disorder_listbox.get(idx)
        count = len(df[df['main.disorder'] == disorder])
        stats_text += f"• {disorder}: {count} samples\n"
        
    stats_label.config(text=stats_text)
    
# Button to update statistics
stats_button = ttk.Button(stats_frame, text="Show Statistics", command=update_stats)
stats_button.pack(padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()

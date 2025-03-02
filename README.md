# EEG-Brainwave-Plotter-by-Disorder

This repository contains a Python script that lets you visualize EEG brainwave data by disorder through an 
interactive GUI built with Tkinter. The tool processes a machine learning EEG dataset, groups the data by disorder, 
and plots the actual brainwave curves (average amplitudes) for each frequency band across standard EEG electrodes.

Features
	
•	Interactive GUI:
Use a dropdown menu to select a disorder and instantly update the brainwave plots.
	
•	Detailed Visualization:
Plots a 2x3 grid of line charts for the following frequency bands:
	•	Delta
	•	Theta
	•	Alpha
	•	Beta
	•	High Beta
	•	Gamma
	•	Data Processing:

Automatically maps EEG feature columns (based on frequency band prefixes) to standard electrode positions.

Requirements
	•	Python 3.x
	•	Pandas
	•	Matplotlib
	•	Tkinter (usually comes with Python)

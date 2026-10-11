# PitchLab — From Sound to Musical Notes

A Python-based audio frequency analyzer that uses **Fast Fourier Transform (FFT)** and harmonic-aware analysis to estimate the fundamental frequency of a sound and identify its corresponding musical note.

## Overview

PitchLab demonstrates how Digital Signal Processing (DSP) can be used to analyze audio signals and extract meaningful frequency information.

The application accepts a generated test signal or a WAV audio recording, analyzes its frequency components, estimates the fundamental frequency, and maps the result to the nearest musical note.

## Features

* **Audio input:** Analyze generated test signals and WAV recordings.
* **FFT-based frequency analysis:** Transform a time-domain audio signal into its frequency-domain representation.
* **Musical note detection:** Map the estimated frequency to the nearest equal-tempered musical note.
* **Harmonic-aware detection:** Estimate the fundamental frequency when a higher harmonic has a greater amplitude than the fundamental.
* **Signal visualization:** Plot the audio waveform and frequency spectrum.
* **Frequency comparison:** Compare the strongest spectral peak with the harmonic-aware estimate.

## How It Works

The processing pipeline consists of the following stages:

1. **Audio acquisition:** Generate a test signal or load a WAV recording.
2. **Signal preparation:** Select a suitable audio segment and apply a Hann window to reduce spectral leakage.
3. **FFT computation:** Use the Fast Fourier Transform to obtain the signal's frequency spectrum.
4. **Peak analysis:** Identify prominent frequency components in the spectrum.
5. **Fundamental estimation:** Use harmonic relationships to estimate the fundamental frequency.
6. **Note identification:** Convert the estimated frequency into the nearest musical note and calculate its deviation in cents.
7. **Visualization:** Display the waveform and frequency spectrum for analysis.

## Technologies Used

* Python
* NumPy — numerical computation and FFT
* SciPy — signal processing and peak detection
* Matplotlib — waveform and spectrum visualization
* SoundFile — WAV audio file handling

## Installation

### Prerequisites

* Python 3.10 or later recommended
* Git
* A WAV audio file for real-recording analysis

### 1. Clone the repository

```bash
git clone https://github.com/Sachit-Timane/PitchLab.git
cd PitchLab
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Execute the main Python script:

```bash
python pitchlab.py
```

Use the interactive menu to select the desired operation:

| Option | Operation                                                       |
| ------ | --------------------------------------------------------------- |
| 1      | Test frequency estimation using a known 440 Hz signal           |
| 2      | Analyze a WAV audio recording                                   |
| 3      | Test harmonic-aware detection                                   |
| 4      | Compare the strongest FFT peak with the harmonic-aware estimate |

*Menu options may vary slightly depending on the current version of the script.*

For WAV analysis, provide the path to the audio file when prompted.

## Experimental Results

### Experiment 1: Known-frequency test

A synthetic signal with a known frequency of 440 Hz is analyzed to verify the frequency-estimation pipeline.

The expected musical note is **A4**.

### Experiment 2: Harmonic-aware detection

A synthetic signal with a fundamental frequency of 220 Hz is generated with a stronger second harmonic at 440 Hz.

| Measurement                     | Observed result |
| ------------------------------- | --------------: |
| Actual fundamental              |       220.00 Hz |
| Strongest FFT peak              |       441.43 Hz |
| Note from strongest peak        |              A4 |
| Harmonic-aware estimate         |       220.72 Hz |
| Note from harmonic-aware method |              A3 |

The strongest-peak method selects the second harmonic rather than the actual fundamental. The harmonic-aware method estimates the fundamental near 220 Hz and correctly identifies the note as A3.

### Experiment 3: Real audio recording

A tuning-fork WAV recording was analyzed.

| Measurement        | Observed result |
| ------------------ | --------------: |
| Strongest FFT peak |       441.43 Hz |
| Detected note      |              A4 |
| Offset from 440 Hz |     +5.62 cents |

These values are specific to the tested recording and analysis settings; results may differ with other recordings, noise levels, and sampling parameters.

## Limitations

* The current implementation is primarily designed for estimating a dominant musical pitch from a single tone or a signal with a clear fundamental.
* FFT frequency resolution depends on the sampling rate and FFT size.
* Harmonics, background noise, transients, and low-amplitude recordings can affect estimation accuracy.
* Mapping a frequency to the nearest musical note does not guarantee that the source was played in tune.
* Polyphonic audio containing multiple simultaneous notes may require more advanced pitch-detection techniques.

## Future Improvements

* Add support for live microphone input.
* Implement improved pitch estimation using methods such as autocorrelation or YIN.
* Add configurable FFT sizes and compare frequency resolution.
* Evaluate performance across different instruments and noisy recordings.
* Extend the application toward multi-pitch detection and real-time visualization.

## Academic Context

**Project:** PitchLab — From Sound to Musical Notes
**Domain:** Digital Signal Processing
**Purpose:** Educational implementation of FFT-based audio analysis and musical pitch estimation.

## License

This project is available for educational and academic use. A formal open-source license can be added to define permissions for reuse and redistribution.

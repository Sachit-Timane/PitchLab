
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import find_peaks, windows

# -----------------------------------------
# PitchLab: FFT-Based Musical Note Detection
# -----------------------------------------

SAMPLE_RATE = 44100
FFT_SIZE = 8192


def generate_test_signal(frequency=440, duration=1.0, sr=SAMPLE_RATE):
    """Generate a known sine wave for validation."""
    t = np.arange(int(sr * duration)) / sr
    signal = np.sin(2 * np.pi * frequency * t)
    return signal, sr

def generate_harmonic_signal(frequency=220, duration=1.0, sr=SAMPLE_RATE):
    t = np.arange(int(sr * duration)) / sr

    signal = (
        0.4 * np.sin(2 * np.pi * frequency * t)
        + 1.0 * np.sin(2 * np.pi * 2 * frequency * t)
        + 0.7 * np.sin(2 * np.pi * 3 * frequency * t)
        + 0.4 * np.sin(2 * np.pi * 4 * frequency * t)
    )

    return signal, sr


def load_audio(filename):
    filename = filename.strip().strip('"').strip("'")

    audio, sr = sf.read(filename)

    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    audio = audio.astype(float)

    if len(audio) == 0:
        raise ValueError("The WAV file is empty.")

    # Select the loudest segment of FFT_SIZE samples
    if len(audio) > FFT_SIZE:
        window_count = 1 + (len(audio) - FFT_SIZE) // (FFT_SIZE // 2)
        hop = FFT_SIZE // 2

        best_start = 0
        best_rms = -1.0

        for i in range(window_count):
            start = i * hop
            segment = audio[start:start + FFT_SIZE]
            rms = np.sqrt(np.mean(segment ** 2))

            if rms > best_rms:
                best_rms = rms
                best_start = start

        audio = audio[best_start:best_start + FFT_SIZE]

        print(f"Selected audio segment: {best_start / sr:.3f} s")
        print(f"Segment RMS: {best_rms:.6f}")

    return audio, sr


def analyze_fft(audio, sr, fft_size=FFT_SIZE):
    audio = np.asarray(audio, dtype=float)

    if len(audio) == 0:
        raise ValueError("Audio file contains no samples.")

    # Use a segment with the actual audio data
    if len(audio) < fft_size:
        audio = np.pad(audio, (0, fft_size - len(audio)))
    else:
        audio = audio[:fft_size]

    # Remove DC offset and apply Hann window
    audio = audio - np.mean(audio)
    window = windows.hann(len(audio), sym=False)
    windowed = audio * window

    print("FFT input max:", np.max(np.abs(audio)))
    print("Windowed max:", np.max(np.abs(windowed)))
    print("FFT max magnitude:", np.max(np.abs(np.fft.rfft(windowed))))
    print("FFT size:", len(windowed))
    # Calculate one-sided FFT magnitude
    spectrum = np.fft.rfft(windowed)
    magnitude = np.abs(spectrum)
    frequencies = np.fft.rfftfreq(len(windowed), d=1 / sr)

    # Ignore DC and find the strongest non-zero frequency bin.
    # This avoids failing when find_peaks() returns no local maxima.
    # if len(magnitude) <= 1 or np.max(magnitude[1:]) <= 1e-12:
    #     raise ValueError(
    #         "No usable frequency content found in this audio segment."
    #     )
    print("Non-DC maximum:", np.max(magnitude[1:]))
    
    
    # Search the musical fundamental range for this experiment
    min_freq = 70
    max_freq = 2000

    valid = np.where(
        (frequencies >= min_freq) &
        (frequencies <= max_freq)
    )[0]

    strongest = valid[np.argmax(magnitude[valid])]
    estimated_frequency = frequencies[strongest]
    return frequencies, magnitude, estimated_frequency



def run_harmonic_experiment():
    audio, sr = generate_harmonic_signal(220)

    frequencies, magnitude, strongest = analyze_fft(audio, sr)
    fundamental = estimate_fundamental(frequencies, magnitude)

    strongest_note, _ = frequency_to_note(strongest)
    fundamental_note, _ = frequency_to_note(fundamental)

    print("\n=== Harmonic Detection Experiment ===")
    print(f"Actual fundamental: 220.00 Hz (A3)")
    print(f"Strongest peak: {strongest:.2f} Hz ({strongest_note})")
    print(
        f"Harmonic-aware estimate: "
        f"{fundamental:.2f} Hz ({fundamental_note})"
    )

    plot_results(
        audio, sr, frequencies, magnitude,
        strongest, fundamental
    )
    
def estimate_fundamental(frequencies, magnitude):
    peaks, _ = find_peaks(magnitude)

    # Consider plausible musical fundamentals
    candidates = [
        p for p in peaks
        if 70 <= frequencies[p] <= 1000
    ]

    if not candidates:
        return 0.0

    best_frequency = 0.0
    best_score = -1.0

    for peak in candidates:
        candidate_frequency = frequencies[peak]
        score = 0.0

        # Score the candidate using its harmonic series
        for harmonic in range(1, 7):
            target = candidate_frequency * harmonic

            if target >= frequencies[-1]:
                break

            index = np.argmin(np.abs(frequencies - target))
            score += magnitude[index] / np.sqrt(harmonic)

        if score > best_score:
            best_score = score
            best_frequency = candidate_frequency

    return best_frequency

def frequency_to_note(frequency):
    """Convert a positive frequency into an equal-tempered note."""
    if frequency <= 0:
        return "Unknown", 0.0

    midi = int(round(69 + 12 * np.log2(frequency / 440.0)))

    note_names = [
        "C", "C#", "D", "D#", "E", "F",
        "F#", "G", "G#", "A", "A#", "B"
    ]

    note = note_names[midi % 12]
    octave = midi // 12 - 1

    reference = 440.0 * 2 ** ((midi - 69) / 12)
    cents = 1200 * np.log2(frequency / reference)

    return f"{note}{octave}", cents


def plot_results(audio, sr, frequencies, magnitude, estimated_frequency,harmonic_frequency=None):
    """Plot the waveform and FFT spectrum."""
    time = np.arange(len(audio)) / sr

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    axes[0].plot(time, audio)
    axes[0].set_title("Recorded Audio — Time Domain")
    axes[0].set_xlabel("Time (seconds)")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(frequencies, magnitude)
    axes[1].axvline(
        estimated_frequency,
        linestyle="--",
        label=f"Strongest peak: {estimated_frequency:.2f} Hz"
    )
    if harmonic_frequency is not None:
        axes[1].axvline(
        harmonic_frequency,
        color="green",
        linestyle=":",
        label=f"Harmonic estimate: {harmonic_frequency:.2f} Hz"
    )
    axes[1].set_title("FFT Magnitude Spectrum")
    axes[1].set_xlabel("Frequency (Hz)")
    axes[1].set_ylabel("Magnitude")
    axes[1].set_xlim(0, min(2000, sr / 2))
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def main():
    print("\n=== PitchLab ===")
    print("1. Test with a known 440 Hz signal")
    print("2. Analyze a WAV recording")
    print("3. Test harmonic-aware detection")
    print("4. Compare strongest peak vs harmonic-aware detection")
    
    choice = input("Choose : ").strip()

    if choice == "1":
        audio, sr = generate_test_signal(440)
        reference_frequency = 440.0

    elif choice == "2":
        filename = input("Enter WAV filename/path: ").strip()
        audio, sr = load_audio(filename)
        reference_frequency = None
    elif choice == "3":
        audio, sr = generate_harmonic_signal(220)
        reference_frequency = 220.0
    elif choice == "4":
        run_harmonic_experiment()
        return
    else:
        print("Invalid choice.")
        return

    frequencies, magnitude, estimated = analyze_fft(audio, sr)
    harmonic_estimated = estimate_fundamental(frequencies, magnitude)
    harmonic_note, harmonic_cents = frequency_to_note(harmonic_estimated)

    print(f"Strongest FFT peak: {estimated:.2f} Hz")
    print(f"Strongest-peak note: {frequency_to_note(estimated)[0]}")
    print(f"Harmonic-aware estimate: {harmonic_estimated:.2f} Hz")
    print(f"Harmonic-aware note: {harmonic_note}")
    note, cents = frequency_to_note(estimated)

    print(f"\nSample rate: {sr} Hz")
    print(f"Estimated strongest peak: {estimated:.2f} Hz")
    print(f"Detected note: {note}")
    print(f"Offset from nearest note: {cents:+.2f} cents")

    if reference_frequency is not None:
        print(f"Expected frequency: {reference_frequency:.2f} Hz")
        print(f"Absolute frequency error: "
              f"{abs(estimated - reference_frequency):.2f} Hz")

    plot_results(
        audio, sr, frequencies, magnitude,
        estimated,
        harmonic_estimated if choice == "3" else None
    )

if __name__ == "__main__":
    main()
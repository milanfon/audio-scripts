import numpy as np
import sounddevice as sd

def generate_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave

def play_sine_wave(frequency, duration, sample_rate=44100, output_device=None):
    wave = generate_sine_wave(frequency, duration, sample_rate)
                                                                                        
    if output_device is not None:
        sd.default.device = output_device
                                
    sd.play(wave, samplerate=sample_rate)
    sd.wait()  # Wait until the sound is finished

if __name__ == "__main__":
    frequency = 1000  # Frequency in Hz
    duration = 5      # Duration in seconds
    print("Available audio devices:")
    print(sd.query_devices())
    play_sine_wave(frequency, duration)

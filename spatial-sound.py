import numpy as np
import sounddevice as sd
import time
import threading
import sys
import csv

last_measured_level = None
measured_values = []

def generate_sine_wave(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave

def play_sine_wave(frequency, duration, sample_rate=44100, output_device=None):
    wave = generate_sine_wave(frequency, duration, sample_rate)
                                                                                        
    if output_device is not None:
        sd.default.device = output_device
                                
    sd.play(wave, samplerate=sample_rate)
    sd.wait()  

def get_level(data, reference=0.00002):     # The reference value is important
    rms_level = np.sqrt(np.mean(np.square(data)))
    if rms_level > 0:
        return 20 * np.log10(rms_level / reference)
    else:
        return -np.inf

def monitor_input(interval=0.1, duration=5, sample_rate=44100):
    global last_measured_level
    print("Monitor input audio levels...")
    with sd.InputStream(samplerate=sample_rate, channels=1) as stream:
        start_time = time.time()
        while time.time() - start_time < duration:
            data, _ = stream.read(int(sample_rate * interval))
            rms_level = get_level(data)
            last_measured_level = rms_level
            sys.stdout.write(f"\rInput level: {rms_level:.2f} dB(A)")
            sys.stdout.flush()
            time.sleep(interval)

if __name__ == "__main__":
    frequency = 500  
    duration = 3      

    print("Available audio devices:")
    print(sd.query_devices())

    num_segments = 8

    for segment in range(1, num_segments + 1):
        input(f"\nPosition {segment}/{num_segments}: Press Enter to start measurement.")
        last_measured_level = None

        wave_thread = threading.Thread(target=play_sine_wave, args=(frequency, duration))
        monitor_thread = threading.Thread(target=monitor_input, kwargs={"duration": duration})

        wave_thread.start()
        monitor_thread.start()

        wave_thread.join()
        monitor_thread.join()

        if last_measured_level is not None:
            measured_values.append((segment, last_measured_level))
            print(f"\nMeasured value at position {segment}: {last_measured_level:.2f} dB(A)")
        else:
            print(f"No measurement recorded at position {segment}.")

    csv_filename = "measurements.csv"
    with open(csv_filename, mode="w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Position', 'Measured Level (dB(A))'])
        for segment, level in measured_values:
            csv_writer.writerow([segment, f"{level:.2f}"])

    print(f"\nAll measurements completed. Results saved to {csv_filename}")

    print("Finished!")

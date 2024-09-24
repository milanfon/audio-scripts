import numpy as np
import sounddevice as sd
import time
import threading

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
    print("Monitor input audio levels...")
    with sd.InputStream(samplerate=sample_rate, channels=1) as stream:
        start_time = time.time()
        while time.time() - start_time < duration:
            data, _ = stream.read(int(sample_rate * interval))
            rms_level = get_level(data)
            print(f"Input level: {rms_level:.2f} dB(A)")
            time.sleep(interval)

if __name__ == "__main__":
    frequency = 500  
    duration = 10      

    print("Available audio devices:")
    print(sd.query_devices())

    wave_thread = threading.Thread(target=play_sine_wave, args=(frequency, duration))
    monitor_thread = threading.Thread(target=monitor_input, kwargs={"duration": duration})

    wave_thread.start()
    monitor_thread.start()

    wave_thread.join()
    monitor_thread.join()

    print("Finished!")

import numpy as np
import librosa
import simpleaudio
import time
import lib.beat as beat

"""
Play the desired audio song and print the beats in real time.

The beats are divided into 5 frequency bands:
- Sub (0 - 60Hz)
- Low (60 - 300Hz)
- Mid (300 - 3kHz)
- High Mid (3k - 6kHz)
- High (6k - 20kHz)

The "Combi" beats represent a combination of the beats in the sub and low frequencies.
"""

# Converts an audio signal into the int16 format
def audioToInt(audio):
    return (audio * (32767 / np.max(np.abs(audio)))).astype(np.int16)

song = 'song.mp3'

# Load the song from a mp3 file
y, sr = librosa.load(song)

# Detect the beats
beat_times_combi = beat.detect_combi_beats(y, sr)
sub_times = beat.detect_beats(y, sr, freq_range='sub')
low_times = beat.detect_beats(y, sr, freq_range='low')
mid_times = beat.detect_beats(y, sr, freq_range='mid')
high_mid_times = beat.detect_beats(y, sr, freq_range='high_mid')
high_times = beat.detect_beats(y, sr, freq_range='high')
beats = [
    sub_times,
    low_times,
    mid_times,
    high_mid_times,
    high_times
]

# Play the audio
a = simpleaudio.play_buffer(audioToInt(y), 1, 2, sr)
start_time = time.time()

# Print the estimated BPM (not really accurate)
print(f"Estimated BPM = {len(beat_times_combi) / (len(y) / sr) * 60}\n")

print("        |  S   L   M   H   H   B ")
print("        |  u   o   i   i   i   e ")
print("        |  b   w   d   g   g   a ")
print("        |              h   h   t ")
print("        |                        ")
print("        |              M         ")
print("        |              i         ")
print("  time  |              d         ")
print("--------+------------------------")

# Sync the beats
beat_indices = [0, 0, 0, 0, 0]
combi_beat_index = 0
while a.is_playing():
    time_since_start = time.time() - start_time
    
    print(" {0: 6.2f} | ".format(time_since_start), end=' ')

    for i, beat_times in enumerate(beats):
        if beat_indices[i] < len(beat_times) and time_since_start >= beat_times[beat_indices[i]]:
            print("o", end='   ')
            beat_indices[i] += 1
        else:
            print(" ", end='   ')

    if combi_beat_index < len(beat_times_combi) and time_since_start >= beat_times_combi[combi_beat_index]:
        # print(f"\033[1mCombi {time_since_start}\033[0m")
        print("\033[31m\033[1mo\033[0m", end='   ')
        combi_beat_index += 1
    else:
        print(" ", end='   ')

    print()

    time.sleep(0.1) 
    # 0.1 => 10 PPS     (Prints Per Second)
    # 0.05 => 20 PPS
    # 0.02 => 50 PPS
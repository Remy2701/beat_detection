import librosa
import lib.beat as beat

"""
Detect the beats in a desired song (using the sub and low frequency bands).
"""

path = 'song.mp3'

# Load the song from a mp3 file
y, sr = librosa.load(path)

# Detect the beats
beats = beat.detect_combi_beats(y, sr)
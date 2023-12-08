# Beat Detection Algorithm (Python)
A beat detection algorithm written in python.

Documentation is available in the [doc](doc) folder with an [explanation](doc/algorithm.md) of the algorithm.

## Usage
```python
import librosa
import lib.beat as beat

# Load the song from a mp3 file
y, sr = librosa.load('song.mp3')

# Detects the beat in the sub and low frequencies
beats = beat.detect_combi_beats(y, sr)
```

A More complex is also available [here](synced.py).
This example syncs the beats with the audio and plays the song.

## Libraries used

| Library     | Module  | Description               |
| ----------- | ------- | ------------------------- |
| scipy       | src     | Used for filtering        |
| numpy       | src     | Used for array operations |
| librosa     | example | Used to load the song     |
| simpleaudio | example | Used to play the audio    |
| time        | example | Used to sync the beats    |
| matplotlib  | doc     | Used to plot the results  |

## References
- [Beat Detction Algorithm (part 1) by Marco Ziccardi](https://mziccard.me/2015/05/28/beats-detection-algorithms-1/)
- [Music Onset Detection by Ruohua Zhou and Josh D Reiss](http://eecs.qmul.ac.uk/~josh/documents/2010/Zhou%20Reiss%20-%20Music%20Onset%20Detection%202010.pdf)
- [Music Instruction Frequency Cheatsheet](https://www.sweetwater.com/insync/music-instrument-frequency-cheatsheet/)
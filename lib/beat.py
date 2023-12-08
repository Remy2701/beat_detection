import numpy as np
import lib.filters as filters

def _create_blocks(
    y: np.ndarray, 
    block_size: int = 1024
) -> np.ndarray:
    """
    Divides the signal into blocks.

    Parameters
    ----------
    y : np.ndarray
        The signal to divide into blocks.   
    block_size : int, optional
        The size of each block, by default 1024.

    Returns
    -------
    np.ndarray
        The blocks of the signal.
    """

    return np.array_split(y, len(y) / (block_size - 1))

def _calculate_energy(
    blocks: np.ndarray,
) -> np.ndarray:
    """
    Computes the energy of each block.

    Parameters
    ----------
    blocks : np.ndarray
        The blocks of the signal.
    
    Returns
    -------
    np.ndarray
        The energy of each block.

    Notes
    -----
    The energy of a block is the sum of the squares of the values in the block.
    """

    return [np.sum(block**2) for block in blocks]

def _moving_mean_single(
    energy: np.ndarray, 
    i: int, 
    window_size: int = 43
) -> float:
    """
    Compute the moving average of the energy for a single block.

    Parameters
    ----------
    energy : np.ndarray
        The energy of each block.
    i : int
        The index of the block to compute the moving average for.
    window_size : int, optional
        The size of the window to use, by default 43.
    
    Returns
    -------
    float
        The moving average of the energy for the block.
    """

    value = np.mean(energy[max(0, i - window_size):(i + 1)])
    return np.nan_to_num(value, 0)

def _moving_mean(
    energy: np.ndarray,
    window_size: int = 43
) -> np.ndarray:
    """
    Compute the moving average of the energy of each block.

    Parameters
    ----------
    energy : np.ndarray
        The energy of each block.
    window_size : int, optional
        The size of the window to use, by default 43.
    
    Returns
    -------
    np.ndarray
        The moving average of the energy of each block.

    See Also
    --------
    _moving_mean_single : Compute the moving average of the energy for a single block.
    """
    return np.array([_moving_mean_single(energy, i, window_size) for i in range(len(energy))])

def _variance_single(
    energy: np.ndarray, 
    i: int
) -> float:
    """
    Compute the variance of the energy for a single block.

    Parameters
    ----------
    energy : np.ndarray
        The energy of each block.
    i : int
        The index of the block to compute the variance for.

    Returns
    -------
    float
        The variance of the energy for the block.

    Notes
    -----
    The variance of a block is the difference between the energy of the current block and the energy of the previous 
    block.
    """

    if i == 0:
        return energy[i]
    else:
        return max(0, (energy[i - 1] - energy[i]))
    
def _variance(
    energy: np.ndarray
) -> np.ndarray:
    """
    Compute the variance of the energy of each block.

    Parameters
    ----------
    energy : np.ndarray
        The energy of each block.
    
    Returns
    -------
    np.ndarray
        The variance of the energy of each block.

    See Also
    --------
    _variance_single : Compute the variance of the energy for a single block.
    """

    return np.array([_variance_single(energy, i) for i in range(len(energy))])

def _is_beat_single(
    variance: np.ndarray, 
    avg: np.ndarray, 
    i: int
) -> float:
    """
    Detect whether a single block is a beat.

    Parameters
    ----------
    variance : np.ndarray
        The energy variance of each block.
    avg : np.ndarray
        The moving average of the energy of each block.
    i : int
        The index of the block to detect the beat for.

    Returns
    -------
    float
        Whether the block is a beat (1.0 represent a beat and 0.0 no beat).
    """

    if variance[i] > avg[i] and (i == 0 or variance[i - 1] < avg[i - 1]):
        return 1
    else: 
        return 0
    
def _detect_beats(
    variance: np.ndarray,
    avg: np.ndarray
) -> np.ndarray:
    """
    Detect the beats in the signal for each blocks.

    Parameters
    ----------
    variance : np.ndarray
        The energy variance of each block.
    avg : np.ndarray
        The moving average of the energy of each block.

    Returns
    -------
    np.ndarray
        The beats in the signal for each blocks.

    See Also
    --------
    _is_beat_single : Detect whether a single block is a beat.
    """

    return np.array([_is_beat_single(variance, avg, i) for i in range(len(variance))])

def _correct_beats_single(
    beats: np.ndarray, 
    i: int,
    sr: int,
    max_bpm = 400,
    block_size = 1024
) -> float:
    """
    Correct the beats for a single block based on the given bpm.

    Parameters
    ----------
    beats : np.ndarray
        The beats in the signal for each blocks.
    i : int
        The index of the block to correct the beat for.
    sr : int
        The sample rate of the signal.
    max_bpm : int, optional
        The maximum bpm to use, by default 400.
    block_size : int, optional
        The size of each block, by default 1024.

    Returns
    -------
    float
        The corrected beat for the block (1.0 represent a beat and 0.0 not a beat).
    """

    min_block_distance = (60 / max_bpm) * sr / block_size
    if beats[i] == 1:
        for j in range(i - int(np.floor(min_block_distance)), i):
            if beats[j] == 1:
                return 0
    return beats[i]

def _correct_beats(
    beats: np.ndarray,
    sr: int,
    max_bpm = 400,
    block_size = 1024
) -> np.ndarray:
    """
    Correct the beat for each block based on the given bpm.

    Parameters
    ----------
    beats : np.ndarray
        The beats in the signal for each blocks.
    sr : int
        The sample rate of the signal.
    max_bpm : int, optional
        The maximum bpm to use, by default 400.
    block_size : int, optional
        The size of each block, by default 1024.

    Returns
    -------
    np.ndarray
        The corrected beats in the signal for each blocks.

    See Also
    --------
    _correct_beats_single : Correct the beats for a single block based on the given bpm.
    """

    return np.array([_correct_beats_single(beats, i, sr, max_bpm, block_size) for i in range(len(beats))])

def _correct_beats_single_weighted(
    beats: np.ndarray, 
    i: int,
    sr: int,
    max_bpm = 400,
    block_size = 1024
) -> float:
    """
    Correct the beats for a single block based on the given bpm with a weighted approach.
    A more important beat will have a value of 2.0 (instead of the traditional 1.0).

    Parameters
    ----------
    beats : np.ndarray
        The beats in the signal for each blocks.
    i : int
        The index of the block to correct the beat for.
    sr : int
        The sample rate of the signal.
    max_bpm : int, optional
        The maximum bpm to use, by default 400.

    Returns
    -------
    float
        The corrected beat for the block (1.0 represent a beat and 0.0 not a beat).
    """

    min_block_distance = (60 / max_bpm) * sr / block_size
    if beats[i] == 1:
        for j in range(i - int(np.floor(min_block_distance)), i):
            if beats[j] >= 1:
                return 0
        for j in range(i + 1, i + int(np.floor(min_block_distance))):
            if beats[j] == 2:
                return 0
    elif beats[i] == 2:
        for j in range(i - int(np.floor(min_block_distance)), i):
            if beats[j] == 2:
                return 0
        for j in range(i + 1, i + int(np.floor(min_block_distance))):
            if beats[j] == 2:
                return 0
    return min(1, beats[i])

def _correct_beats_weighted(
    beats: np.ndarray,
    sr: int,
    max_bpm = 400,
    block_size = 1024
) -> np.ndarray:
    """
    Correct the beat for each block based on the given bpm with a weighted approach.
    A more important beat will have a value of 2.0 (instead of the traditional 1.0).

    Parameters
    ----------
    beats : np.ndarray
        The beats in the signal for each blocks.
    sr : int
        The sample rate of the signal.
    max_bpm : int, optional
        The maximum bpm to use, by default 400.
    block_size : int, optional
        The size of each block, by default 1024.

    Returns
    -------
    np.ndarray
        The corrected beats in the signal for each blocks.

    See Also
    --------
    _correct_beats_single_weighted : Correct the beats for a single block based on the given bpm with a weighted approach.
    """

    return np.array([_correct_beats_single_weighted(beats, i, sr, max_bpm, block_size) for i in range(len(beats))])

def _beat_to_time(
    beats: np.ndarray,
    block_size: int = 1024,
    sr: int = 44100
) -> np.ndarray:
    """
    Converts the beat of each block into a list of time (in seconds) where a beat has been detected.

    Parameters
    ----------
    beats : np.ndarray
        The beats in the signal for each blocks.
    block_size : int, optional
        The size of each block, by default 1024.
    sr : int, optional
        The sample rate of the signal, by default 44100.

    Returns
    -------
    np.ndarray
        The list of time (in seconds) where a beat has been detected.
    """

    beat_times = []
    for i, beat in enumerate(beats):
        if beat == 1:
            beat_times.append(i * block_size / sr)
    return np.array(beat_times)

def _detect_all_beats(
    y: np.ndarray,
    sr: int = 44100,
    block_size: int = 1024,
    window_size: int = 43,
    max_bpm = 400,
    freq_range = 'sub'
) -> np.ndarray:
    """
    Detect all the beats in the choosen frequency range of a given signal.

    Parameters
    ----------
    y : np.ndarray
        The signal to detect the beats from.
    sr : int, optional
        The sample rate of the signal, by default 44100.
    block_size : int, optional
        The size of each block, by default 1024.
    window_size : int, optional
        The size of the window to use, by default 43.
    max_bpm : int, optional
        The maximum bpm to use, by default 400.
    freq_range : str, optional
        The frequency range to use, by default 'sub'.
        One of ['sub', 'low', 'mid', 'high_mid', 'high'].
    
    Returns
    -------
    np.ndarray
        The beats in the signal for each blocks.
    """

    # Filter the signal
    if freq_range == 'sub':
        y = filters.sub_filter(sr, y)
    elif freq_range == 'low':
        y = filters.low_filter(sr, y)
    elif freq_range == 'mid':
        y = filters.midrange_filter(sr, y)
    elif freq_range == 'high_mid':
        y = filters.high_midrange_filter(sr, y)
    elif freq_range == 'high':
        y = filters.high_filter(sr, y)

    # Split the signal into blocks
    blocks = _create_blocks(y, block_size)

    # Compute the fft of each block
    energy = _calculate_energy(blocks)

    # Compute the moving average of the energy
    energy_block_avg = _moving_mean(energy, window_size)

    # Compute the variance of the energy
    energy_block_variance = _variance(energy)

    # Detect the beats in the signal
    beats = _detect_beats(energy_block_variance, energy_block_avg)

    # Correct the beats
    beats = _correct_beats(beats, sr, max_bpm, block_size)

    # Ignore the 1st window
    for i in range(0, window_size):
        beats[i] = 0

    return beats

def detect_beats(
    y: np.ndarray,
    sr: int = 44100,
    block_size: int = 1024,
    window_size: int = 43,
    max_bpm = 400,
    freq_range = 'sub'
) -> np.ndarray:
    """
    Detect all the beats in the choosen frequency range of a given signal.

    Parameters
    ----------
    y : np.ndarray
        The signal to detect the beats from.
    sr : int, optional
        The sample rate of the signal, by default 44100.
    block_size : int, optional
        The size of each block, by default 1024.
    window_size : int, optional
        The size of the window to use, by default 43.
    max_bpm : int, optional
        The maximum bpm to use, by default 400.
    freq_range : str, optional
        The frequency range to use, by default 'sub'.
        One of ['sub', 'low', 'mid', 'high_mid', 'high'].
    
    Returns
    -------
    np.ndarray
        The time at which each beat occur.
    """

    beats = _detect_all_beats(y, sr, block_size, window_size, max_bpm, freq_range)
    
    return _beat_to_time(beats, block_size, sr)

def detect_combi_beats(
    y: np.ndarray,
    sr: int = 44100,
    block_size: int = 1024,
    window_size: int = 43,
    max_bpm = 400
) -> np.ndarray:
    """
    Detect all the beats in a given signal (using the sub and low frequencies).

    Parameters
    ----------
    y : np.ndarray
        The signal to detect the beats from.
    sr : int, optional
        The sample rate of the signal, by default 44100.
    block_size : int, optional
        The size of each block, by default 1024.
    window_size : int, optional
        The size of the window to use, by default 43.
    max_bpm : int, optional
        The maximum bpm to use, by default 400.

    Returns
    -------
    np.ndarray
        The time at which each beat occur.
    """

    sub_beats = _detect_all_beats(y, sr, block_size, window_size, max_bpm, 'sub')
    low_beats = _detect_all_beats(y, sr, block_size, window_size, max_bpm, 'low')

    beats = np.zeros(len(sub_beats))
    for i in range(len(low_beats)):
        if sub_beats[i] == 1:
            beats[i] = 2
        elif low_beats[i] == 1:
            beats[i] = 1

    beats = _correct_beats_weighted(beats, sr, max_bpm, block_size)

    return _beat_to_time(beats, block_size, sr)
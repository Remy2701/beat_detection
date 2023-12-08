import scipy.signal as signal
import numpy as np

def create_sub_filter(sr: int):
    """
    Create a filter to keep only the sub frequencies (0 - 60Hz)

    Parameters
    ----------
    sr : int
        The sample rate of the filter.

    Returns
    -------
    b, a: np.ndarray
        The numerator (b), and denominator (a) of the filter.
    """

    order = 5
    cutOff = 60.0
    return signal.butter(order, cutOff, fs=sr, btype='low', analog=False)

def sub_filter(
    sr: int, 
    y: np.ndarray
) -> np.ndarray:
    """
    Apply the sub filter to the signal (Keeping only the sub frequencies [0 - 60Hz])

    Parameters
    ----------
    sr : int
        The sample rate of the filter.
    y : np.ndarray
        The signal to filter.
    
    Returns
    -------
    np.ndarray
        The filtered signal.

    See Also
    --------
    create_sub_filter : Create the sub filter.
    """

    # Create the filter
    b, a = create_sub_filter(sr)

    # Apply the filter
    return signal.lfilter(b, a, y)

def create_low_filter(sr: int):
    """
    Create a filter to keep only the low frequencies (60 - 300Hz)

    Parameters
    ----------
    sr : int
        The sample rate of the filter.

    Returns
    -------
    b, a: np.ndarray
        The numerator (b), and denominator (a) of the filter.
    """

    order = 3
    cutOff1 = 60.0
    cutOff2 = 300.0
    return signal.butter(order, [cutOff1, cutOff2], fs=sr, btype='bandpass', analog=False)

def low_filter(
    sr: int, 
    y: np.ndarray
) -> np.ndarray:
    """
    Apply the low filter to the signal (Keeping only the low frequencies [60 - 300Hz])

    Parameters
    ----------
    sr : int
        The sample rate of the filter.
    y : np.ndarray
        The signal to filter.
    
    Returns
    -------
    np.ndarray
        The filtered signal.

    See Also
    --------
    create_low_filter : Create the low filter.
    """

    # Create the filter
    b, a = create_low_filter(sr)

    # Apply the filter
    return signal.lfilter(b, a, y)

def create_midrange_filter(sr: int):
    """
    Create a filter to keep only the midrange frequencies (300 - 2kHz)

    Parameters
    ----------
    sr : int
        The sample rate of the filter.

    Returns
    -------
    b, a: np.ndarray
        The numerator (b), and denominator (a) of the filter.
    """

    order = 5
    cutOff1 = 300.0
    cutOff2 = 2000.0
    return signal.butter(order, [cutOff1, cutOff2], fs=sr, btype='bandpass', analog=False)

def midrange_filter(
    sr: int, 
    y: np.ndarray
) -> np.ndarray:
    """
    Apply the midrange filter to the signal (Keeping only the midrange frequencies [300 - 2kHz])

    Parameters
    ----------
    sr : int
        The sample rate of the filter.
    y : np.ndarray
        The signal to filter.
    
    Returns
    -------
    np.ndarray
        The filtered signal.

    See Also
    --------
    create_midrange_filter : Create the midrange filter.
    """

    # Create the filter
    b, a = create_midrange_filter(sr)

    # Apply the filter
    return signal.lfilter(b, a, y)

def create_high_midrange_filter(sr: int):
    """
    Create a filter to keep only the high midrange frequencies (2k - 6kHz)

    Parameters
    ----------
    sr : int
        The sample rate of the filter.

    Returns
    -------
    b, a: np.ndarray
        The numerator (b), and denominator (a) of the filter.
    """

    order = 5
    cutOff1 = 2000.0
    cutOff2 = 6000.0
    return signal.butter(order, [cutOff1, cutOff2], fs=sr, btype='bandpass', analog=False)

def high_midrange_filter(
    sr: int, 
    y: np.ndarray
) -> np.ndarray:
    """
    Apply the high midrange filter to the signal (Keeping only the high midrange frequencies [2k - 6kHz])

    Parameters
    ----------
    sr : int
        The sample rate of the filter.
    y : np.ndarray
        The signal to filter.
    
    Returns
    -------
    np.ndarray
        The filtered signal.

    See Also
    --------
    create_high_midrange_filter : Create the high midrange filter.
    """

    # Create the filter
    b, a = create_high_midrange_filter(sr)

    # Apply the filter
    return signal.lfilter(b, a, y)

def create_high_filter(sr: int):
    """
    Create a filter to keep only the high frequencies (6k - 10kHz)

    Parameters
    ----------
    sr : int
        The sample rate of the filter.

    Returns
    -------
    b, a: np.ndarray
        The numerator (b), and denominator (a) of the filter.
    """

    order = 5
    cutOff1 = 6000.0
    cutOff2 = 10000.0
    return signal.butter(order, [cutOff1, cutOff2], fs=sr, btype='bandpass', analog=False)

def high_filter(
    sr: int, 
    y: np.ndarray
) -> np.ndarray:
    """
    Apply the high filter to the signal (Keeping only the high frequencies [6k - 10kHz])

    Parameters
    ----------
    sr : int
        The sample rate of the filter.
    y : np.ndarray
        The signal to filter.
    
    Returns
    -------
    np.ndarray
        The filtered signal.

    See Also
    --------
    create_high_filter : Create the high filter.
    """

    # Create the filter
    b, a = create_high_filter(sr)

    # Apply the filter
    return signal.lfilter(b, a, y)

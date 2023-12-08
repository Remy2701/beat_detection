import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

def _plot_filter_response(
    a: np.ndarray,
    b: np.ndarray,
    sr: int,
    use_log_scale: bool = True,
):
    """
    Plots the frequency response of the filter.

    Parameters
    ----------
    a : np.ndarray
        The denominator of the filter.
    b : np.ndarray
        The numerator of the filter.
    sr : int
        The sample rate of the filter.
    use_log_scale : bool, optional
        Whether to use a log scale for the y-axis, by default True.
    """

    # Compute the frequency response of the filter
    w, h = signal.freqz(b, a, fs=sr, worN=8000)

    # Plot the frequency response of the filter
    if use_log_scale:
        plt.plot(w, 20 * np.log10(np.abs(h)))
    else:
        plt.plot(w, np.abs(h))

def _apply_filter_response_settings(title: str, use_log_scale: bool = True):
    if use_log_scale:
        plt.xscale('log')
    else:
        plt.xscale('linear')
    plt.title(title)
    plt.ylabel("Amplitude (dB)")
    plt.xlabel("Frequency (Hz)")
    plt.margins(0, 0.1)
    plt.grid(which='both', axis='both')
    plt.show()

def plot_filter_response(
    a: np.ndarray,
    b: np.ndarray,
    sr: int,
    use_log_scale: bool = True,
    title: str = "Filter"
):
    """
    Plots the frequency response of the filter.

    Parameters
    ----------
    a : np.ndarray
        The denominator of the filter.
    b : np.ndarray
        The numerator of the filter.
    sr : int
        The sample rate of the filter.
    use_log_scale : bool, optional
        Whether to use a log scale for the y-axis, by default True.
    title : str, optional
        The title of the plot, by default "Filter".
    """

    # Plot the frequency response of the filter
    _plot_filter_response(a, b, sr, use_log_scale)

    # Apply additional settings
    _apply_filter_response_settings(title, use_log_scale)

def plot_all_filter_response(
    a: np.ndarray,
    b: np.ndarray,
    sr: int,
    use_log_scale: bool = True,
    title: str = "Filters"
):
    """
    Plots the frequency response of all the filters.

    Parameters
    ----------
    a : np.ndarray
        The denominator of the filters.
    b : np.ndarray
        The numerator of the filters.
    sr : int
        The sample rate of the filters.
    use_log_scale : bool, optional
        Whether to use a log scale for the y-axis, by default True.
    title : str, optional
        The title of the plot, by default "Filters".
    """

    for i in range(len(a)):
        _plot_filter_response(a[i], b[i], sr, use_log_scale)

    _apply_filter_response_settings(title, use_log_scale)
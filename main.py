
from numpy import *
from ipywidgets import *
import scipy.io.wavfile
from scipy import signal
import sys

import warnings

warnings.filterwarnings("ignore")
# kilka plików miało błędne nagłówki o długości zawartych danych, 
# skrypt zczytywał je poprawnie jednak wywalał warning na konsoli


minmax_mezczyzna = [85, 180]
minmax_kobieta = [165, 255]


# (*) <-- w tych miejscach wykonują się części opisane w sprawozdaniu


def gender_detection(inFile):
    # (1)
    w, sig = scipy.io.wavfile.read(inFile)

    # (2)
    n_kanalow = len(sig.shape)
    if n_kanalow == 2:
        sig = array([s[0] for s in sig])

    N = len(sig)
    LP = N / w

    # (3)
    partLen = N // (int(LP))
    parts = array([sig[i * partLen:(i + 1) * partLen] for i in range(int(LP))])

    # (4)
    # https://en.wikipedia.org/wiki/Window_function
    window = signal.windows.tukey(N // int(LP))
    parts_windowed = [part * window for part in parts]

    # (5)
    parts_fft = [abs(fft.fft(part)) for part in parts_windowed]

    # (6)
    adder = array([ones(N // int(LP))] * int(LP))
    for part_n in range(len(parts_fft)):
        for i in range(1, 6):
            for j in range(len(parts[part_n][::i])):
                adder[part_n][j] *= parts_fft[part_n][i * j]

    # (7)            
    summed_adder = adder.sum(axis=0)

    # (8)
    if (sum(summed_adder[minmax_mezczyzna[0]:minmax_mezczyzna[1]]) > sum(
            summed_adder[minmax_kobieta[0]:minmax_kobieta[1]])):
        decyzja = 'M'
    else:
        decyzja = 'K'

    return decyzja


if __name__ == "__main__":
    inFile = sys.argv[1]
    result = gender_detection(inFile)
    print(result)
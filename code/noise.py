import numpy as np
import matplotlib.pyplot as plt
from pycbc.filter.matchedfilter import matched_filter
from pycbc.waveform import get_td_waveform
import pycbc.psd
from scipy.ndimage import gaussian_filter
from scipy.ndimage import generic_filter1d
import pycbc.psd
import pycbc.psd
import pycbc.types
import pylab

delta_f = 1.0 / 10
length = int(2048 / delta_f)
f_low = 20.0

psd_LIGO = pycbc.psd.read.from_txt('AplusDesign.txt', length=length, delta_f=delta_f, low_freq_cutoff=f_low, is_asd_file=True)
psd_KAGRA = pycbc.psd.read.from_txt('kagra_80Mpc.txt', length=length, delta_f=delta_f, low_freq_cutoff=f_low, is_asd_file=True)
psd_Virgo1 = pycbc.psd.read.from_txt('avirgo_O5high_NEW.txt', length=length, delta_f=delta_f, low_freq_cutoff=f_low, is_asd_file=True)
psd_Virgo2 = pycbc.psd.read.from_txt('avirgo_O5low_NEW.txt', length=length, delta_f=delta_f, low_freq_cutoff=f_low, is_asd_file=True)

figure = plt.figure(figsize = (10, 5))
pylab.loglog(psd_LIGO.sample_frequencies, psd_LIGO, label='LIGO (350 Mpc)')
pylab.loglog(psd_Virgo1.sample_frequencies, psd_Virgo1, label='Virgo (275 Mpc)')
pylab.loglog(psd_KAGRA.sample_frequencies, psd_KAGRA, label='KAGRA (80 Mpc)')
#pylab.loglog(psd_Virgo2.sample_frequencies, psd_Virgo2 , label='Virgo (low noise)')
pylab.xlim(xmin=23, xmax=2000)
pylab.ylim(ymin=1e-48, ymax=5e-44)
pylab.xlabel(r'Frequency (Hz)', fontsize=18)
pylab.ylabel(r'PSD (Hz)', fontsize=18)
pylab.yticks(fontsize=14)
pylab.xticks(fontsize=14)
pylab.legend(fontsize=18)
pylab.xlabel('Hz')
pylab.savefig("noise.png")
pylab.show()

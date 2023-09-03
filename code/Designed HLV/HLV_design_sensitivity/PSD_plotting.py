#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[4]:


# Load PSD data
delta_f = 1.0 / 10
length = int(2048 / delta_f)
f_low = 10.0



# Load PSD data directly, no need for further squaring
"""
The "aLIGO_ZERO_DET_high_P_psd.txt" text file used in this code is downloaded from open-source available at the following GitHub link: 

https://github.com/lscsoft/bilby/blob/master/bilby/gw/detector/noise_curves/aLIGO_ZERO_DET_high_P_asd.txt
"""
psd_LIGO = pycbc.psd.read.from_txt('aLIGO_ZERO_DET_high_P_psd.txt', length=length, delta_f=delta_f, low_freq_cutoff=f_low, is_asd_file=True)

"""
The "AdV_psd.txt" text file used in this code is downloaded from open-source available at the following GitHub link: 

https://github.com/lscsoft/bilby/blob/master/bilby/gw/detector/noise_curves/AdV_psd.txt
"""
psd_Virgo = pycbc.psd.read.from_txt('AdV_psd.txt', length=length, delta_f=delta_f, low_freq_cutoff=f_low, is_asd_file=True)

# Create the plot
figure = plt.figure(figsize=(10, 5))
pylab.loglog(psd_LIGO.sample_frequencies, np.sqrt(psd_LIGO), label='LIGO')
pylab.loglog(psd_Virgo.sample_frequencies, np.sqrt(psd_Virgo), label='Virgo')
pylab.xlim(xmin=23, xmax=2000)
pylab.ylim(ymin=1e-50, ymax=1e-30)  # Adjusted y-axis limits as per professor's feedback
pylab.xlabel(r'Frequency (Hz)', fontsize=18)
pylab.ylabel(r'PSD (Hz)', fontsize=18)
pylab.yticks(fontsize=14)
pylab.xticks(fontsize=14)
pylab.legend(fontsize=18)
pylab.title("Power Spectral Density of Noise in LIGO and Virgo Detectors", fontsize=20)

# Save and display the plot
pylab.savefig("noise.png")
pylab.show()


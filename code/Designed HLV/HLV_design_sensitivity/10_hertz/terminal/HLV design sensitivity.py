#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/bin/python
"""
Tutorial to demonstrate a new interferometer

We place a new instrument in Gingin, with an A+ sensitivity in a network of A+
interferometers at Hanford and Livingston
"""


# In[2]:


import numpy as np

import bilby
#import gwinc

# Set the duration and sampling frequency of the data segment that we're going
# to inject the signal into
duration = 4.
sampling_frequency = 2048.


# In[3]:


# Specify the output directory and the name of the simulation.
outdir = 'outdir'
label = 'next_genBBH'
bilby.core.utils.setup_logger(outdir=outdir, label=label)

# Set up a random seed for result reproducibility.  This is optional!
np.random.seed(88170232)

AdV_psd=np.loadtxt("AdV_psd.txt")
AdV_psd=AdV_psd[AdV_psd[:,0]>=10]

hl_psd=np.loadtxt("aLIGO_ZERO_DET_high_P_psd.txt")
hl_psd=hl_psd[hl_psd[:,0]>=10]


frequencies = np.logspace(0, 3, 1000)


# In[4]:


# Set up three other detectors at Hanford, Livingston and Virgo
interferometers = bilby.gw.detector.InterferometerList(['H1', 'L1','V1'])


# In[9]:


interferometers[0].power_spectral_density =        bilby.gw.detector.PowerSpectralDensity(
            frequency_array=hl_psd[:,0], psd_array=hl_psd[:,1])

interferometers[1].power_spectral_density =        bilby.gw.detector.PowerSpectralDensity(
            frequency_array=hl_psd[:,0], psd_array=hl_psd[:,1])
    
interferometers[2].power_spectral_density =        bilby.gw.detector.PowerSpectralDensity(
            frequency_array=AdV_psd[:,0], psd_array=AdV_psd[:,1])


# In[10]:


# Inject a gravitational-wave signal into the network
# as we're using a three-detector network of A+, we inject a GW150914-like
# signal at 4 Gpc
injection_parameters = dict(
   mass_1=36., mass_2=29., a_1=0.4, a_2=0.3, tilt_1=0.5, tilt_2=1.0,
   phi_12=1.7, phi_jl=0.3, luminosity_distance=2000., theta_jn=0.4, psi=2.659,
   phase=1.3, geocent_time=1502019943, ra=1.375, dec=-1.2108)
# date and time 2027-08-11T11:45:25


# In[11]:


# Fixed arguments passed into the source model
waveform_arguments = dict(waveform_approximant='IMRPhenomPv2',
                          reference_frequency=50.)

# Create the waveform_generator using a LAL BinaryBlackHole source function
waveform_generator = bilby.gw.WaveformGenerator(
    duration=duration, sampling_frequency=sampling_frequency,
    frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
    waveform_arguments=waveform_arguments)

start_time = injection_parameters['geocent_time'] + 2 - duration


# In[12]:


# inject the signal into the interferometers

for interferometer in interferometers:
    interferometer.set_strain_data_from_power_spectral_density(
        sampling_frequency=sampling_frequency, duration=duration, start_time=start_time)
    interferometer.inject_signal(
        parameters=injection_parameters, waveform_generator=waveform_generator)

    # plot the data for sanity
    signal = interferometer.get_detector_response(
        waveform_generator.frequency_domain_strain(), injection_parameters)
    interferometer.plot_data(signal=signal, outdir=outdir, label=label)


# In[13]:


priors = bilby.gw.prior.BBHPriorDict()
for key in ['a_1', 'a_2', 'tilt_1', 'tilt_2', 'phi_12', 'phi_jl', 'psi',
            'geocent_time']:
    priors[key] = injection_parameters[key]
   
priors['geocent_time'] = bilby.core.prior.Uniform(
    minimum=injection_parameters['geocent_time'] - 0.1,
    maximum=injection_parameters['geocent_time'] + 0.1,
    name='geocent_time', latex_label='$t_c$', unit='$s$')


# In[14]:


# Initialise the likelihood by passing in the interferometer data (IFOs)
# and the waveoform generator
likelihood = bilby.gw.GravitationalWaveTransient(
    interferometers=interferometers, waveform_generator=waveform_generator,
    time_marginalization=True, phase_marginalization=True,
    distance_marginalization=True, priors=priors)


# In[15]:


result = bilby.run_sampler(
    likelihood=likelihood, priors=priors, sampler='dynesty', npoints=2000,
    injection_parameters=injection_parameters, outdir=outdir,
    label=label, maxmcmc=1000, nlive=512, walks=100, n_checkpoint=5000, dlogz=0.2,
    conversion_function=bilby.gw.conversion.generate_all_bbh_parameters)

# make some plots of the outputs
result.plot_corner()


# In[ ]:





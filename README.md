# MCAL
MCAL is a python program that uses the pseudo equivalent widths (PEWs) of high-resolution spectral lines from the HARPS spectrograph to infer temperatures and metallicities of M-dwarf stars.

From the results of MCAL a paper was written and published in Astronomy and Astrophysics magazine entitled *Metallicity of M dwarfs. III. Planet-metallicity and planet-stellar mass correlations of the HARPS GTO M dwarf sample*.

url: <https://ui.adsabs.harvard.edu/abs/2013A%26A...551A..36N/abstract>

The latest version of MCAL is v. 4.1 and it is stored under the folder MCAL. 

This version of the software is described in the paper *Metallicity of M dwarfs. IV. A high-precision [Fe/H] and Teff technique from high-resolution optical spectra for M dwarfs*

url: <https://ui.adsabs.harvard.edu/abs/2014A%26A...568A.121N/abstract>

**Abstract**

**Aims:** In this work we develop a technique to obtain high precision determinations of both metallicity and effective temperature of M dwarfs in the optical.

**Methods:** A new method is presented that makes use of the information of 4104 lines in the 530-690 nm spectral region. It consists in the measurement of pseudo equivalent widths and their correlation with established scales of [Fe/H] and Teff.

**Results:** Our technique achieves a rms of 0.08 ± 0.01 for [Fe/H], 91 ± 13 K for Teff, and is valid in the (-0.85,0.26 dex), (2800, 4100 K), and (M0.0, M5.0) intervals for [Fe/H], Teff and spectral type respectively. We also calculated the RMSEV which estimates uncertainties of the order of 0.12 dex for the metallicity and of 293 K for the effective temperature. The technique has an activity limit and should only be used for stars with log LHα/Lbol< - 4.0.

## Code

The code produced for MCAL will be described here. All code was written in python 2.7.X. Feel free to upgrade it to 3.X! :)

Inside the folder MCAL we can find the following files:

* runallv4.py - script to run all the other programs. In the startup section one can choose to use FFT to filter high frequency noise, the file type of the input spectra (FITS or text file), and the name of the file with the full path of the spectra. The script also calculates the H index described by Gomes da Silva et al. (2011) and warns if the star is too active.

**NOTE:** Use the FFT filter at your own risk! The filter should be fine tuned manually, and one should not choose a frequency cut too far from the Nyquist frequency. Moreover, it does not work well for low SNR. Check the function fft_filterv2.py for details.

**NOTE 2** : The input spectra should always have a step of 0.01 A. If the step is different you need to interpolate the spectra before using this method.

**NOTE 3**: The spectral range of the technique is 5339-6907 A.

**NOTE 4**: The minimum recommended resolution of the spectra to use this method is R = 40.000, with a SNR of at least 25. The details regarding this constraints are given in Neves et al. (2014).

* fft_filterv2.py - The function that performs the FFT filtering of the spectra.

* int_calc_stars.py - function to calculate the pseudo EWs of the relevant lines. It uses lines.rdb as input. An output file, ew_out.npz, is also created. It takes 4-5 minutes per star to calculate the EWs on a 2010 i5 2.4 Ghz computer.

* mcalv3.npz - function that calculates the [Fe/H] and Teff of each star using the calibration matrix file coef_calv3.npz. The output will be displayed on the screen and can also be optionally saved to a file (check runallv4.py for details).

* stars.txt - Text file with the full path of the spectra. This file should have all the spectra files for analysis.

* Gl105B_S1D.fits and Gl849_S1D.fits are two HARPS spectra that can be used to demonstrate how the program works. Their full file names appear in the file stars.txt. One should remove them from stars.txt before calibrating new stars.

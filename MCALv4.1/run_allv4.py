###script to run all programs of the calibration sequentially###
###
###INPUT FILES: spectra files with 0.01 step, EWs
###OUTPUT FILES: FFT Filtered flux, [Fe/H] and Teff 

import pyfits as p
from pylab import *
from fft_filterv2 import fft_filter
from int_calc_stars import int_calc_stars
from mcalv3 import mcal

###startup###
star = ()
fft_f = 'yes' #'no' - disable fft_filtering; 'yes' - enable fft_filtering
file_type = 'fits' #'fits' - FITS file input; 'txt' - text file input 
star_file = 'stars.txt' #file with full star filenames
star = append(star,loadtxt(star_file,usecols=(0,),dtype='string',skiprows=1))

sample = star.size

###FILE TYPE

x,y = [],[]

if file_type == 'fits' :
    length,start,step =  [],[],[]
    for n in range(sample) :
	   
	   hdu = (p.open(star[n]))
	   length.append(hdu[0].header['NAXIS1']) ####length of the spectrum
	   start.append(hdu[0].header['CRVAL1']) ###starting point
	   step.append(hdu[0].header['CDELT1']) ###step of the spectrum
	   x.append(arange(length[n])*step[n]+start[n]) ###wavelength
	   y.append(hdu[0].data) ###flux

if file_type == 'txt' :
    for n in range(sample) :
	   
	   x.append(loadtxt(star_file[n],delimiter='\t',usecols=(0,),dtype='string',skiprows=0)) #change delimiter and skiprows as needed! 
##wavelength as first column 
	   y.append(loadtxt(star_file[n],delimiter='\t',usecols=(1,),dtype='string',skiprows=0)) #change delimiter and skiprows as needed! 
##flux as second column 

###FFT FILTERING

if fft_f == 'yes' : 
    print 'FFT filtering in progress...'
    yfft = fft_filter(y)
#    np.savez ('fft_filter.npz',x=x,y=y,yfft=yfft) #optional save to keeep the fft filtered flux

###CALCULATE EWs
###NOTE: The function int_calc_stars will have a file output called ew_out.npz that includes the EWs of the stars
if fft_f == 'yes' : int_ew = int_calc_stars(x,yfft)
if fft_f == 'no' : int_ew = int_calc_stars(x,y)

###CALCULATE corrected Halpha to obtain a measure of the activity
print 'Calculating Halpha activity index...'
ha,ha_rtest = (),()
aha =  1.8565921 #correction coefficients
bha = -0.0870908 #correction coefficients

for n in range(sample) : 

    hlc = max(find (x[n] <= 6562.01)) #limits to measure Halpha index
    hrc = min(find (x[n] >= 6563.61)) #limits to measure Halpha index
    hl1 = max(find (x[n] <= 6545.495)) #limits to measure Halpha index
    hl2 = min(find (x[n] >= 6556.245)) #limits to measure Halpha index
    hr1 = max(find (x[n] <= 6575.934)) #limits to measure Halpha index
    hr2 = min(find (x[n] >= 6584.684)) #limits to measure Halpha index
  
    ha_core = sum(y[n][hlc:hrc])
    href1 = sum(y[n][hl1:hl2])
    href2 = sum(y[n][hr1:hr2])
    ha_rtest = append(ha_rtest,ha_core/(href1+href2))
    ha = append(ha,ha_rtest[n]*aha+bha) #ha corrected
    if ha[n] >= 0.25 : print 'WARNING: the star',star[n],'may be too active to use this calibration. Halpha =',ha[n],'. Check the webpage or Neves (2014) for more details.'
    else : print 'No significant Halpha emission for star', star[n]



###CALCULATE [Fe/H] and Teff
###IF YOU WANT TO LOAD the EWs from the file 'ew_out.npz' saved by int_calc_stars uncomment the next line
#int_ew = np.load('ew_out.npz') #TO LOAD the EWs from the output file

feh,teff = mcal(int_ew)

###PRINT RESULTS
#outpar = open('parameters.rdb','w') #Optional line to use to print result on a file. 
#To use outpar you need to add '>> outpar' after the print commands
tam = star.dtype.itemsize
print 'star','\t','feh','\t','teff'
print '----','\t','---','\t','----'
for n in range(sample) :
    white = " "*(tam - len(star[n])) #CHANGE if needed
    print '%s\t%s%4.2f\t%i' %(star[n],white,feh[n],teff[n]) #CHANGE if needed

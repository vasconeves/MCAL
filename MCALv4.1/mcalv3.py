#import os
from pylab import *
from scipy import optimize
from scipy import integrate 
import time

close('all')

def mcal(int_ew) :
    """INPUT: array of peak to peak EWs for each star
    should be a nx4104 array!!! n = number of stars
    OUTPUT: [Fe/H] and Teff for each star """


###removing all possible nans from the EW file

    int_ew = nan_to_num(int_ew)


###loading the calibration matrix and errors

    file_cal = np.load('coef_calv3.npz') ###calibration matrix
    coef = file_cal['coef'] #tellurics exclusion
    e_total = file_cal['e_total'] #tellurics exclusion


####2nd part of the calibration: refit with weights

    z2 = int_ew

    fun2 = lambda a,xx2,yy2,zz2 : a[0] + a[1]*xx2+a[2]*yy2 + a[3]*zz2 #experiencia FICA ESTA
    err2 = lambda a,xx2,yy2,zz2,z2,erro : (z2 - fun2(a,xx2,yy2,zz2))*((1/erro**2)/(sum(1/erro**2))) #FICA ESTA

    xx2fit = coef[:,0]
    yy2fit = coef[:,1]
    zz2fit = coef[:,2]

    a = array([0,0,0,3500])

    fit2 = []
    coef2 = []
    residual2 = []
    efitfeh = []
    efitteff = []
    r2fit2 = []

    for n in range(len(z2)) : 

	   fit2.append(optimize.leastsq (err2,a,args=(xx2fit,yy2fit,zz2fit,z2[n],e_total),full_output=1)) # optimize.leastsq
	   
	   rss = sum(fit2[n][2]['fvec']**2)/(z2[n].size-4)
	   efitfeh = append(efitfeh,sqrt(diag(rss*fit2[n][1])[2]))
	   efitteff = append(efitteff,sqrt(diag(rss*fit2[n][1])[3]))
	   coef2.append(fit2[n][0])

    corr_fit = ()
    feh_fit = ()
    teff_fit = ()
    feh_fit2 = ()
    teff_fit2 = ()

    for n in range (len(z2)): 
	   feh_fit = append(feh_fit,coef2[n][2])
	   teff_fit = append(teff_fit,coef2[n][3])

    return feh_fit,teff_fit


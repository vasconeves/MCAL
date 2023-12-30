import os
from pylab import *
from scipy import optimize
from scipy import integrate 
import time

#star0=loadtxt('../temp5.rdb',delimiter='\t',usecols=(0,),dtype='string',skiprows=2)

def int_calc_stars(xx,yy) : 
    
    print 'Starting  int_calc...',time.ctime()
    xinif=loadtxt('lines.rdb',delimiter='\t',usecols=(0,),dtype='float',skiprows=2)
    xendf=loadtxt('lines.rdb',delimiter='\t',usecols=(1,),dtype='float',skiprows=2)

####BEGINNING




    ##calculating the integral of other spectra!

    yini = []
    yend = []
    yint = []
    int1 = []
    int2 = []
    integral = []
    integralnew = []
    yeq = []
    yeqplot = []
    mini = []
    mend = []
    yi = []
    m = []
    maxlocfs = []
    endmaxfs = []
    xintf = []
    iadjust = []
    eadjust = []
    mlfs = []
    emfs = []
    
    maxloc_adjust = []
    endmax_adjust = []

    for n in range(len(xx)) : 
	   print 'Calculating the EWs of star',n+1,'of',len(xx),'. Time:',time.ctime()
	   step = xx[n][1]-xx[n][0]
	   yinit = []
	   yendt = []
	   yintt = []
	   yinttnew = []
	   mt = []
	   xint = []
	   intnew = []
	   int1t = []
	   int2t = []
	   integralt = []
	   yeqt = []
	   yeqplott = []
	   minit = []
	   mendt = []
	   indini = []
	   indend = []
	   yit = []
	   
#	   print maxlocfs[0:100]
	   maxlocfs = []
	   endmaxfs = []
	   

	   for i in range(0,len(xinif)) :

		  maxlocf = min(find(xx[n].round(2) >= xinif[i]))
		  endmaxf = max(find (xx[n].round(2) <= xendf[i]))
		  maxloc_adjust = yy[n][maxlocf-2:maxlocf+3]
		  endmax_adjust = yy[n][endmaxf-2:endmaxf+3]
		  #print maxlocf,endmaxf
		  #print maxloc_adjust
		  ind_temp = max(find (maxloc_adjust == max(maxloc_adjust)))
		  #print ind_temp
		  ind_maxloc = maxlocf+ind_temp-2
		  maxlocfs.append(int(ind_maxloc))
		  ind_temp = min(find (endmax_adjust == max(endmax_adjust)))
		  ind_endmax = endmaxf+ind_temp-2
		  endmaxfs.append(int(ind_endmax))

		  yinit.append(yy[n][maxlocfs[i]])
		  yendt.append(yy[n][endmaxfs[i]])

		  yit.append(yy[n][maxlocfs[i]:endmaxfs[i]+1])  # nao normalizado
		  
		  xint.append(xx[n][maxlocfs[i]:endmaxfs[i]+1])
		  
		  tam = yit[i].size
		  
		  if any(yinit[i] < yit[i][0:5]) : minit.append(max(yit[i][0:5]))
		  else : minit.append(yinit[i])
		  if any(yendt[i] < yit[i][-5:-1]) : mendt.append(max(yit[i][-5:-1]))
		  else : mendt.append(yendt[i])
		  
		  yintt.append(yy[n][maxlocfs[i]:endmaxfs[i]+1]-max(minit[i],mendt[i]))  #normalizado
		  yinttnew.append(yy[n][maxlocfs[i]:endmaxfs[i]+1])  

		  indini.append(max(find (minit[i] == yit[i])))
		  indend.append(min(find (mendt[i] == yit[i])))
		  mt.append ((mendt[i]-minit[i])/(xint[i][indend[i]]-xint[i][indini[i]]))

		  yeqt.append(minit[i]+mt[i]*(xint[i]-xint[i][indini[i]])-max(minit[i],mendt[i])) # condicao fronteira para o integral normalizada
		  yeqplott.append(minit[i] + mt[i]*(xint[i]-xint[i][indini[i]]))

####		   if yeqt < yintt
		  intnew.append(1000*np.trapz(1-yinttnew[i]/yeqplott[i],dx=0.01))
		  
		  int1t.append(np.trapz (yintt[i],dx=0.01))
		  int2t.append(np.trapz (yeqt[i],dx=0.01))

		  if int1t[i] < 0 : 
			 int1t[i] = -int1t[i]
			 int2t[i] = -int2t[i] 

		  integralt.append ((int1t[i]-int2t[i])*1000) #integral in mA
		  

	   #print yinit[0]
	   yini.append(yinit)
	   yend.append(yendt)
	   yi.append(yit)
	   mini.append(minit)
	   mend.append(mendt)
	   yint.append(yintt)
	   m.append(mt)
	   yeq.append(yeqt)
	   yeqplot.append(yeqplott)
	   int1.append(int1t)
	   int2.append(int2t)
	   integral.append(integralt)
	   integralnew.append(intnew)
	   xintf.append(xint)
	   iadjust.append(maxloc_adjust)
	   eadjust.append(endmax_adjust)
	   mlfs.append(maxlocfs)
	   emfs.append(endmaxfs)

#    raw_input ('Press enter to continue')
    integral = array(integral) #datacube of all stars
    integralnew = array(integralnew)
    np.savez ('ew_out.npz',int_ew=integralnew)
    print 'End int_calc',time.ctime() 
    return integralnew






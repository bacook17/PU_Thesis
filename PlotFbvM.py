#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

"""
Plot the baryon-fraction against Mass, for the cluster sample provided in inputfile
"""

def PlotFbvM(inputfile):
    Data = np.genfromtxt(inputfile, dtype=None, names=True)
    Mass = Data['Mvir'] 
 
    Fb_vir = Data['Fgvir'] + Data['Fs200b']
    Fb_12v = Data['Fg12v'] + Data['Fs200b'] 
    errb_vir = np.sqrt(np.power(Data['errgvir'], 2) + np.power(Data['errs200b'], 2))
    errb_12v = np.sqrt(np.power(Data['errg12v'], 2) + np.power(Data['errs200b'], 2))

    #Data from Werk+ 2014
    Fb_gal = 0.144
    errb_gal = 0.03
    M_gal = 10**12.2

    Fb_gal_min, Fb_gal_max = (0.095, 0.19)

    plt.errorbar(Mass, Fb_vir, yerr=errb_vir, c='r', marker='o', ls='', mfc='r', mec='k', ms=8, label=r'r$_{vir}\,$ - Groups+Clusters')
    plt.errorbar(Mass*(1.02), Fb_12v, yerr=errb_12v, marker='o', ls='', mfc='w', ecolor='g', mec='g', ms=8, mew=1, label=r'1.2r$_{vir}\,$ - Groups+Clusters')
        
    plt.errorbar(M_gal, Fb_gal, yerr=errb_gal, marker='p', mec='b', mfc='w', ms=8, ls='', ecolor='b', mew=1, label=r'r$_{vir}\,$ - Galaxies') #using mean of min/max
    plt.errorbar(M_gal, Fb_gal_min, yerr=np.array([[0],[.005]]), uplims=True, mfc='b', mec='b', ms=12, ecolor='b', label='')
    plt.errorbar(10**(12.2), Fb_gal_max, yerr=np.array([[0.005],[0]]), lolims=True, mfc='b', mec='b', ms=12, ecolor='b', label='')
#    lables = np.array([r'Rasheed+ 2010',r'Rasheed+ 2010', r'Rasheed+2010', r'Ade+ 2013', r'Ade+ 2013',r'Eckert+ 2013', r'Eckert+'])

"""
    for i in np.arange(len(Mass)):
        if (np.logical_not(np.isnan(Fb[i]))):
            plt.axvline(Mass[i], ls=':', c='k')
            plt.text(Mass[i], 0.18, lables[Data['Label'][i]], horizontalalignment='left', verticalalignment='top', size='x-small')
"""

def SetAxes(legend=False):
    x = np.linspace(1e+12,2e+15,1000)

    F_wmap = 0.164 #median of given data sets
    sig_F_wmap = 0.004 #Systematic uncertainty, not statistical

    F_planck = 0.156 #median of given data sets
    sig_F_planck = 0.003 #statistical uncertainty

    plt.axhline(y=F_wmap, ls=':', c='k', zorder=-1)
    plt.text(8e+12,F_wmap+0.005, r'f$_{b,WMAP}$', verticalalignment='bottom', size='large')
    plt.fill_between(x, y1=F_wmap - sig_F_wmap, y2=F_wmap + sig_F_wmap, color='k', alpha=0.3, zorder=-2)

    plt.axhline(y=F_planck, ls=':', c='k', zorder=-1)
    plt.text(8e+12,F_planck-0.005, r'f$_{b,Planck}$', verticalalignment='top', size='large')
    plt.fill_between(x, y1=F_planck - sig_F_planck, y2=F_planck + sig_F_planck, edgecolor='k', color='w', zorder=-3, hatch='//', lw=0.0)

    plt.xlabel(r'M$_{vir}$ (M$_\odot$)', size='x-large')
    plt.ylabel(r'f$_b$ ($<$ r)', size='x-large')

    plt.xscale('log')
    plt.xlim([1e+12,2e+15])

    plt.text(4e+12, 0.09, 'Galaxies', size='medium', verticalalignment='center')
    plt.plot(3e+12, 0.09, 'ko', ms=8, mfc='k', mec='k', marker=r'$\Leftarrow$')

    plt.text(1.7e+13, 0.09, 'Groups & Clusters', size='medium', verticalalignment='center')
    plt.plot(1.3e+14, 0.09, 'ko', ms=8, mfc='k', mec='k', marker=r'$\Rightarrow$')

    plt.tick_params(size=10, which='major')
    plt.tick_params(size=5, which='minor')

    if legend:
        plt.legend(loc=0, prop={'size':'medium'}, markerscale=0.7, numpoints=1)

if __name__ == '__main__':
    inputfile = 'F_new.dat'
    plt.figure(1, facecolor='w')
    PlotFbvM(inputfile)
    SetAxes(legend=True)
    if len (sys.argv) == 1:
        plt.show()

    #If two command-line arguments, second is interpreted as
    #name of path to save figure to.
    if len (sys.argv) > 1:
        print("Saving figure as " + sys.argv[1] + "\n")
        plt.savefig (sys.argv[1])

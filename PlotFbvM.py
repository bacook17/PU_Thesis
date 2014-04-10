#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

"""
Plot the baryon-fraction against Mass, for the cluster sample provided in inputfile
"""

def PlotFbvM(inputfile):
    Data = np.genfromtxt(inputfile, dtype=None, names=True)
    Mass = Data['Mass'] * 1.35 #1.35 is rough correction from M500 -> Mvir
    
    Fb = Data['Fvir'] + Data['FS200b']
    Fb2 = Data['Fvir']*np.array([1.08, 1.11, 1.16, 1.18, 1.19, 1.04, 1.086]) + Data['FS200b'] #factors derived for Rasheed data by extrapolating to higher radius, for Planck data by point at 2.28R500 on plot
    #errb = Data['errvir'] + Data['errS200b']
    errb = np.sqrt(np.power(Data['errvir'], 2) + np.power(Data['errS200b'], 2))

    Fb_gal = 0.144
    errb_gal = 0.03
    M_gal = 10**12.2

    Fb_gal_min, Fb_gal_max = (0.095, 0.19)

    plt.errorbar(Mass, Fb, yerr=errb, c='r', marker='o', ls='', mfc='r', mec='k', ms=8, label=r'f$_{gas}$ + f$_*$')
    plt.errorbar(Mass, Fb2, yerr=errb, marker='o', ls='', mfc='None', ecolor='g', mec='g', ms=8, mew=1, label=r'f(1.2r$_{vir}$)', zorder=-1)
        
    plt.errorbar(M_gal, Fb_gal, yerr=errb_gal, marker='p', mec='b', mfc='w', ms=8, ls='', ecolor='b', mew=1, label=r'Werk+ 2014') #using mean of min/max
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
    plt.text(1e+13,F_wmap+0.005, r'f$_{b,WMAP}$', verticalalignment='bottom', size='medium')
    plt.fill_between(x, y1=F_wmap - sig_F_wmap, y2=F_wmap + sig_F_wmap, color='k', alpha=0.3, zorder=-2)

    plt.axhline(y=F_planck, ls=':', c='k', zorder=-1)
    plt.text(1e+13,F_planck-0.004, r'f$_{b,Planck}$', verticalalignment='top', size='medium')
    plt.fill_between(x, y1=F_planck - sig_F_planck, y2=F_planck + sig_F_planck, edgecolor='k', color='w', zorder=-3, hatch='//', lw=0.0)

    plt.xlabel(r'M$_{vir}$ (M$_\odot$)')
    plt.ylabel(r'f$_b$ ($<$ r$_{vir}$)')

    plt.xscale('log')
    plt.xlim([1e+12,2e+15])

    plt.text(4e+12, 0.1, 'Galaxies', size='small', verticalalignment='center')
    plt.plot(3e+12, 0.1, 'ko', ms=8, mfc='k', mec='k', marker=r'$\Leftarrow$')

    plt.text(2e+13, 0.1, 'Groups & Clusters', size='small', verticalalignment='center')
    plt.plot(1.3e+14, 0.1, 'ko', ms=8, mfc='k', mec='k', marker=r'$\Rightarrow$')


    if legend:
        plt.legend(loc=0, prop={'size':'small'}, markerscale=0.7, numpoints=1)

if __name__ == '__main__':
    inputfile = 'F_all.dat'
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

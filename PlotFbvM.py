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
    Fb2 = Data['Fvir']*np.array([1.08, 1.11, 1.16, 1.18, np.nan, 1., 1.,]) + Data['FS200b']
    #errb = Data['errvir'] + Data['errS200b']
    errb = np.sqrt(np.power(Data['errvir'], 2) + np.power(Data['errS200b'], 2))

    plt.errorbar(Mass, Fb, yerr=errb, c='r', marker='o', ls='', mfc='r', mec='k', ms=8, label=r'f$_{gas}$ + f$_*$')
    plt.errorbar(Mass, Fb2, yerr=errb, c='g', marker='o', ls='', mfc='g', mec='k', ms=8, label=r'f(1.2r$_{vir}$)')

    plt.errorbar(10**(12.2), 0.11502, yerr=np.array([[.03742],[.07938]]), marker='o', mfc='k', mec='k', ms=8, ls='', label=r'Werk+ 2014', ecolor='k')

#    lables = np.array([r'Rasheed+ 2010',r'Rasheed+ 2010', r'Rasheed+2010', r'Ade+ 2013', r'Ade+ 2013',r'Eckert+ 2013', r'Eckert+'])

"""
    for i in np.arange(len(Mass)):
        if (np.logical_not(np.isnan(Fb[i]))):
            plt.axvline(Mass[i], ls=':', c='k')
            plt.text(Mass[i], 0.18, lables[Data['Label'][i]], horizontalalignment='left', verticalalignment='top', size='x-small')
"""

def SetAxes(legend=False):
    x = np.linspace(1e+12,2e+15,1000)
    F_b = 0.162
    sig_F_b = 0.006
    plt.axhline(y=F_b, ls='--', c='k', label=None, zorder=-1)
    plt.text(6e+12,F_b+0.0005, r'f$_{b,cosmic}$', verticalalignment='bottom', size='small')
    plt.fill_between(x, y1=F_b - sig_F_b, y2=F_b + sig_F_b, color='k', alpha=0.3, zorder=-1)

    plt.xlabel(r'M$_{vir}$ (M$_\odot$)')
    plt.ylabel(r'f$_b$ ($<$ r$_{vir}$)')

    plt.xscale('log')
    plt.xlim([1e+12,2e+15])

    plt.text(4e+12, 0.08, 'Galaxies', size='small', verticalalignment='center')
    plt.plot(3e+12, 0.08, 'ko', ms=8, mfc='k', mec='k', marker=r'$\leftarrow$')

    plt.text(2e+13, 0.08, 'Groups & Clusters', size='small', verticalalignment='center')
    plt.plot(1.3e+14, 0.08, 'ko', ms=8, mfc='k', mec='k', marker=r'$\rightarrow$')


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

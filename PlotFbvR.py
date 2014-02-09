#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

"""
Plot the baryon-fraction against Mass, for the cluster sample provided in inputfile
"""

def PlotFbvM(inputfile):
    Data = np.genfromtxt(inputfile, dtype=None, names=True)
    Mass = Data['Mass']/1e+13
    
    Fb = Data['Fvir'] + Data['FS200b']
    #errb = Data['errvir'] + Data['errS200b']
    errb = np.sqrt(np.power(Data['errvir'], 2) + np.power(Data['errS200b'], 2))

    plt.errorbar(Mass, Fb, yerr=errb, c='r', marker='o', ls='', mfc='r', mec='k', ms=8, label=r'f$_{gas}$ + f$_*$')

#    lables = np.array([r'Rasheed+ 2010',r'Rasheed+ 2010', r'Rasheed+2010', r'Ade+ 2013', r'Ade+ 2013',r'Eckert+ 2013', r'Eckert+'])

"""
    for i in np.arange(len(Mass)):
        if (np.logical_not(np.isnan(Fb[i]))):
            plt.axvline(Mass[i], ls=':', c='k')
            plt.text(Mass[i], 0.18, lables[Data['Label'][i]], horizontalalignment='left', verticalalignment='top', size='x-small')
"""

def SetAxes(legend=False):
    x = np.linspace(4,110,1000)
    F_b = 0.162
    sig_F_b = 0.006
    plt.axhline(y=F_b, ls='--', c='k', label=None, zorder=-1)
    plt.text(10,F_b+0.0005, r'f$_{b,cosmic}$ (CMB+BAO+H$_0$)', verticalalignment='bottom', size='small')
    plt.fill_between(x, y1=F_b - sig_F_b, y2=F_b + sig_F_b, color='k', alpha=0.3, zorder=-1)

    plt.xlabel(r'Mass ($\times 10^{13} M_\odot$)')
    plt.ylabel(r'f$_b$ ($<$ r$_{vir}$)')

    plt.xscale('log')
    plt.xlim([4,110])

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

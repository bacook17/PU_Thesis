#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

"""
Plot the baryon-fraction against Mass, for the cluster sample provided in inputfile
"""

def PlotFbvM(inputfile):
    Data = np.genfromtxt(inputfile, dtype=None, names=True)
    Mass = Data['Mass']/1e+13
    
    plt.errorbar(Mass, Data['Fvir'], yerr=Data['errvir'], c='k', marker='o', ls='', mfc='w', mec='k', label=r'F$_{gas}$')

    Fb = Data['Fvir'] + Data['FS200b']
    #errb = Data['errvir'] + Data['errS200b']
    errb = np.sqrt(np.power(Data['errvir'], 2) + np.power(Data['errS200b'], 2))

    plt.errorbar(Mass, Fb, yerr=errb, c='r', marker='*', ls='', mfc='r', mec='r', ms=8, label=r'F$_{gas}$ + F$_*$')


def SetAxes(legend=False):
    plt.axhline(y=0.165, ls='-', c='k', label=r'$\Omega_{b}$/$\Omega_{M}$ (WMAP)')
    x = np.linspace(1,100,1000)
    plt.plot(x,0.165 - 0.01*np.power(x/100.,-0.256), ls='--', c='k', label=r'Expected Hot Gas')
    plt.xlabel(r'Mass ($\times 10^{13} M_\odot$)')
    plt.ylabel(r'F (< R$_{vir}$)')

    plt.xscale('log')
    plt.xlim(xmin=4)

    if legend:
        plt.legend(loc=0)

if __name__ == '__main__':
    inputfile = 'F_all.dat'
    plt.figure(1, facecolor='w')
    PlotFbvM(inputfile)
    SetAxes(legend=True)
    plt.show()

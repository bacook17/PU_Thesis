#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

"""
Plot the gas-fraction against Mass, for the cluster sample provided in inputfile
"""

def PlotFgvM(inputfile):
    GasData = np.genfromtxt(inputfile, dtype=None, names=True)

    Mass = GasData['Mass']/1e+13

    plt.errorbar(Mass, GasData['F500'], yerr=GasData['err500'], c='b', marker='o', ls='', label=r'r$_{500}$')
    plt.errorbar(Mass, GasData['F200'], yerr=GasData['err200'], c='g', marker='o', ls='', label=r'r$_{200}$')
    plt.errorbar(Mass, GasData['Fvir'], yerr=GasData['errvir'], c='r', marker='o', ls='', label=r'r$_{vir}$')

def SetAxes(legend=False):
#    plt.axhline(y=0.165, ls='-', c='k', label=r'$\Omega_{b}$/$\Omega_{M}$ (WMAP)')
    f_b = 0.162
    f_star = 0.009
    err_b = 0.006
    err_star = 0.001
    f_gas = f_b - f_star
    err_gas = np.sqrt(err_b**2 + err_star**2)

    plt.axhline(y=f_gas, ls='--', c='k', label=None, zorder=-1)
    x = np.linspace(4,110,1000)
    plt.fill_between(x, y1=f_gas - err_gas, y2=f_gas + err_gas, color='k', alpha=0.3, zorder=-1)
    plt.text(10, f_gas+0.0005, 'Expected Hot Gas', verticalalignment='bottom', size='small')
    plt.xlabel(r'Mass ($\times 10^{13} M_\odot$)')
    plt.ylabel(r'f$_{gas}$ ($<$ r)')

    plt.xscale('log')
    plt.xlim([4,110])

    if legend:
        plt.legend(loc=0, prop={'size':'small'}, markerscale=0.7, numpoints=1)

if __name__ == '__main__':
    inputfile = 'F_all.dat'
    plt.figure(1, facecolor='w')
    PlotFgvM(inputfile)
    SetAxes(legend=True)
    if len (sys.argv) == 1:
        plt.show()

    #If two command-line arguments, second is interpreted as
    #name of path to save figure to.
    if len (sys.argv) > 1:
        print("Saving figure as " + sys.argv[1] + "\n")
        plt.savefig (sys.argv[1])

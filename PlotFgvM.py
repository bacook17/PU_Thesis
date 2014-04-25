#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

"""
Plot the gas-fraction against Mass, for the cluster sample provided in inputfile
"""

def PlotFgvM(inputfile):
    GasData = np.genfromtxt(inputfile, dtype=None, names=True)

    Mass = GasData['Mvir']

    plt.errorbar(Mass, GasData['Fg500'], yerr=GasData['errg500'], c='b', marker='o', ls='', label=r'r$_{500}$', ms=8)
    plt.errorbar(Mass, GasData['Fg200'], yerr=GasData['errg200'], c='g', marker='D', ls='', label=r'r$_{200}$', ms=8)
    plt.errorbar(Mass, GasData['Fgvir'], yerr=GasData['errgvir'], c='r', marker='s', ls='', label=r'r$_{vir}$', ms=8)
    plt.errorbar(Mass, GasData['Fg12v'], yerr=GasData['errg12v'], c='y', marker='h', ls='', label=r'1.2$\times\,$r$_{vir}$', ms=8)

def SetAxes(legend=False):
#    plt.axhline(y=0.165, ls='-', c='k', label=r'$\Omega_{b}$/$\Omega_{M}$ (WMAP)')
    f_b = 0.164
    f_star = 0.01
    err_b = 0.004
    err_star = 0.004
    f_gas = f_b - f_star
    err_gas = np.sqrt(err_b**2 + err_star**2)

    plt.axhline(y=f_gas, ls='--', c='k', label='', zorder=-1)
    x = np.linspace(1e+13,200e+13,1000)
    plt.fill_between(x, y1=f_gas - err_gas, y2=f_gas + err_gas, color='k', alpha=0.3, zorder=-1)
    plt.text(10e+13, f_gas+0.005, r'f$_{gas}$', verticalalignment='bottom', size='large')
    plt.xlabel(r'M$_{vir}$ (M$_\odot$)', size='x-large')
    plt.ylabel(r'f$_{gas}$ ($<$ r)', size='x-large')

    plt.xscale('log')
    plt.xlim([1e+13,2e+15])
    plt.ylim(ymin=0.03)

    plt.tick_params(length=10, which='major')
    plt.tick_params(length=5, which='minor')

    plt.minorticks_on()
    if legend:
        plt.legend(loc=0, prop={'size':'large'}, markerscale=0.7, numpoints=1)

if __name__ == '__main__':
    inputfile = 'F_new.dat'
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

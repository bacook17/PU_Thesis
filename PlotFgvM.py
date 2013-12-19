#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

"""
Plot the gas-fraction against Mass, for the cluster sample provided in inputfile
"""

def PlotFgvM(inputfile):
    GasData = np.genfromtxt(inputfile, dtype=None, names=True)

    Mass = GasData['Mass']/1e+13

    plt.errorbar(Mass, GasData['F500'], yerr=GasData['err500'], c='b', marker='o', ls='', label=r'R$_{500}$')
    plt.errorbar(Mass, GasData['F200'], yerr=GasData['err200'], c='g', marker='o', ls='', label=r'R$_{200}$')
    plt.errorbar(Mass, GasData['Fvir'], yerr=GasData['errvir'], c='r', marker='o', ls='', label=r'R$_{vir}$')

def SetAxes(legend=False):
    plt.axhline(y=0.165, ls='-', c='k', label=r'$\Omega_{b}$/$\Omega_{M}$ (WMAP)')
    plt.axhline(y=0.153, ls='--', c='k', label=r'Expected Hot Gas')
    plt.xlabel(r'Mass ($\times 10^{13} M_\odot$)')
    plt.ylabel(r'F$_{gas}$ (<R)')

    plt.xscale('log')
    plt.xlim(xmin=4)

    if legend:
        plt.legend(loc=0)

if __name__ == '__main__':
    inputfile = 'F_all.dat'
    plt.figure(1, facecolor='w')
    PlotFgvM(inputfile)
    SetAxes(legend=True)
    plt.show()

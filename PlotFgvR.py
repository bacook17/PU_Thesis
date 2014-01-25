#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

"""
Plot the gas-fraction against radius, for the cluster sample provided in inputfile
"""
"""
def PlotFgvR_first(inputfile):
    
    GasData = np.genfromtxt(inputfile, dtype=None, names=True)

    #Radius in units of R500
    R500 = 1.
    R200 = 1.43
    Rvir = 1.90

    #use nan for missing data in a column
    F500 = GasData['F500'][np.logical_not(np.isnan(GasData['F500']))]
    F200 = GasData['F200'][np.logical_not(np.isnan(GasData['F200']))]
    Fvir = GasData['Fvir'][np.logical_not(np.isnan(GasData['Fvir']))]

    err500 = GasData['err500'][np.logical_not(np.isnan(GasData['err500']))]
    err200 = GasData['err200'][np.logical_not(np.isnan(GasData['err200']))]
    errvir = GasData['errvir'][np.logical_not(np.isnan(GasData['errvir']))]

    M500 = GasData['Mass']
    
    plt.errorbar(R500 + np.zeros_like(F500), F500, yerr=err500)
    plt.errorbar(R200 + np.zeros_like(F200), F200, yerr=err200)
    plt.errorbar(Rvir + np.zeros_like(Fvir), Fvir, yerr=errvir)
"""
def PlotFgvR(inputfile):
    GasData = np.genfromtxt(inputfile, dtype=None, names=True)

    #Radius in units of R500
    R500 = 1.
    R200 = 1.325
    Rvir = 1.90
    R3_500 = 3.

    radius = np.array([R500, R200, Rvir, R3_500])

    colors = np.array(['b', 'r', 'g'])
    styles = np.array(['-','--','-.','..'])

    lables = np.array([r'Rasheed et al. 2010 - %1.1e M$_\odot$',r'Rasheed et al. 2010 - %1.1e M$_\odot$',r'Rasheed et al. 2010 - %1.1e M$_\odot$',r'Rasheed et al. 2010 - %1.1e M$_\odot$',r'Ade et al. 2013 - %1.1e M$_\odot$', r'Eckert et al. 2013 - %1.1e M$_\odot$', r'Eckert et al. 2013 - Cool Core']) 
    
    for i in np.arange(len(GasData['Mass'])):
        data = GasData[i]
        Fgas = np.array([data['F500'], data['F200'], data['Fvir'], data['F3_R500']])
        err = np.array([data['err500'], data['err200'], data['errvir'], data['err3_R500']])
        
        plt.errorbar(radius, Fgas, yerr=err, c=colors[data['ref']-1], marker='o', ms=8, ls=data['Style'])#, label = lables[data['Label']] %(data['Mass']))

def SetAxes(legend=False):
    plt.axhline(y=0.165, ls='-', c='k', label=r'$\Omega_{b}$/$\Omega_{M}$ (WMAP)')
    plt.axhline(y=0.153, ls='--', c='k', label=r'Expected Hot Gas')
    plt.xlabel(r'R/R$_{500}$')
    plt.ylabel(r'F$_{gas}$ (<R)')
    plt.xticks([1., 1.43, 1.5, 1.9, 2., 3.],[1, r'R$_{200}$', 1.5, r'R$_{vir}$', 2.,3.])
    plt.xlim([0.8,3.2])

    if legend:
        plt.legend(loc=0)

if __name__ == '__main__':
    inputfile = 'F_all.dat'
    plt.figure(1, facecolor='w')
    PlotFgvR(inputfile)
    SetAxes(legend=True)
    if len (sys.argv) == 1:
        plt.show()

    #If two command-line arguments, second is interpreted as
    #name of path to save figure to.
    if len (sys.argv) > 1:
        print("Saving figure as " + sys.argv[1] + "\n")
        plt.savefig (sys.argv[1])

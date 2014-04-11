#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

def PlotFgvR(inputfile):
    GasData = np.genfromtxt(inputfile, dtype=None, names=True)

    #Radius in units of R500
    R500 = 1./1.9
    R200 = 1.325/1.9
    Rvir = 1.
    R3_500 = 3./1.9

    radius = np.array([R500, R200, Rvir, R3_500])

    colors = np.array(['b', 'r', 'g'])
    styles = np.array(['-','--','-.','..'])

    lables = np.array([r'Rasheed+ 2011 - %1.1e M$_\odot$',r'Planck Coll. H1 - %1.1e M$_\odot$', r'Planck Coll. H2 - %1.1e M$_\odot$',r'Eckert+ 2013 - %1.1e M$_\odot$', r'Eckert+ 2013 - Cool Core'])

    markers = np.array(['o','s','D','^','o','s','o','D'])
    
    for i in np.arange(len(GasData['Mass'])):
        data = GasData[i]
        Fgas = np.array([data['F500'], data['F200'], data['Fvir'], data['F3_R500']])
        err = np.array([data['err500'], data['err200'], data['errvir'], data['err3_R500']])
        
        plt.errorbar(radius, Fgas, yerr=err, c=colors[data['ref']-1], marker=markers[i], ms=8, ls=data['Style'], label = lables[data['Label']] %(data['Mass']*1.35)) #1.35 is correction from M500 -> Mvir

def SetAxes(legend=False):
    f_b = 0.164
    f_star = 0.01
    err_b = 0.006
    err_star = 0.001
    f_gas = f_b - f_star
    err_gas = np.sqrt(err_b**2 + err_star**2)

    plt.axhline(y=f_gas, ls='--', c='k', label='', zorder=-1)
    x = np.linspace(.4,2.,1000)
    plt.fill_between(x, y1=f_gas - err_gas, y2=f_gas + err_gas, color='k', alpha=0.3, zorder=-1)
    plt.text(.6, f_gas+0.006, r'f$_{gas}$', verticalalignment='bottom', size='large')
    plt.xlabel(r'r/r$_{vir}$', size='x-large')
    plt.ylabel(r'f$_{gas}$ ($<$ r)', size='x-large')

    plt.xscale('log')
    plt.xticks([1./1.9, 1.33/1.9, 1, 1.5, 2.],[r'r$_{500}$', r'r$_{200}$', 1, 1.5, 2], size='large')
    plt.tick_params(length=10, which='major')
    plt.tick_params(length=5, which='minor')
    plt.xlim([0.4,2.])

    if legend:
        plt.legend(loc=0, prop={'size':'small'}, markerscale=0.7, numpoints=1)

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

#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os

def PlotFgvR(inputfile):
    GasData = np.genfromtxt(inputfile, dtype=None, names=True)

    #Radius in units of R500
    R500 = 1./1.9
    R200 = 1.325/1.9
    Rvir = 1.
    
    radius = np.array([R500, R200, Rvir, 1.2*Rvir])

    colors = np.array(['b','c', 'r', 'g', 'y'])
    styles = np.array(['-','--','-.','..'])

    lables = np.array([r'G09 - %1.0e M$_\odot$',r'P1 - %1.0e M$_\odot$', r'P2 - %1.0e M$_\odot$',r'E13 - %1.0e M$_\odot$', r'E13 - Cool Core', r'U09 - %1.0e M$_\odot$'])

    markers = np.array(['o','s','D','^','o','s','o','D'])
    
    for i in np.arange(len(GasData['Mvir'])):
        data = GasData[i]
        Fgas = np.array([data['Fg500'], data['Fg200'], data['Fgvir'], data['Fg12v']])
        err = np.array([data['errg500'], data['errg200'], data['errgvir'], data['errg12v']])
        
        plt.errorbar(radius, Fgas, yerr=err, c=data['Color'], marker=data['Marker'], ms=8, ls=data['Style'], label = lables[data['Label']] %(data['Mvir']))

def SetAxes(legend=False):
    f_b = 0.164
    f_star = 0.01
    err_b = 0.006
    err_star = 0.004
    f_gas = f_b - f_star
    err_gas = np.sqrt(err_b**2 + err_star**2)

    plt.axhline(y=f_gas, ls='--', c='k', label='', zorder=-1)
    x = np.linspace(.0,2.,1000)
    plt.fill_between(x, y1=f_gas - err_gas, y2=f_gas + err_gas, color='k', alpha=0.3, zorder=-1)
    plt.text(.6, f_gas+0.006, r'f$_{gas}$', verticalalignment='bottom', size='large')
    plt.xlabel(r'r/r$_{vir}$', size='x-large')
    plt.ylabel(r'f$_{gas}$ ($<$ r)', size='x-large')

    plt.xscale('log')
    plt.xticks([1./1.9, 1.33/1.9, 1, 1.5, 2.],[r'r$_{500}$', r'r$_{200}$', 1, 1.5, 2], size='large')
    #plt.yticks([.1, .2], ['0.10', '0.20'])
    plt.tick_params(length=10, which='major')
    plt.tick_params(length=5, which='minor')
    plt.xlim([0.4,1.5])
    plt.minorticks_on()

    if legend:
        plt.legend(loc=0, prop={'size':'small'}, markerscale=0.7, numpoints=1, ncol=2)

if __name__ == '__main__':
    inputfile = 'F_new.dat'
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

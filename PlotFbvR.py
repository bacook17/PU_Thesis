#! /usr/bin/env python
import sys, os.path as op
import matplotlib.pyplot as plt, numpy as np, os
from scipy.interpolate import interp1d

"""
Plot the baryon-fraction against Radius, for the cluster sample provided in inputfile_1 and stellar fraction data 
provided in inputfile_2, and eventually LSS and galaxy scales
"""

def PlotFbvR(inputfile_1, inputfile_2):
    Gas_Data = np.genfromtxt(inputfile_1, dtype=None, names=True)
    Star_Data = np.genfromtxt(inputfile_2, skip_header=1, unpack=True, delimiter=',')

    #Radius in units of R500
    R500 = 1.
    R200 = 1.325
    Rvir = 1.90
    R3_500 = 3.

    star_radius = Star_Data[0]*R200 #radius in units of R500
    gas_radius = np.array([R500, R200, Rvir, R3_500])

    F_star_med = np.array(Star_Data[3])
    err_star_med = np.array(Star_Data[4])
    F_star_med_int = interp1d(star_radius, F_star_med)
    err_star_med_int = interp1d(star_radius, err_star_med)

    F_star_high = np.array(Star_Data[5])
    err_star_high = np.array(Star_Data[6])
    F_star_high_int = interp1d(star_radius, F_star_high)
    err_star_high_int = interp1d(star_radius, err_star_high)
   

    #Average the data for the two "medium richness" samples
    F_gas_med_500, err_gas_med_500 = WeightMean(Gas_Data['F500'][np.array([2,3])], Gas_Data['err500'][np.array([2,3])])
    F_gas_med_200, err_gas_med_200 = WeightMean(Gas_Data['F200'][np.array([2,3])], Gas_Data['err200'][np.array([2,3])])
    F_gas_med_vir, err_gas_med_vir = WeightMean(Gas_Data['Fvir'][np.array([2,3])], Gas_Data['errvir'][np.array([2,3])])
    F_gas_med_3_500, err_gas_med_3_500 = np.nan, np.nan
    
    F_gas_med = np.array([F_gas_med_500,F_gas_med_200,F_gas_med_vir,F_gas_med_3_500])
    err_gas_med = np.array([err_gas_med_500,err_gas_med_200,err_gas_med_vir,err_gas_med_3_500])

    #Average the data for the three "high richness" samples
    F_gas_high_500, err_gas_high_500 = WeightMean(Gas_Data['F500'][np.array([0,1,4])], Gas_Data['err500'][np.array([0,1,4])])
    F_gas_high_200, err_gas_high_200 = WeightMean(Gas_Data['F200'][np.array([0,1,4])], Gas_Data['err200'][np.array([0,1,4])])
    F_gas_high_vir, err_gas_high_vir = WeightMean(Gas_Data['Fvir'][np.array([0,1,4])], Gas_Data['errvir'][np.array([0,1,4])])
    F_gas_high_3_500, err_gas_high_3_500 = Gas_Data['F3_R500'][4], Gas_Data['err3_R500'][4]

    F_gas_high = np.array([F_gas_high_500,F_gas_high_200,F_gas_high_vir,F_gas_high_3_500])
    err_gas_high = np.array([err_gas_high_500,err_gas_high_200,err_gas_high_vir,err_gas_high_3_500])

    #Combine with the (interpolated) stellar fraction at each radius
    F_b_med = F_gas_med + F_star_med_int(gas_radius)
    err_b_med = np.sqrt(np.power(err_gas_med, 2) + np.power(err_star_med_int(gas_radius),2))

    F_b_high = F_gas_high + F_star_high_int(gas_radius)
    err_b_high = np.sqrt(np.power(err_gas_high, 2) + np.power(err_star_high_int(gas_radius),2))

    #Plot them all
    plt.errorbar(gas_radius,F_gas_med, yerr=err_gas_med, c='g', marker='o', ls='--', mfc='g', mec='k', ms=8, label=r'Gas, med')
    plt.errorbar(gas_radius,F_gas_high, yerr=err_gas_high, c='b', marker='o', ls='--', mfc='b', mec='k', ms=8, label=r'Gas, high')
    plt.errorbar(star_radius, F_star_med, yerr=err_star_med, c='g', marker='*', ls='--', mfc='g', mec='k', ms=8, label=r'Stars, med')
    plt.errorbar(star_radius, F_star_high, yerr=err_star_high, c='b', marker='*', ls='--', mfc='b', mec='k', ms=8, label=r'Stars, high')

    plt.errorbar(gas_radius, F_b_med, yerr=err_b_med, c='g', marker='D', ls='--', mfc='g', mec='k', ms=8, label=r'Baryons, med')
    plt.errorbar(gas_radius, F_b_high, yerr=err_b_high, c='b', marker='D', ls='--', mfc='b', mec='k', ms=8, label=r'Baryons, high')

    F_b_max = F_b_high[-1]
    err_b_max = err_b_high[-1]

    radius_extrapolate = np.logspace(np.log10(R3_500), np.log10(40), 100)
    plt.fill_between(radius_extrapolate, y1=F_b_max - err_b_max, y2=F_b_max + err_b_max, color='b', alpha=0.3, zorder=-2)
    plt.plot(radius_extrapolate, np.zeros_like(radius_extrapolate)+F_b_max, 'b--', marker=None, lw=2)


def WeightMean(values, errors):
    w = np.power(errors, -2)
    mean = np.sum(values*w)/np.sum(w)
    uncert = np.power(np.sum(w),-0.5)

    return mean, uncert

def SetAxes(legend=False):
    x = np.linspace(.2,40,1000)
    F_b = 0.162
    sig_F_b = 0.006
    plt.axhline(y=F_b, ls='--', c='k', label=None, zorder=-1)
    plt.text(.4,F_b+0.005, r'f$_{b,cosmic}$ (CMB+BAO+H$_0$)', verticalalignment='bottom', size='medium')
    plt.fill_between(x, y1=F_b - sig_F_b, y2=F_b + sig_F_b, color='k', alpha=0.3, zorder=-1)

    plt.xlabel(r'r/r$_{500}$')
    plt.ylabel(r'f$_{X}$ ($<$ r)')

    plt.xscale('log')
    plt.xlim([0.2,40])

    plt.ylim(ymax=0.2)

    if legend:
        plt.legend(loc=0, prop={'size':'small'}, markerscale=0.7, numpoints=1)

if __name__ == '__main__':
    inputfile_1 = 'F_all.dat'
    inputfile_2 = 'stellar_fraction.dat'
    plt.figure(1, facecolor='w')
    PlotFbvR(inputfile_1, inputfile_2)
    SetAxes(legend=True)
    if len (sys.argv) == 1:
        plt.show()

    #If two command-line arguments, second is interpreted as
    #name of path to save figure to.
    if len (sys.argv) > 1:
        print("Saving figure as " + sys.argv[1] + "\n")
        plt.savefig (sys.argv[1])

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

    #Radius in units of Rvir
    R500 = 1./1.9
    R200 = 1.325/1.9
    Rvir = 1.
    R3_500 = 3./1.9

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
#    F_gas_med_500, err_gas_med_500 = WeightMean(Gas_Data['F500'][np.array([2,3])], Gas_Data['err500'][np.array([2,3])])
#    F_gas_med_200, err_gas_med_200 = WeightMean(Gas_Data['F200'][np.array([2,3])], Gas_Data['err200'][np.array([2,3])])
#    F_gas_med_vir, err_gas_med_vir = WeightMean(Gas_Data['Fvir'][np.array([2,3])], Gas_Data['errvir'][np.array([2,3])])
    F_gas_med_500, err_gas_med_500 = WeightMean(Gas_Data['F500'][np.array([2,3,4])], Gas_Data['err500'][np.array([2,3,4])])
    F_gas_med_200, err_gas_med_200 = WeightMean(Gas_Data['F200'][np.array([2,3,4])], Gas_Data['err200'][np.array([2,3,4])])
    F_gas_med_vir, err_gas_med_vir = WeightMean(Gas_Data['Fvir'][np.array([2,3,4])], Gas_Data['errvir'][np.array([2,3,4])])

    F_gas_med_3_500, err_gas_med_3_500 = np.nan, np.nan
    
    F_gas_med = np.array([F_gas_med_500,F_gas_med_200,F_gas_med_vir,F_gas_med_3_500])
    err_gas_med = np.array([err_gas_med_500,err_gas_med_200,err_gas_med_vir,err_gas_med_3_500])

    #Average the data for the three "high richness" samples
#    F_gas_high_500, err_gas_high_500 = WeightMean(Gas_Data['F500'][np.array([0,1,5])], Gas_Data['err500'][np.array([0,1,5])])
#    F_gas_high_200, err_gas_high_200 = WeightMean(Gas_Data['F200'][np.array([0,1,5])], Gas_Data['err200'][np.array([0,1,5])])
#    F_gas_high_vir, err_gas_high_vir = WeightMean(Gas_Data['Fvir'][np.array([0,1,5])], Gas_Data['errvir'][np.array([0,1,5])])
    F_gas_high_500, err_gas_high_500 = WeightMean(Gas_Data['F500'][np.array([0,1,5,6])], Gas_Data['err500'][np.array([0,1,5,6])])
    F_gas_high_200, err_gas_high_200 = WeightMean(Gas_Data['F200'][np.array([0,1,5,6])], Gas_Data['err200'][np.array([0,1,5,6])])
    F_gas_high_vir, err_gas_high_vir = WeightMean(Gas_Data['Fvir'][np.array([0,1,5,6])], Gas_Data['errvir'][np.array([0,1,5,6])])

    F_gas_high_3_500, err_gas_high_3_500 = Gas_Data['F3_R500'][5], Gas_Data['err3_R500'][5]

    F_gas_high = np.array([F_gas_high_500,F_gas_high_200,F_gas_high_vir,F_gas_high_3_500])
    err_gas_high = np.array([err_gas_high_500,err_gas_high_200,err_gas_high_vir,err_gas_high_3_500])

    #Combine with the (interpolated) stellar fraction at each radius
    F_b_med = F_gas_med + F_star_med_int(gas_radius)
    err_b_med = np.sqrt(np.power(err_gas_med, 2) + np.power(err_star_med_int(gas_radius),2))

    F_b_high = F_gas_high + F_star_high_int(gas_radius)
    err_b_high = np.sqrt(np.power(err_gas_high, 2) + np.power(err_star_high_int(gas_radius),2))

    #Plot F_gas and F_star
    plt.figure(1, facecolor='w')

    plt.errorbar(gas_radius,F_gas_high, yerr=err_gas_high, color='b', marker='D', ls='--', mfc='w', mec='b',mew=1.5, ms=8, label=r'Gas, M > 10$^{14.5}$M$_\odot$')
    plt.errorbar(gas_radius,F_gas_med, yerr=err_gas_med, color='g', marker='D', ls='--', mfc='w', mec='g',mew=1.5, ms=8, label=r'Gas, M < 10$^{14.5}$M$_\odot$')
    plt.text(1.25,0.12, r'f$_{gas}$($<$ r)', size='large')

    plt.errorbar(star_radius, F_star_high, yerr=err_star_high, c='b', marker='*', ls='--', mfc='b', mec='k', ms=12, label=r'Stars, M > 10$^{14.5}$M$_\odot$')
    plt.errorbar(star_radius, F_star_med, yerr=err_star_med, c='g', marker='*', ls='--', mfc='g', mec='k', ms=12, label=r'Stars, M < 10$^{14.5}$M$_\odot$')
    plt.text(2, 0.025, r'f$_{stars}$($<$ r)', size='large')
    
    plt.figure(2, facecolor='w')
    plt.errorbar(gas_radius, F_b_high, yerr=err_b_high, c='b', marker='o', ls='--', mfc='b', mec='k', ms=8, label=r'M > 10$^{14.5}$M$_\odot$')
    plt.errorbar(gas_radius, F_b_med, yerr=err_b_med, c='g', marker='s', ls='--', mfc='g', mec='k', ms=8, label=r'M < 10$^{14.5}$M$_\odot$')

    F_b_max = F_b_high[-1]
    err_b_max = err_b_high[-1]

    radius_extrapolate = np.logspace(np.log10(R3_500), np.log10(40), 100)
    plt.fill_between(radius_extrapolate, y1=F_b_max - err_b_max, y2=F_b_max + err_b_max, color='b', alpha=0.3, zorder=-1)
    plt.plot(radius_extrapolate, np.zeros_like(radius_extrapolate)+F_b_max, 'b--', marker=None, lw=2)


def WeightMean(values, errors):
    w = np.power(errors, -2)
    mean = np.sum(values*w)/np.sum(w)
    uncert = np.power(np.sum(w),-0.5)

    return mean, uncert

def SetAxes(legend=False):
    x = np.linspace(.1,20,1000)
    F_wmap = 0.164 #median of given data sets
    sig_F_wmap = 0.004 #Systematic uncertainty, not statistical

    F_planck = 0.156 #median of given data sets
    sig_F_planck = 0.003 #statistical uncertainty

    plt.figure(1)
    plt.axhline(y=F_wmap, ls=':', c='k', zorder=-1)
    plt.text(5,F_wmap+0.005, r'f$_{b,WMAP}$', verticalalignment='bottom', size='large')
    plt.fill_between(x, y1=F_wmap - sig_F_wmap, y2=F_wmap + sig_F_wmap, color='k', alpha=0.3, zorder=-2)

    plt.axhline(y=F_planck, ls=':', c='k', zorder=-1)
    plt.text(5,F_planck-0.005, r'f$_{b,Planck}$', verticalalignment='top', size='large')
    plt.fill_between(x, y1=F_planck - sig_F_planck, y2=F_planck + sig_F_planck, edgecolor='k', color='w', zorder=-3, hatch='//', lw=0.0)

    plt.xlabel(r'r/r$_{vir}$', size='x-large')
    plt.ylabel(r'f$_{X}$ ($<$ r)', size='x-large')

    plt.xscale('log')
    plt.xlim([0.4,20])
    plt.tick_params(size=10, which='major')
    plt.tick_params(size=5, which='minor')

    plt.ylim(ymax=0.2)

    if legend:
        plt.legend(loc=0, prop={'size':'medium'}, markerscale=0.7, numpoints=1)

    plt.figure(2)
    plt.axhline(y=F_wmap, ls=':', c='k', zorder=-1)
    plt.text(0.4,F_wmap+0.005, r'f$_{b,WMAP}$', verticalalignment='bottom', size='large')
    plt.fill_between(x, y1=F_wmap - sig_F_wmap, y2=F_wmap + sig_F_wmap, color='k', alpha=0.3, zorder=-2)

    plt.axhline(y=F_planck, ls=':', c='k', zorder=-1)
    plt.text(0.4,F_planck-0.004, r'f$_{b,Planck}$', verticalalignment='top', size='large')
    plt.fill_between(x, y1=F_planck - sig_F_planck, y2=F_planck + sig_F_planck, color='w', edgecolor='k', zorder=-3, hatch='//', lw=0.0)

    plt.xlabel(r'r/r$_{vir}$', size='x-large')
    plt.ylabel(r'f$_{b}$ ($<$ r)', size='x-large')

    plt.xscale('log')
    plt.xlim([0.3,20])

    plt.ylim([0.06,0.2])
    plt.tick_params(size=10, which='major')
    plt.tick_params(size=5, which='minor')

    if legend:
        plt.legend(loc=0, prop={'size':'medium'}, markerscale=0.7, numpoints=1)

if __name__ == '__main__':
    inputfile_1 = 'F_all.dat'
    inputfile_2 = 'stellar_fraction.dat'
    plt.figure(1, facecolor='w')
    PlotFbvR(inputfile_1, inputfile_2)
    SetAxes(legend=True)
    if len (sys.argv) < 3:
        plt.show()

    #If two command-line arguments, second is interpreted as
    #name of path to save figure to.
    if len (sys.argv) == 3:
        plt.figure(1)
        print("Saving figure 1 as " + sys.argv[1] + "\n")
        plt.savefig (sys.argv[1])

        plt.figure(2)
        print("Saving figure 2 as " + sys.argv[2] + "\n")
        plt.savefig (sys.argv[2])

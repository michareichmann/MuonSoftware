#!/usr/bin/env python
# coding=utf-8
# --------------------------------------------------------
# script to plot the calibration data of the TAC
# created June 28th 2019 by M. Reichmann (remichae@phys.ethz.ch)
# --------------------------------------------------------

import csv
from pylab import plot, xlabel, ylabel, title, legend
from matplotlib import pyplot
from numpy import array, linspace
from scipy import odr

def get_calibration(show=False):
    with open('calibration.csv') as f:
        data = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        points = array([row for row in data], 'd')
    x, y = points[:,0], points[:,1]
    xerr, yerr = array([.01] * len(x), 'd'), array([.003] * len(y), 'd')
    fit_func = lambda p, x: p[0] + p[1] * x
    m = odr.Model(fit_func)
    d = odr.RealData(x, y, sx=xerr, sy=yerr)
    p0 = [.1, .3]
    o = odr.ODR(d, m, beta0=p0)
    out = o.run()
    x_fit = linspace(min(x), max(x), 100)
    fit = fit_func(out.beta, x_fit)
    if show:
        pyplot.errorbar(x, y, yerr=xerr,  xerr=yerr, capsize=1, ls='', label='data', markersize=5, marker='o')
        xlabel('Time [us]')
        ylabel('Voltage [V]')
        title('TAC Voltage Calibration')
        plot(x_fit, fit, 'r', lw=2, label='fit: {:1.3f} ({:1.3f}) * x + {:1.3f} ({:1.3f})\nchi2: {:1.2f}'.format(out.beta[0], out.sd_beta[0], out.beta[1], out.sd_beta[1], out.res_var))
        legend(loc='lower right', fontsize = 14)
        pyplot.show()
    return out.beta, out.sd_beta


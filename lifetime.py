#!/usr/bin/env python
# coding=utf-8
# --------------------------------------------------------
# script to plot the lifetime of the muon
# created June 28th 2019 by M. Reichmann (remichae@phys.ethz.ch)
# --------------------------------------------------------

from pylab import plot, xlabel, ylabel, title, legend, hist, axis
from matplotlib import pyplot
from numpy import array, arange, mean, e
from scipy import odr
from calibration import get_calibration

data = []
times = []
with open('wave0.txt') as f:
    event = []
    for line in f.readlines():
        line = line.strip('\n\r')
        if line[0].isdigit():
            event.append(int(line))
        if line.startswith('Trigger Time Stamp'):
            times.append(int(line.split(':')[-1]))
        if line.startswith('DC offset'):
            if event:
                data.append(array(event))
            event = []

voltages = [mean(v[400:600]) - mean(v[0:100]) for v in data]
voltages = [v / (2 ** 14 - 1) for v in voltages if v > 50]  # adc to volt
c = get_calibration()
times = [12 - (v - c[0][0]) / c[0][-1] for v in voltages]  # volt to us
n, bins, patches = hist(times, 30, label='data', hold=True)
axis([0, 12, 0, 40])


def wf(n=0):
    plot(arange(len(data[n])), data[n], 'r', lw=2)
    pyplot.show()


def fit(show=True):
    fit_func = lambda t, x: e ** (-1 * (x - t[1]) / t[0])
    m = odr.Model(fit_func)
    d = odr.RealData(bins[:-1], n)
    t0 = [.5, 7]
    o = odr.ODR(d, m, beta0=t0)
    out = o.run()
    x_fit = bins
    fit = fit_func(out.beta, x_fit)
    if show:
        xlabel('Time [us]')
        ylabel('Number of Entries')
        title('Muon Life Time')
        plot(x_fit, fit, 'r', lw=2, label='fit: e^(-x/t0), t0={:1.3f} ({:1.3f}) \nchi2: {:1.2f}'.format(out.beta[0], out.sd_beta[0], out.res_var))
        legend(loc='upper right', fontsize = 14)
        axis([0, 12, 0, 40])
        pyplot.show()
    return out.beta, out.sd_beta

a = fit()
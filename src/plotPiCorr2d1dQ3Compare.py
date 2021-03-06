#!/usr/bin/env python3
# Purpose:  Read pre-computed 1d and 2d-correlation maps in a wall-parallel
#           plane for the energy flux (Pi) and Q3 events representing typical
#           inward interactions of the near-wall cycle. Correlation maps are
#           read from several ascii files and plotted for three different
#           filters (Fourier, Gauss, box) to compare the effect of the kernel.
#           The 1d correlations appear along the corresponding axes of the 2d
#           maps. Additional contour lines can be plotted on top of the 2d maps.
#           Output is interactive or as pfd figure file. TODO: find out how
#           to read number following a particular string when reading from file,
#           see manual hack below.
# Usage:    python plotPiCorr2d1dQ3Compare.py
# Authors:  Daniel Feldmann, Mohammad Umair
# Date:     28th March 2019
# Modified: 24th September 2019

import timeit
import numpy as np
import h5py

# plot mode: (0) none, (1) interactive, (2) pdf
print('Plot 1d and 2d cross-correlations between energy flux and Q3 (inward) interactions based on different kernels.')
plot = int(input("Enter plot mode (0 = none, 1 = interactive, 2 = pdf file): "))

# some case parameters
Re_b   = 5300.0 # Bulk Reynolds number  Re_b   = u_b   * D / nu = u_cHP * R / nu
Re_tau =  180.4 # Shear Reynolds number Re_tau = u_tau * R / nu

# read 1d azimuthal cross-correlation with Q3 events for Fourier filtered eFlux from ascii file
fnam = 'piCorrThQsFourier2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 1d cross-correlation from', fnam)
th1d  = np.loadtxt(fnam)[:, 0] # 1st column: Azimuthal separation, only once
pqthF = np.loadtxt(fnam)[:, 8] # 9th column: Cross-correlation Q3 with Pi

# read 1d azimuthal cross-correlation with Q3 events for Gauss filtered eFlux from ascii file
fnam = 'piCorrThQsGauss2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 1d cross-correlation from', fnam)
pqthG = np.loadtxt(fnam)[:, 8] # 9th column: Cross-correlation Q3 with Pi

# read 1d azimuthal cross-correlation with Q3 events for box filtered eFlux from ascii file
fnam = 'piCorrThQsBox2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 1d cross-correlation from', fnam)
pqthB = np.loadtxt(fnam)[:, 8] # 9th column: Cross-correlation Q3 with Pi

# read 1d axial cross-correlation with Q3 events for Fourier filtered eFlux from ascii file
fnam = 'piCorrZQsFourier2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 1d cross-correlation from', fnam)
z1d  = np.loadtxt(fnam)[:, 0] # 1st column: Axial separation, only once
pqzF = np.loadtxt(fnam)[:, 8] # 9th column: Cross-correlation Q3 with Pi

# read 1d axial cross-correlation with Q3 events for Gauss filtered eFlux from ascii file
fnam = 'piCorrZQsGauss2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 1d cross-correlation from', fnam)
pqzG = np.loadtxt(fnam)[:, 8] # 9th column: Cross-correlation Q3 with Pi

# read 1d axial cross-correlation with Q3 events for box filtered eFlux from ascii file
fnam = 'piCorrZQsBox2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 1d cross-correlation from', fnam)
pqzB = np.loadtxt(fnam)[:, 8] # 9th column: Cross-correlation Q3 with Pi

# grid size, manual hack (TODO: read this from header info of piCorrThZ*.dat)
nth = len(th1d) # 385  # azimuthal grid points
nz  = len(z1d)  # 2305 # axial grid points
print('With', nth, 'azimuthal (th) points')
print('With', nz, 'axial (z) points')
print('It is your responsibility to make sure that the 2d correlations are defined on the exact same grid.')

# read 2d cross-correlation with Q3 events for Fourier filtered eFlux from ascii file
fnam = 'piCorrThZQsFourier2d_pipe0002_01675000to01675000nt0001.dat'
fnam = 'piCorrThZQsFourier2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 2d cross-correlations from', fnam)
Dt = np.loadtxt(fnam)[:, 0] #  1st column: Azimuthal displacement
Dz = np.loadtxt(fnam)[:, 1] #  2nd column: Axial displacement
f  = np.loadtxt(fnam)[:, 9] # 10th column: Cross-correlation for Q3 and Pi

# read 2d cross-correlation with Q3 events for Gauss filtered eFlux from ascii file
fnam = 'piCorrThZQsGauss2d_pipe0002_01675000to01675000nt0001.dat'
fnam = 'piCorrThZQsGauss2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 2d cross-correlations from', fnam)
g  = np.loadtxt(fnam)[:, 9] # 10th column: Cross-correlation for Q3 and Pi

# read 2d cross-correlation with Q3 events for box filtered eFlux from ascii file
fnam = 'piCorrThZQsBox2d_pipe0002_01675000to01675000nt0001.dat'
fnam = 'piCorrThZQsBox2d_pipe0002_00570000to01675000nt0222.dat'
print('Reading 2d cross-correlations from', fnam)
b  = np.loadtxt(fnam)[:, 9] # 10th column: Cross-correlation for Q3 and Pi

# re-cast cross-correlation data into 2d array for plotting
# (TODO: this is straight-forward fortran programming style and can maybe be done much more efficiently in Python...?)
print('Re-cast data into 2d arrays for plotting')
DeltaTh = np.zeros(nth)
DeltaZ  = np.zeros(nz)
ccF = np.zeros((nth, nz))
ccG = np.zeros((nth, nz))
ccB = np.zeros((nth, nz))
for i in range(nth):
 for j in range(nz):
  DeltaTh[i] = Dt[i*(nz)+j]
  DeltaZ[j]  = Dz[i*(nz)+j]
  ccF[i, j] = f[i*(nz)+j]
  ccG[i, j] = g[i*(nz)+j]
  ccB[i, j] = b[i*(nz)+j]

# find absolute maxima of 2d data sets
amccF = np.max(np.abs(ccF))            # Fourier max
amccG = np.max(np.abs(ccG))            # Gauss max
amccB = np.max(np.abs(ccB))            # Box max
amcc  = np.max([amccF, amccG, amccB])  # all max
print("Absolute maximum correlation value:", amcc)
amcc  = 0.120                          # manual max
clm   = 0.100*amcc                     # set contour level threshold

# convert spatial separation from outer to inner units
th1d = th1d * Re_tau
z1d  =  z1d * Re_tau
DeltaTh = DeltaTh * Re_tau
DeltaZ  = DeltaZ  * Re_tau

# plotting
if plot not in [1, 2]: sys.exit() # skip everything below
print('Creating plot (using LaTeX)...')
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [
r"\usepackage[utf8]{inputenc}",
r"\usepackage[T1]{fontenc}",
r'\usepackage{lmodern, palatino, eulervm}',
#r'\usepackage{mathptmx}',
r"\usepackage[detect-all]{siunitx}",
r'\usepackage{amsmath, amstext, amssymb}',
r'\usepackage{xfrac}']
#mpl.rcParams.update({'font.family': 'sans-serif'})
mpl.rcParams.update({'font.family' : 'serif'})
mpl.rcParams.update({'font.size' : 8})
mpl.rcParams.update({'lines.linewidth'   : 0.75})
mpl.rcParams.update({'axes.linewidth'    : 0.75})
mpl.rcParams.update({'xtick.major.size'  : 2.00})
mpl.rcParams.update({'xtick.major.width' : 0.75})
mpl.rcParams.update({'xtick.minor.size'  : 1.00})
mpl.rcParams.update({'xtick.minor.width' : 0.75})
mpl.rcParams.update({'ytick.major.size'  : 2.00})
mpl.rcParams.update({'ytick.major.width' : 0.75})
mpl.rcParams.update({'ytick.minor.size'  : 1.00})
mpl.rcParams.update({'ytick.minor.width' : 0.75})

# create figure suitable for A4 format
def mm2inch(*tupl):
 inch = 25.4
 if isinstance(tupl[0], tuple):
  return tuple(i/inch for i in tupl[0])
 else:
   return tuple(i/inch for i in tupl)
#fig = plt.figure(num=None, figsize=mm2inch(134.0, 150.0), dpi=300, constrained_layout=False)
fig = plt.figure(num=None, dpi=100, constrained_layout=False)

# conservative colour palette appropriate for colour-blind (http://mkweb.bcgsc.ca/colorblind/)
Vermillion    = '#D55E00'
Blue          = '#0072B2'
BluishGreen   = '#009E73'
Orange        = '#E69F00'
SkyBlue       = '#56B4E9'
ReddishPurple = '#CC79A7'
Yellow        = '#F0E442'
Grey          = '#999999'
Black         = '#000000'
exec(open("./colourMaps.py").read()) # many thanks to github.com/nesanders/colorblind-colormap
VermBlue = CBWcm['VeBu']             # from Vermillion (-) via White (0) to Blue (+)

# modify box for filter name annotation and sub figure label
filterBox = dict(boxstyle="square, pad=0.3", lw=0.5, fc='w', ec=Black)
labelBox  = dict(boxstyle="square, pad=0.3", lw=0.5, fc='w', ec='w')

# axes grid for multiple subplots
import matplotlib.gridspec as gridspec
gs = fig.add_gridspec(nrows=4, ncols=2, hspace=0.0, wspace=0.0, width_ratios=[1,0.25], height_ratios=[1,1,1,1])

# my data range
# define sub-set for plotting (Here in plus units)
xmin = -600.00
xmax =  400.00
ymin = -150.00
ymax =  150.00
cmin =   -0.35
cmax =    0.20

# plot 2d correlation map for Fourier eFlux
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(left=xmin, right=xmax)
ax1.set_ylabel(r"$\Delta\theta r^{+}$")
ax1.set_ylim(bottom=ymin, top=ymax)
ax1.set_yticks([-100, 0.0, 100])
ax1.tick_params(labelbottom=False, labelleft=True)
ax1.minorticks_on()
im1 = ax1.imshow(ccF, vmin=-amcc, vmax=+amcc, cmap=VermBlue, interpolation='bilinear', extent=[np.min(DeltaZ), np.max(DeltaZ), np.min(DeltaTh), np.max(DeltaTh)], origin='lower')
cl1n = ax1.contour(DeltaZ, DeltaTh, ccF, levels=[-clm], colors=Vermillion, linestyles='-', linewidths=0.5)
cl1p = ax1.contour(DeltaZ, DeltaTh, ccF, levels=[+clm], colors=Blue, linestyles='-', linewidths=0.5)
ax1.text(0.98, 0.9, r"Fourier", ha="right", va="top", transform=ax1.transAxes, rotation=0, bbox=filterBox)
ax1.text(0.02, 0.9, r"a)", ha="left", va="top", transform=ax1.transAxes) #, rotation=0, bbox=labelBox)

# plot 2d correlation map for Gauss eFlux
ax2 = fig.add_subplot(gs[1,0], sharex=ax1)
ax2.set_xlim(left=xmin, right=xmax)
ax2.set_ylabel(r"$\Delta\theta r^{+}$")
ax2.set_ylim(bottom=ymin, top=ymax)
ax2.set_yticks([-100, 0.0, 100])
ax2.tick_params(labelbottom=False, labelleft=True)
ax2.minorticks_on()
im2 = ax2.imshow(ccG, vmin=-amcc, vmax=+amcc, cmap=VermBlue, interpolation='bilinear', extent=[np.min(DeltaZ), np.max(DeltaZ), np.min(DeltaTh), np.max(DeltaTh)], origin='lower')
cl2n = ax2.contour(DeltaZ, DeltaTh, ccG, levels=[-clm], colors=Vermillion, linestyles='-', linewidths=0.5)
cl2p = ax2.contour(DeltaZ, DeltaTh, ccG, levels=[+clm], colors=Blue, linestyles='-', linewidths=0.5)
ax2.text(0.98, 0.9, r"Gauss", ha="right", va="top", transform=ax2.transAxes, rotation=0, bbox=filterBox)
ax2.text(0.02, 0.9, r"b)", ha="left", va="top", transform=ax2.transAxes) #, rotation=0, bbox=labelBox)

# plot 2d correlation map for box eFlux
ax3 = fig.add_subplot(gs[2,0], sharex=ax1)
ax3.set_xlim(left=xmin, right=xmax)
ax3.set_ylabel(r"$\Delta\theta r^{+}$")
ax3.set_ylim(bottom=ymin, top=ymax)
ax3.set_yticks([-100, 0.0, 100])
ax3.tick_params(labelbottom=False, labelleft=True)
ax3.minorticks_on()
im3 = ax3.imshow(ccB, vmin=-amcc, vmax=+amcc, cmap=VermBlue, interpolation='bilinear', extent=[np.min(DeltaZ), np.max(DeltaZ), np.min(DeltaTh), np.max(DeltaTh)], origin='lower')
cl3n = ax3.contour(DeltaZ, DeltaTh, ccB, levels=[-clm], colors=Vermillion, linestyles='-', linewidths=0.5)
cl3p = ax3.contour(DeltaZ, DeltaTh, ccB, levels=[+clm], colors=Blue, linestyles='-', linewidths=0.5)
ax3.text(0.98, 0.9, r"Box", ha="right", va="top", transform=ax3.transAxes, rotation=0, bbox=filterBox)
ax3.text(0.02, 0.9, r"c)", ha="left", va="top", transform=ax3.transAxes) #, rotation=0, bbox=labelBox)

# plot 1d azimuthal cross-correlation on the right
ax4 = fig.add_subplot(gs[2,1], sharey = ax3)
ax4.set_xlabel(r"$C_{Q_{3}\Pi}$")
ax4.set_xlim(left=-0.01, right=0.05)
ax4.set_xticks([0.0, 0.05])
ax4.set_ylim(bottom=ymin, top=ymax)
ax4.minorticks_on()
ax4.tick_params(labelbottom=True, labelleft=False)
ax4.axhline(y=0.0, color=Grey)
ax4.axvline(x=0.0, color=Grey)
ax4.plot(pqthF, th1d, color=Black,      linestyle='-', zorder=7, label=r"Fourier")
ax4.plot(pqthG, th1d, color=Vermillion, linestyle='-', zorder=9, label=r"Gauss")
ax4.plot(pqthB, th1d, color=Blue,       linestyle='-', zorder=8, label=r"Box")
#ax4.legend(bbox_to_anchor=(-0.02, 0.0), frameon=False, fancybox=False, facecolor=None, edgecolor=None, framealpha=None)
ax4.legend(loc='upper center', bbox_to_anchor=(0.55, -0.4), frameon=False, fancybox=False, facecolor=None, edgecolor=None, framealpha=None)
ax4.text(0.95, 0.9, r"d)", ha="right", va="top", transform=ax4.transAxes) #, rotation=0, bbox=labelBox)

# plot 1d axial cross-correlation at the bottom
ax5 = fig.add_subplot(gs[3,0], sharex = ax1)
ax5.set_xlabel(r"$\Delta z^+$")
ax5.set_xlim(left=xmin, right=xmax)
ax5.set_xticks([-600, -400, -200, 0, 200, 400])
ax5.minorticks_on()
ax5.set_ylabel(r"$C_{Q_{3}\Pi}$")
ax5.set_ylim(bottom=-0.15, top=0.15)
ax5.set_yticks([-0.15, 0.0, 0.15])
ax5.axhline(y=0.0, color=Grey)
ax5.axvline(x=0.0, color=Grey)
ax5.plot(z1d, pqzF, color=Black,      linestyle='-', zorder=7, label=r"Fourier")
ax5.plot(z1d, pqzG, color=Vermillion, linestyle='-', zorder=9, label=r"Gauss")
ax5.plot(z1d, pqzB, color=Blue,       linestyle='-', zorder=8, label=r"Box")
ax5.text(0.02, 0.9, r"e)", ha="left", va="top", transform=ax5.transAxes) #, rotation=0, bbox=labelBox)

# plot inset/zoom in 1d axial cross-correlation
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)
ax6 = plt.axes([0,0,1,1]) # Create a set of inset Axes: these should fill the bounding box allocated to them
ip = InsetPosition(ax5, [0.10, 0.10, 0.25, 0.80]) # Manually set position and relative size of the inset within original ax5
ax6.set_axes_locator(ip)
ax6.set_xlim(left=-15.0, right=15.0) # where to zoom in?
ax6.set_xticks([])
ax6.set_yticks([])
ax6.axhline(y=0.0, color=Grey)
ax6.axvline(x=0.0, color=Grey)
ax6.plot(z1d, pqzF, color=Black,      linestyle='-', zorder=7, label=r"Fourier")
ax6.plot(z1d, pqzG, color=Vermillion, linestyle='-', zorder=9, label=r"Gauss")
ax6.plot(z1d, pqzB, color=Blue,       linestyle='-', zorder=8, label=r"Box")
#mark_inset(ax2, ax3, loc1=3, loc2=1, fc="none", ec='0.5') # Mark the region corresponding to the inset

# add this for consistent representation of images in ax1 to ax3
# ax1.set_aspect('equal')
# ax2.set_aspect('equal')
# ax3.set_aspect('equal')
# hack: aspect=equal is default for imshow, but destroys my gridspec
ax1.set_aspect('auto')
ax2.set_aspect('auto')
ax3.set_aspect('auto')

# plot common colour bar
axc = plt.axes([0.76, 0.515, 0.035, 0.355])
fmt = FormatStrFormatter('%4.2f')
cb1 = plt.colorbar(im1, cax=axc, format=fmt, orientation="vertical")
cb1.ax.set_ylabel(r"$C_{Q_{3}\Pi}$")
cb1.set_ticks([-amcc, 0.0, +amcc])
axc.axhline(y=-clm, color=Vermillion) # mark negative contour level in colourbar
axc.axhline(y=+clm, color=Blue)       # mark positive contour level in colourbar

# plot mode interactive or pdf
if plot != 2:
 #plt.tight_layout()
 plt.show()
else:
 #fig.tight_layout()
 fnam = str.replace(fnam, '.dat', '.pdf')
 fnam = str.replace(fnam, 'piCorrThZQsBox2d', 'plotPiCorr2d1dQ3Compare')
 plt.savefig(fnam)
 print('Written file', fnam)
fig.clf()

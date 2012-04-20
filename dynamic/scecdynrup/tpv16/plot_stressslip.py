#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# ----------------------------------------------------------------------
#
# Plot initial stress and slip profiles.
#
# PREREQUISITES: matplotlib, numpy, gmt, tables

sim = "tpv16"
cell = "tet4"
dx = 75
griddata = False

# ----------------------------------------------------------------------
import tables
import numpy
import matplotlib.pyplot as pyplot
import matplotlib.cm as cm
import sys
import subprocess

sys.path.append("../../../figures")
import matplotlibext

lineStyle = ("black", 'solid')

# ----------------------------------------------------------------------
figure = matplotlibext.Figure()
figure.open(3.0, 3.0, margins=[[0.4, 0.3, 0.16], [0.35, 0.3, 0.2]], dpi=150)

nrows = 2
ncols = 1
icol = 0

for irow in xrange(nrows):
    if griddata:
        inputRoot = "output/%s_%s_%03dm-fault" % (sim,cell,dx)
        h5 = tables.openFile("%s.h5" % inputRoot, 'r')
        vertices = h5.root.geometry.vertices[:]
        distDip = -vertices[:,2]
        distStrike = vertices[:,1]
        if irow == 0:
            tractionShear = h5.root.vertex_fields.traction[1,:,0].squeeze()
            data = numpy.transpose((distStrike, distDip, -tractionShear/1.0e+6))
        else:
            slip = h5.root.vertex_fields.slip[-1,:,:].squeeze()
            slipMag = (slip[:,0]**2 + slip[:,1]**2)**0.5
            data = numpy.transpose((distStrike, distDip, slipMag))
        h5.close()
        numpy.savetxt("tmp.dat", data, fmt='%14.6f')
        cmd = "triangulate -Gtmp.grd -I75.0/75.0 -R-24.0e+3/+24.0e+3/0.0/19.5e+3 -Jx1.0 < tmp.dat > /dev/null "
        subprocess.call(cmd, shell=True)
        cmd = "grd2xyz tmp.grd > tmp%d.txtgrd" % irow
        subprocess.call(cmd, shell=True)


    ax = figure.axes(nrows, ncols, irow+1, icol+1)
    filename = "tmp%d.txtgrd" % irow
    data = numpy.loadtxt(filename)
    data = numpy.reshape(data, (261, 641, 3))
    if irow == 0:
        label = "Initial Shear Traction (MPa)"
        contours = numpy.arange(0.0, 50.01, 5.0)
    else:
        label = "Final Slip (m)"
        contours = numpy.arange(0.0, 5.01, 0.5)
    pyplot.set_cmap(cm.hot_r)
    CS = ax.contourf(data[:,:,0]/1.0e+3, data[:,:,1]/1e+3, data[:,:,2],
                     levels=contours)
    pyplot.hold(True)
    ax.contour(data[:,:,0]/1.0e+3, data[:,:,1]/1e+3, data[:,:,2],
                levels=contours,
               colors=lineStyle[0],
               linewidths=0.5)

    ax.set_xlim((-24.0, +24.0))
    ax.set_xlabel("Dist. Along Strike (km)")
    ax.set_ylim((19.5, 0.0))
    ax.set_yticks(numpy.arange(0, 20.01, 5.0))
    ax.set_ylabel("Dist. Down Dip (km)")
    ax.set_title(label)
    ax.set_aspect('equal')
    
    pyplot.colorbar(CS, orientation='vertical', fraction=0.05, pad=0.02)

    if irow+1 < nrows:
        ax.set_xticklabels([])
        ax.set_xlabel("")
    if icol > 0:
        ax.set_title("")
        ax.set_yticklabels([])
        ax.set_ylabel("")

pyplot.show()
pyplot.savefig("%s_stressslip" % (sim))


# End of file

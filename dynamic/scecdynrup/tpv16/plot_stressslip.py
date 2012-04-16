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
griddata = True

# ----------------------------------------------------------------------
import tables
import numpy
import matplotlib.pyplot as pyplot
import sys
import subprocess

sys.path.append("../../../figures")
import matplotlibext

lineStyle = ("black", 'solid')

# ----------------------------------------------------------------------
figure = matplotlibext.Figure()
figure.open(3.0, 2.5, margins=[[0.4, 0.3, 0.1], [0.35, 0.4, 0.1]], dpi=150)

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
            data = numpy.transpose((distStrike, dispDip, tractionShear))
        else:
            slip = h5.root.vertex_fields.slip[-1,:,:].squeeze()
            slipMag = (slip[:,0]**2 + slip[:,1]**2)**0.5
            data = numpy.transpose((distStrike, distDip, slipMag))
        h5.close()
        numpy.savetxt("tmp.dat", data, fmt='%14.63')
        cmd = "awk '/^j/ {next}; { print $0 }' tmp.dat | triangulate -Gtmp.grd -I75.0/75.0 -R-24.0e+3/+24.0e+3/0.0/19.5e+3 -Jx1.0 > /dev/null "
                subprocess.call(cmd, shell=True)
                cmd = "grd2xyz tmp.grd > tmp.txtgrd"
                subprocess.call(cmd, shell=True)


    ax = figure.axes(nrows, ncols, irow+1, icol+1)
    filename = "tmp.txtgrd"
    data = numpy.loadtxt(filename)
    data = numpy.reshape(data, (261, 641, 3))
    contours = ax.contour(data[:,:,0]/1.0e+3, data[:,:,1]/1e+3, data[:,:,2],
                                  levels=numpy.arange(0.0, 10.01, 0.5),
                                  colors=lineStyle[0],
                                  linewidths=1.0,
                                  linestyles=lineStyle[1])

    ax.set_xlim((-24.0, +24.0))
    ax.set_xlabel("Dist. Along Strike (km)")
    ax.set_ylim((19.5, 0.0))
    ax.set_yticks(numpy.arange(0, 20.01, 5.0))
    ax.set_ylabel("Dist. Down Dip (km)")
    ax.set_aspect('equal')
    
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

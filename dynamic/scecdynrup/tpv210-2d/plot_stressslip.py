#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# ----------------------------------------------------------------------
#
# Plot initial stress and slip profiles.
#
# PREREQUISITES: matplotlib, numpy, tables.

sim = "tpv13"
cell = "tri3"
dx = 100
showAB = True

infoFilename = "output/%s_%s_%03dm-fault_info.h5" % (sim,cell,dx)
dataFilename = "output/%s_%s_%03dm-fault.h5" % (sim,cell,dx)

# ----------------------------------------------------------------------
import tables
import numpy
import matplotlib.pyplot as pyplot
import sys

sys.path.append("../../../figures")
import matplotlibext

# ----------------------------------------------------------------------
h5 = tables.openFile(infoFilename, 'r')
coefdyn = h5.root.vertex_fields.dynamic_coefficient[:].squeeze()
coefstatic = h5.root.vertex_fields.static_coefficient[:].squeeze()
cohesion = h5.root.vertex_fields.cohesion[:].squeeze() / 1.0e+6
h5.close()

h5 = tables.openFile(dataFilename, 'r')
vertices = h5.root.geometry.vertices[:]
slip = h5.root.vertex_fields.slip[:].squeeze()
traction = h5.root.vertex_fields.traction[1,:,:].squeeze() / 1.0e+6
h5.close()

from math import pi, sin
dipDist = -vertices[:,1]/sin(60.0*pi/180.0)/1.0e+3
order = numpy.argsort(dipDist)

figure = matplotlibext.Figure()
figure.open(3.0, 5.25, margins=[[0.45, 0, 0.15], [0.35, 0.55, 0.2]], dpi=150)

ax = figure.axes(2.0, 1, 1.0, 1)
ax.plot(traction[order,0], dipDist[order], 
        color='red', 
        linewidth=1,
        dashes=(None,None))
ax.hold(True)
ax.plot(traction[order,1], dipDist[order], 
        color='blue', 
        linewidth=1,
        dashes=(3.0,1.5))

ax.plot(cohesion-coefstatic[order]*traction[order,1], dipDist[order], 
        color='orange', 
        linewidth=1,
        dashes=(6.0,1.5))
ax.plot(cohesion-coefdyn[order]*traction[order,1], dipDist[order], 
        color='green', 
        linewidth=1,
        dashes=(1.5,1.5))

ax.set_xlim((-150,150))
ax.set_xlabel("Traction (MPa)")
ax.set_ylim((15.0, 0.0))
ax.set_ylabel("Dist. Down Dip (km)")
ax.legend(('$T_\mathit{shear}$', 
           '$T_\mathit{normal}$',
           '$T_\mathit{failure}$',
           '$T_\mathit{sliding}$',
           ), loc="upper left")
if showAB:
    ax.text(-150, -0.5, "(a)", fontweight='bold')
             

ax = figure.axes(2.0, 1, 2.0, 1)
itime = slip.shape[0]-1
ax.plot(slip[itime,order,0], dipDist[order], 
        color='red', 
        linewidth=1,
        dashes=(None,None))
ax.set_xlabel("Slip (m)")
ax.set_ylim((15.0, 0.0))
ax.set_ylabel("Dist. Down Dip (km)")
if showAB:
    ax.text(0, -0.5, "(b)", fontweight='bold')

pyplot.show()
pyplot.savefig("%s-2d_%s_%03dm_stressslip" % (sim,cell,dx))


# End of file

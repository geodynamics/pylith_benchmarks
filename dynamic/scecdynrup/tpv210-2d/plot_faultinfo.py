#!/usr/bin/env python
#
# ======================================================================
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ======================================================================
#

sim = "tpv12"
cell = "tri3"
dx = 200

inputRoot = "output/%s_%s_%03dm-fault_info" % (sim,cell,dx)

# ----------------------------------------------------------------------
import tables
import numpy
import pylab

# ----------------------------------------------------------------------
h5 = tables.openFile("%s.h5" % inputRoot, 'r')
vertices = h5.root.geometry.vertices[:]
traction = h5.root.vertex_fields.initial_traction[:].squeeze()
h5.close()

from math import pi, sin
dipDist = vertices[:,1]/sin(60.0*pi/180.0)

# Expected tractions
if sim == "tpv10":
    mask = numpy.bitwise_and(dipDist <= -10.5e+3, dipDist >= -13.5e+3)
    shearE = mask*(0.2e+6 + ((0.760+0.0057)*7378*-dipDist)) + \
        ~mask*0.55*7378*-dipDist
    normalE = 7378*dipDist

elif sim == "tpv11": # No 2-D case
    mask = numpy.bitwise_and(dipDist <= -10.5e+3, dipDist >= -13.5e+3)
    shearE = mask*(0.2e+6 + ((0.570+0.0057)*7378*-dipDist)) + \
        ~mask*0.55*7378*-dipDist
    normalE = 7378*dipDist

elif sim == "tpv12":
    mask = dipDist > -13.8e+3
    normalE = mask*7390.01*dipDist + ~mask*14427.98*dipDist
    shearE = mask*-0.549847*normalE + ~mask*0.0

pylab.plot(shearE, dipDist, 'k*',
           traction[:,0], dipDist, 'rx',
           normalE, dipDist, 'k*',
           traction[:,1], dipDist, 'rx')
pylab.show()

# End of file

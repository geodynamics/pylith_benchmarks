#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ----------------------------------------------------------------------
#

sim = "tpv13"
cell = "tet4"
dx = 100

inputRoot = "output/%s_%s_%03dm-fault" % (sim,cell,dx)
outdir = "scecfiles/%s_%s_%03dm/" % (sim,cell,dx)

# ----------------------------------------------------------------------
import tables
import numpy
import time

# ----------------------------------------------------------------------
threshold = 0.001 # threshold for detecting slip has started
maxTime = 1.0e+10 # Large value for default rupture time

h5 = tables.openFile("%s.h5" % inputRoot, 'r')
vertices = h5.root.geometry.vertices[:]
slip = h5.root.vertex_fields.slip[:]
slipRate = h5.root.vertex_fields.slip_rate[:]
timeStamps =  h5.root.time[:].ravel()
dt = timeStamps[1] - timeStamps[0]

h5.close()

nsteps = timeStamps.shape[0]
npts = vertices.shape[0]

rupTime = maxTime * numpy.ones( (npts,), dtype=numpy.float64)

# Create buffer for current rupture time
tmpTime = numpy.zeros( (npts,), dtype=numpy.float64)

itime = 0
for timestamp in timeStamps:
    t = timeStamps[itime]

    # Compute magnitude of slip rate
    slipRateMag = (slipRate[itime,:,0]**2 + slipRate[itime,:,1]**2)**0.5

    # Set rupture time at locations where threshold is exceeded
    mask = slipRateMag > threshold
    tmpTime[:] = maxTime
    tmpTime[mask] = t

    indices = numpy.where(tmpTime < rupTime)[0]
    rupTime[indices] = t

    itime += 1

# Write data
headerA = \
    "# problem = %s\n" % sim.upper() + \
    "# author = Brad Aagaard\n" + \
    "# date = %s\n" % (time.asctime()) + \
    "# code = PyLith\n" + \
    "# code_version = 1.7.0a (scecdynrup branch)\n" + \
    "# element_size = %s m\n" % dx + \
    "# Contour data in 3 columns of E14.6:\n" + \
    "# Column #1 = Distance along strike from hypocenter (m)\n" + \
    "# Column #2 = Distance down-dip from surface (m)\n" + \
    "# Column #3 = Rupture time (s)\n" + \
    "#\n" + \
    "# Data fields\n" + \
    "j k t\n" + \
    "#\n"


distDip = -2*vertices[:,0]
distStrike = vertices[:,1]

filename = "%sruptime.dat" % (outdir)
fout = open(filename, "w")
fout.write(headerA)
data = numpy.transpose((distStrike, distDip, rupTime))
numpy.savetxt(fout, data, fmt='%14.6e')
fout.close()

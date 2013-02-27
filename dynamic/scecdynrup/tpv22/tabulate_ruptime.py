#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# <LicenseText>
#
# ----------------------------------------------------------------------
#

sim = "tpv22"
cell = "tet4"
dx = 200

inputRoot = "output/%s_%s_%03dm" % (sim, cell, dx)
outputRoot = "scecfiles/%s_%s_%03dm" % (sim, cell, dx)

# ----------------------------------------------------------------------
import h5py
import numpy
import time

# ----------------------------------------------------------------------
threshold = 0.001 # threshold for detecting slip has started
maxTime = 1.0e+10 # Large value for default rupture time

# ----------------------------------------------------------------------
def extract(fault):

    h5 = h5py.File("%s-%s.h5" % (inputRoot, fault), 'r', driver="sec2")
    vertices = h5['geometry/vertices'][:]
    slipRate = h5['vertex_fields/slip_rate'][:]
    timeStamps =  h5['time'][:].ravel()
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

    headerA = \
        "# problem = %s\n" % sim.upper() + \
        "# author = Brad Aagaard\n" + \
        "# date = %s\n" % (time.asctime()) + \
        "# code = PyLith\n" + \
        "# code_version = 1.9.0a (scecdynrup branch)\n" + \
        "# element_size = %s\n" % dx + \
        "# Contour data in 3 columns of E14.6:\n" + \
        "# Column #1 = Distance along strike from hypocenter (m)\n" + \
        "# Column #2 = Distance down-dip from surface (m)\n" + \
        "# Column #3 = Rupture time (s)\n" + \
        "#\n" + \
        "# Data fields\n" + \
        "j k t\n" + \
        "#\n"

    distDip = -vertices[:,2]
    distStrike = vertices[:,1]

    filename = "%s_ruptime_%s.dat" % (outputRoot, fault)
    fout = open(filename, "w")
    fout.write(headerA)
    data = numpy.transpose((distStrike, distDip, ruptime))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()

# MAIN FAULT -----------------------------------------------------------
extract("fault_main")

# BRANCH FAULT ---------------------------------------------------------
#extract("fault_stepover")

# End of file

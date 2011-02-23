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

sim = "tpv14"
cell = "tet4"
dx = 200
dt = 0.05

inputRoot = "output/%s_%s_%03dm" % (sim, cell, dx)
outputRoot = "scecfiles/%s_%s_%03dm" % (sim, cell, dx)

threshold = 0.1 # 1 mm/s

# ----------------------------------------------------------------------
import tables
import numpy
import time

# ----------------------------------------------------------------------
def extract(fault):
    tolerance = 1.0e-6

    h5 = tables.openFile("%s-%s.h5" % (inputRoot, fault), 'r')
    vertices = h5.root.geometry.vertices[:]

    # Get datasets
    slip_rate = h5.root.vertex_fields.slip_rate[:]

    # BEGIN TEMPORARY
    #timeStamps =  h5.root.vertex_fields.time (not yet available)
    ntimesteps = slip_rate.shape[0]
    timeStamps = numpy.linspace(0, dt*ntimesteps, ntimesteps, endpoint=True)
    # END TEMPORARY

    h5.close()

    slipRateMag = (slip_rate[:,:,0]**2 +
                   slip_rate[:,:,1]**2)**0.5
    ruptime = 1e+30*numpy.ones( (slip_rate.shape[1],), dtype=numpy.float64)
    for i in xrange(3):
        ii = numpy.where(slipRateMag[i,:] > threshold)[0]
        iimask = timeStamps[i] < ruptime[ii]
        print timeStamps[i]
        print ruptime[iimask]
        ruptime[iimask] = timeStamps[i]

    headerA = \
        "# problem = %s-2D\n" % sim.upper() + \
        "# author = Brad Aagaard\n" + \
        "# date = %s\n" % (time.asctime()) + \
        "# code = PyLith\n" + \
        "# code_version = 1.5.2a (scecdynrup branch)\n" + \
        "# element_size = %s\n" % dx + \
        "# Contour data in 3 columns of E14.6:\n" + \
        "# Column #1 = Distance along strike from hypocenter (m)\n" + \
        "# Column #2 = Distance down-dip from surface (m)\n" + \
        "# Column #3 = Rupture time (s)\n" + \
        "#\n" + \
        "# Data fields\n" + \
        "j k t\n" + \
        "#\n"

    dip = -vertices[:,2]
    if fault == "main_fault":
        strike = (vertices[:,1] - 2000.0)
    elif fault == "branch_fault":
        strike = 2.0 * vertices[:,0]


    filename = "%s_ruptime_%s.dat" % (outputRoot, fault)
    fout = open(filename, "w")
    fout.write(headerA)
    data = numpy.transpose((strike, dip, ruptime))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()




# MAIN FAULT -----------------------------------------------------------
extract("main_fault")

# BRANCH FAULT ---------------------------------------------------------
#extract("branch_fault")


# End of file

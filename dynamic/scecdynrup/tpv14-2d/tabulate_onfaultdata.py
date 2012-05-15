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

sim = "tpv15"
cell = "tri3"
dx = 200
dt = 0.05

inputRoot = "output/%s_%s_%03dm_gradient" % (sim, cell,dx)
outputRoot = "scecfiles/%s_%s_%03dm_gradient" % (sim, cell,dx)

# ----------------------------------------------------------------------
import h5py
import numpy
import time

# ----------------------------------------------------------------------
def extract(fault, targets):
    tolerance = 1.0e-6

    h5 = h5py.File("%s-%s.h5" % (inputRoot, fault), 'r', driver="sec2")
    vertices = h5['geometry/vertices'][:]
    ntargets = targets.shape[0]
    indices = []
    for target in targets:
        dist = ( (vertices[:,0]-target[0])**2 + 
                 (vertices[:,1]-target[1])**2 )**0.5
        min = numpy.min(dist)
        indices.append(numpy.where(dist <= min+tolerance)[0][0])

    print "Indices: ", indices
    print "Coordinates of selected points:\n",vertices[indices,:]

    # Get datasets
    slip = h5['vertex_fields/slip'][:]
    slip_rate = h5['vertex_fields/slip_rate'][:]
    traction = h5['vertex_fields/traction'][:]

    timeStamps =  h5['time'][:]

    h5.close()

    slip = slip[1:,indices,:]
    slip_rate = slip_rate[1:,indices,:]
    traction = traction[1:,indices,:]

    headerA = \
        "# problem = %s-2D\n" % sim.upper() + \
        "# author = Brad Aagaard\n" + \
        "# date = %s\n" % (time.asctime()) + \
        "# code = PyLith\n" + \
        "# code_version = 1.5.2a (scecdynrup branch)\n" + \
        "# element_size = %s\n" % dx
    headerB = \
        "# Time series in 7 columns of E14.6:\n" + \
        "# Column #1 = time (s)\n" + \
        "# Column #2 = horizontal right-lateral slip (m)\n" + \
        "# Column #3 = horizontal right-lateral slip rate (m/s)\n" + \
        "# Column #4 = horizontal right-lateral shear stress (MPa)\n" + \
        "# Column #5 = vertical up-dip slip (m)\n" + \
        "# Column #6 = vertical up-dip slip-rate (m/s)\n" + \
        "# Column #7 = vertical up-dip shear stress (MPa)\n" + \
        "# Column #8 = normal stress (MPa)\n" + \
        "#\n" + \
        "# Data fields\n" + \
        "t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress n-stress\n" + \
        "#\n"

    locHeader = "# location = on fault, %3.1f km along strike and %3.1f km depth\n"
    locName = "st%+04ddp%03d"

    lengthScale = 1000.0
    timeScale = 1000.0
    dip = 7.5
    if fault == "main_fault":
        strike = (targets[:,1] - 2000) / lengthScale
    elif fault == "branch_fault":
        strike = 2.0 * targets[:,0] / lengthScale
    elif fault == "mainbranch_fault":
        maskM = targets[:,0] <= +10.0
        strike = maskM*(targets[:,1] - 2000) / lengthScale + \
                 ~maskM*(2.0 * targets[:,0]) / lengthScale
    elif fault == "mainext_fault":
        strike = (targets[:,1] - 2000) / lengthScale
    else:
        raise ValueError("Unknown fault '%s'" % fault)

    print timeStamps.shape, ntimesteps, slip.shape

    zero = numpy.zeros( (ntimesteps-1, 1), dtype=numpy.float64)
    for iloc in xrange(ntargets):
        if fault == "mainbranch_fault":
            if targets[iloc,0] <= 10.0:
                faultName = "main_fault"
            else:
                faultName = "branch_fault"
        elif fault == "mainext_fault":
            faultName = "main_fault"
        else:
            faultName = fault;
        pt = locName % (round(10*strike[iloc]), 
                        round(10*dip))
        filename = "%s-%s-%s.dat" % (outputRoot, faultName, pt)
        fout = open(filename, 'w');
        fout.write(headerA)
        fout.write("# time_step = %14.6E\n" % dt)
        fout.write("# num_timesteps = %8d\n" % (ntimesteps-1))
        fout.write(locHeader % (strike[iloc], dip))
        fout.write(headerB)
        data = numpy.transpose((timeStamps, 
                                -slip[:,iloc,0],
                                -slip_rate[:,iloc,0],
                                -traction[:,iloc,0]/1e+6,
                                zero,
                                zero,
                                zero,
                                +traction[:,iloc,1]/1e+6))
        numpy.savetxt(fout, data, fmt='%14.6e')
        fout.close()

    return

if sim in ["tpv14", "tpv15"]:
    # ------------------------------------------------------------------
    # MAIN FAULT

    # Target coordinates are relative to faults intersection.
    targets = numpy.array([[0.0,  -2000.0],
                           [0.0,  +2000.0],
                           [0.0,  +5000.0],
                           [0.0,  +9000.0]])
    # Origin of coordinate system is at center of main fault
    targets[:,1] += 2000.0
    
    extract("main_fault", targets)
    
    # ------------------------------------------------------------------
    # BRANCH FAULT

    # Target coordinates are relative to faults intersection.
    targets = numpy.array([[1000.0,  1732.0508],
                           [2500.0,  4330.1270],
                           [4500.0,  7794.2286]])
    # Origin of coordinate system is at center of main fault
    targets[:,1] += 2000.0
    
    extract("branch_fault", targets)

else:
    # ------------------------------------------------------------------
    # MAIN-BRANCH FAULT

    # Target coordinates are relative to faults intersection.
    targets = numpy.array([[0.0,  -2000.0],
                           [1000.0,  1732.0508],
                           [2500.0,  4330.1270],
                           [4500.0,  7794.2286]])
    # Origin of coordinate system is at center of main fault
    targets[:,1] += 2000.0

    extract("mainbranch_fault", targets)

    # ------------------------------------------------------------------
    # MAIN-EXT FAULT
    
    # Target coordinates are relative to faults intersection.
    targets = numpy.array([[0.0,  +2000.0],
                           [0.0,  +5000.0],
                           [0.0,  +9000.0]])
    # Origin of coordinate system is at center of main fault
    targets[:,1] += 2000.0
    
    extract("mainext_fault", targets)


# End of file

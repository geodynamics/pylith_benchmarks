#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ----------------------------------------------------------------------
#

sim = "tpv22"
cell = "tet4"
dx = 200

inputRoot = "output/%s_%s_%03dm" % (sim, cell,dx)
outputRoot = "scecfiles/%s_%s_%03dm/" % (sim, cell,dx)

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
        dist = ( (vertices[:,1]-target[1])**2 + 
                 (vertices[:,2]-target[2])**2 )**0.5
        indices.append(numpy.argmin(dist))
    vertices = vertices[indices,:]

    print "Indices: ", indices
    print "Coordinates of selected points:\n",vertices


    # Get datasets
    slip = h5['vertex_fields/slip'][:]
    slip_rate = h5['vertex_fields/slip_rate'][:]
    traction = h5['vertex_fields/traction'][:]
    timeStamps =  h5['time'][:].ravel()
    nsteps = timeStamps.shape[0]
    dt = timeStamps[1] - timeStamps[0]

    h5.close()

    # Extract locations
    slip = slip[:,indices,:]
    slip_rate = slip_rate[:,indices,:]
    traction = traction[:,indices,:]

    headerA = \
        "# problem = %s\n" % sim.upper() + \
        "# author = Brad Aagaard\n" + \
        "# date = %s\n" % (time.asctime()) + \
        "# code = PyLith\n" + \
        "# code_version = 1.9.1a (scecdynrup branch)\n" + \
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
    strike = vertices[:,1] / lengthScale
    dip = -vertices[:,2] / lengthScale

    for iloc in xrange(ntargets):
        pt = locName % (round(10*strike[iloc]), 
                        round(10*dip[iloc]))
        filename = "%s/%s-%s.dat" % (outputRoot, fault, pt)
        fout = open(filename, 'w');
        fout.write(headerA)
        fout.write("# time_step = %14.6E\n" % dt)
        fout.write("# num_timesteps = %8d\n" % (nsteps))
        fout.write(locHeader % (strike[iloc], dip[iloc]))
        fout.write(headerB)
        data = numpy.transpose((timeStamps, 
                                -slip[:,iloc,0],
                                -slip_rate[:,iloc,0],
                                -traction[:,iloc,0]/1e+6,
                                -slip[:,iloc,1],
                                -slip_rate[:,iloc,1],
                                -traction[:,iloc,1]/1e+6,
                                +traction[:,iloc,2]/1e+6))
        numpy.savetxt(fout, data, fmt='%14.6e')
        fout.close()

    return

# ----------------------------------------------------------------------
# MAIN FAULT

# Target coordinates are relative to faults intersection.
targets = numpy.array([[0.0, -10.0e+3,   0.0   ],
                       [0.0, -10.0e+3,  -5.0e+3],
                       [0.0, -10.0e+3, -10.0e+3],
                       [0.0, -10.0e+3, -15.0e+3],
                       [0.0,  -5.0e+3, -10.0e+3],
                       [0.0,   0.0,    -10.0e+3],
                       [0.0,   0.0,      0.0   ],
                       ])

extract("fault_main", targets)

# ----------------------------------------------------------------------
# STEPOVER FAULT

# Target coordinates are relative to faults intersection.
targets = numpy.array([[0.0,   0.0,      0.0],
                       [0.0,   0.0,    -10.0e+3],
                       [0.0,  +4.0e+3,  -5.0e+3],
                       [0.0,  +5.0e+3,   0.0   ],
                       [0.0,  +5.0e+3,  -5.0e+3],
                       [0.0,  +5.0e+3, -10.0e+3],
                       [0.0,  +5.0e+3, -15.0e+3],
                       [0.0,  +6.5e+3, -10.0e+3],
                       [0.0, +10.0e+3, -10.0e+3],
                       [0.0, +20.0e+3,   0.0   ],
                       [0.0, +20.0e+3, -10.0e+3],
                       ])

extract("fault_stepover", targets)


# End of file

#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# ----------------------------------------------------------------------
#

cell = "tet4"
dx = 100

inputRoot = "output/%s_%3dm-groundsurf" % (cell,dx)
outdir = "scecfiles/%s_%3dm/" % (cell,dx)

# ----------------------------------------------------------------------
import tables
import numpy
import time

# ----------------------------------------------------------------------
targets = numpy.array([[-3000.0, -12000.0, 0.0],
                       [-3000.0,  12000.0, 0.0]])


tolerance = 1.0e-6

h5 = tables.openFile("%s.h5" % inputRoot, 'r')
vertices = h5.root.geometry.vertices[:]
ntargets = targets.shape[0]
indices = []
for target in targets:
    dist = ( (vertices[:,0]-target[0])**2 + 
             (vertices[:,1]-target[1])**2 +
             (vertices[:,2]-target[2])**2 )**0.5
    min = numpy.min(dist)
    indices.append(numpy.where(dist <= min+tolerance)[0][0])

print "Indices: ", indices
print "Coordinates of selected points:\n",vertices[indices,:]


# Get datasets
disp = h5.root.vertex_fields.displacement[:]
vel = h5.root.vertex_fields.velocity[:]
timeStamps =  h5.root.time[:].ravel()
nsteps = timeStamps.shape[0]
dt = timeStamps[1] - timeStamps[0]

h5.close()

# Extract locations
disp = disp[:,indices,:]
vel = vel[:,indices,:]

# Write data
headerA = \
    "# problem = TPV205\n" + \
    "# author = Brad Aagaard\n" + \
    "# date = %s\n" % (time.asctime()) + \
    "# code = PyLith\n" + \
    "# code_version = 1.7.0a (scecdynrup branch)\n" + \
    "# element_size = %s m\n" % dx
headerB = \
    "# Time series in 7 columns of E14.6:\n" + \
    "# Column #1 = time (s)\n" + \
    "# Column #2 = horizontal fault-parallel displacement (m)\n" + \
    "# Column #3 = horizontal fault-parallel velocity (m/s)\n" + \
    "# Column #4 = vertical displacement (m)\n" + \
    "# Column #5 = vertical velocity (m/s)\n" + \
    "# Column #6 = horizontal fault-normal displacement (m)\n" + \
    "# Column #7 = horizontal fault-normal velocity (m/s)\n" + \
    "#\n" + \
    "# Data fields\n" + \
    "t h-disp h-vel v-disp v-vel n-disp n-vel\n" + \
    "#\n"

locHeader = "# location = %3.1f km off fault, %3.1f km along strike " \
    "and %3.1f km depth\n"
locName = "%+04dst%+04ddp%03d"

lengthScale = 1000.0
body = -targets[:,0] / lengthScale
strike = (targets[:,1]) / lengthScale
dip = (targets[:,2]) / lengthScale

for iloc in xrange(ntargets):
    pt = locName % (round(10*body[iloc]), 
                    round(10*strike[iloc]),
                    round(10*dip[iloc]))
    filename = "%sbody%s.dat" % (outdir, pt)
    fout = open(filename, 'w')
    fout.write(headerA)
    fout.write("# time_step = %14.6E\n" % dt)
    fout.write("# num_timesteps = %8d\n" % nsteps)
    fout.write(locHeader % (body[iloc], 
                            strike[iloc], 
                            dip[iloc]))
    fout.write(headerB)
    data = numpy.transpose((timeStamps,
                            +disp[:,iloc,1],
                            +vel[:,iloc,1],
                            -disp[:,iloc,2],
                            -vel[:,iloc,2],
                            -disp[:,iloc,0],
                            -vel[:,iloc,0]))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()

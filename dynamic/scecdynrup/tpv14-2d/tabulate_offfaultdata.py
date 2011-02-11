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
cell = "tri3"
dx = 100
dt = 0.05

inputRoot = "output/%s_%s_%3dm_gradient" % (sim, cell,dx)
outputRoot = "scecfiles/%s_%s_%3dm" % (sim, cell,dx)

# ----------------------------------------------------------------------
import tables
import numpy
import time

# ----------------------------------------------------------------------
targets = numpy.array([[-3000.0, -2000.0],
                       [+3000.0, -2000.0],
                       [-3000.0, +2000.0],
                       [ +600.0, +2000.0],
                       [+4200.0, +2000.0],
                       [-3000.0, +5000.0],
                       [+1400.0, +5000.0],
                       [+5900.0, +5000.0],
                       [-3000.0, +8000.0],
                       [+2300.0, +8000.0],
                       [+7600.0, +8000.0]])
targets[:,1] += 2000.0


h5 = tables.openFile("%s.h5" % (inputRoot), 'r')
vertices = h5.root.geometry.vertices[:]
ntargets = targets.shape[0]
indices = []
tolerance = 1.0e-6
for target in targets:
    dist = ( (vertices[:,0]-target[0])**2 + 
             (vertices[:,1]-target[1])**2 )**0.5
    min = numpy.min(dist)
    indices.append(numpy.where(dist <= min+tolerance)[0][0])

print "Indices: ", indices
print "Coordinates of selected points:\n",vertices[indices,:]

# Get datasets
disp = h5.root.vertex_fields.displacement[:]
vel = h5.root.vertex_fields.velocity[:]

# BEGIN TEMPORARY
#timeStamps =  h5.root.vertex_fields.time (not yet available)
ntimesteps = disp.shape[0]
timeStamps = numpy.linspace(0, dt*ntimesteps, ntimesteps, endpoint=True)
# END TEMPORARY

disp = disp[:,indices,:]
vel = vel[:,indices,:]
zero = numpy.zeros( (ntimesteps, 1), dtype=numpy.float64)

h5.close()

# Write data
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
timeScale = 1000.0
dip = 7.5
body = -targets[:,0] / lengthScale
strike = (targets[:,1] - 2000) / lengthScale

for iloc in xrange(ntargets):
    pt = locName % (round(10*body[iloc]), 
                    round(10*strike[iloc]),
                    round(10*dip))
    filename = "%s_body%s.dat" % (outputRoot, pt)
    fout = open(filename, 'w')
    fout.write(headerA)
    fout.write("# time_step = %14.6E\n" % dt)
    fout.write("# num_timesteps = %8d\n" % ntimesteps)
    fout.write(locHeader % (body[iloc], 
                            strike[iloc], 
                            dip))
    fout.write(headerB)
    data = numpy.transpose((timeStamps,
                            +disp[:,iloc,1],
                            +vel[:,iloc,1],
                            zero,
                            zero,
                            -disp[:,iloc,0],
                            -vel[:,iloc,0]))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()

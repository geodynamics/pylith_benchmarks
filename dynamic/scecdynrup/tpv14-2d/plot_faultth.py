#!/usr/bin/env python
#
# ======================================================================
#
#                           Brad T. Aagaard
#                        U.S. Geological Survey
#
# {LicenseText}
#
# ======================================================================
#

sim = "tpv14"
cell = "tri3"
dx = 50
dt = 0.05

# ======================================================================
import tables
import numpy
import pylab
from mypylab.Figure import Figure


inputRoot = "output/%s_%s_%03dm_gradient" % (sim, cell,dx)

targets = numpy.array([[0.0,   1800.0],
                       [0.0,   1900.0],
                       [0.0,   2000.0],
                       [0.0,   2100.0],
                       [0.0,   2200.0]])

# ----------------------------------------------------------------------
tolerance = 1.0e-6

h5 = tables.openFile("%s-%s.h5" % (inputRoot, "main_fault"), 'r')
vertices = h5.root.geometry.vertices[:]
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
slip = h5.root.vertex_fields.slip[:]
slip_rate = h5.root.vertex_fields.slip_rate[:]
traction = h5.root.vertex_fields.traction[:]

# BEGIN TEMPORARY
#time =  h5.root.vertex_fields.time (not yet available)
ntimesteps = slip.shape[0]
time = numpy.arange(0, dt*ntimesteps, dt)
# END TEMPORARY


nrows = 1
ncols = 3
irow = 1
icol = 1

fig = Figure(fontsize=8, color="lightbg")
fig.open(7.0, 7.25, margins=[[0.1, 0.15, 0.1],
                             [0.4, 0, 0.0]])

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(time, slip[:,indices,0])
icol += 1

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(time, slip[:,indices,1])
icol += 1

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(time, traction[:,indices,1])
icol += 1

pylab.show()


# End of file

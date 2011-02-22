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

sim = "tpv15"
cell = "tri3"
dx = 100
dt = 0.05

# ======================================================================
import tables
import numpy
import pylab
from mypylab.Figure import Figure


inputRoot = "output/%s_%s_%03dm_gradient" % (sim, cell,dx)

targets = numpy.array([[0.0,   2000.0],
                       [0.0,   2100.0],
                       [0.0,   2200.0],
                       [0.0,   2300.0],
                       [0.0,   2400.0],
                       [0.0,   2500.0],
                       [0.0,   2600.0],
                       [0.0,   2700.0],
                       [0.0,   2800.0],
                       [0.0,   2900.0],
                       [0.0,   3000.0],
])
targets[:,1] += 2*1000.0
#targets = numpy.array([[0.0,   -7500.0],
#                       [0.0,   -6000.0],
#                       [0.0,   -4500.0],
#                       ])

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
traction = h5.root.vertex_fields.traction[:] / 1.0e+6

imask = numpy.where(numpy.abs(traction[1,:,1]) < 1.0e-6)[0]
traction[:,imask,1] = 1.0

# BEGIN TEMPORARY
#time =  h5.root.vertex_fields.time (not yet available)
ntimesteps = slip.shape[0]
time = numpy.linspace(0, dt*ntimesteps, ntimesteps, endpoint=True)
# END TEMPORARY

h5.close()


nrows = 2
ncols = 2
irow = 1
icol = 1

fig = Figure(fontsize=8, color="lightbg")
fig.open(7.0, 7.25, margins=[[0.6, 0.6, 0.2],
                             [0.6, 0.5, 0.2]])

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(time, slip_rate[:,indices,0])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Slip Rate (m/s)")
icol += 1

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(time, -traction[:,indices,0]/traction[:,indices,1])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Shear/Normal Traction")
icol += 1

irow = 2
icol = 1
ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(time, -traction[:,indices,0])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Shear Traction (MPa)")
icol += 1

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(time, traction[:,indices,1])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Normal Traction (MPa)")
icol += 1

pylab.show()


print slip[ntimesteps-1,indices,0]

# End of file

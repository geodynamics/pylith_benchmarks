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

cell = "tri3"
dx = 200

inputRoot = "output/%s_%3dm_%s-fault" % (cell,dx,"gradient")

# ======================================================================
import tables
import numpy
import pylab
from mypylab.Figure import Figure

if dx == 200:
    targets = numpy.array([[0.0, -12000.0, 0.0],
                           [0.0,  -7600.0, 0.0],
                           [0.0,  -4400.0, 0.0],
                           [0.0,      0.0, 0.0],
                           [0.0,  +4400.0, 0.0],
                           [0.0,  +7600.0, 0.0],
                           [0.0, +12000.0, 0.0]])
elif dx == 100 or dx == 50:
    targets = numpy.array([[0.0, -12000.0, 0.0],
                           [0.0,  -7500.0, 0.0],
                           [0.0,  -4500.0, 0.0],
                           [0.0,      0.0, 0.0],
                           [0.0,  +4500.0, 0.0],
                           [0.0,  +7500.0, 0.0],
                           [0.0, +12000.0, 0.0]])
    
# ----------------------------------------------------------------------
tolerance = 1.0e-6

h5 = tables.openFile("%s.h5" % inputRoot, 'r')
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
timeStamps =  h5.root.time[:].ravel()
nsteps = timeStamps.shape[0]
dt = timeStamps[1] - timeStamps[0]

h5.close()


nrows = 3
ncols = 2
irow = 1
icol = 1

fig = Figure(fontsize=8, color="lightbg")
fig.open(7.0, 7.25, margins=[[0.6, 0.6, 0.2],
                             [0.6, 0.5, 0.2]])

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(timeStamps, slip_rate[:,indices,0])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Slip Rate (m/s)")
icol += 1

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(timeStamps, -traction[:,indices,0]/traction[:,indices,1])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Shear/Normal Traction")
icol += 1

irow = 2
icol = 1
ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(timeStamps, -traction[:,indices,0])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Shear Traction (MPa)")
icol += 1

ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(timeStamps, traction[:,indices,1])
ax.set_xlabel("Time (s)")
ax.set_ylabel("Normal Traction (MPa)")
icol += 1

irow = 3
icol = 1
ax = fig.axes(nrows, ncols, irow, icol)
ax.plot(-slip[:,:,0], -traction[:,:,0])
ax.set_xlabel("Slip (s)")
ax.set_ylabel("Shear Traction (MPa)")
icol += 1

pylab.show()


# End of file

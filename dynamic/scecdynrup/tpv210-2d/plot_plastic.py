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
cell = "tri3"
dx = 200

inputRoot = "output/%s_%s_%03dm-elastic" % (sim,cell,dx)

# ----------------------------------------------------------------------
import tables
import numpy
import pylab

# ----------------------------------------------------------------------
indices = [16108,16179,16143,16157]

h5 = tables.openFile("%s.h5" % inputRoot, 'r')
# Get datasets
plasticStrain = h5.root.cell_fields.plastic_strain[:]
totalStrain = h5.root.cell_fields.total_strain[:]
stress = h5.root.cell_fields.stress[:]
timeStamps =  h5.root.time[:].ravel()
nsteps = timeStamps.shape[0]

h5.close()

# Extract locations
plasticStrain = plasticStrain[:,indices,:]
totalStrain = totalStrain[:,indices,:]
stress = stress[:,indices,:]/1.0e+6

ii = 0

ax = pylab.subplot(3, 2, 1)
pylab.plot(timeStamps, totalStrain[:,ii,0], 'b-',
           timeStamps, plasticStrain[:,ii,0], 'r-')
ax.set_title("Total Strain, Plastic Strain")

ax = pylab.subplot(3, 2, 3)
pylab.plot(timeStamps, totalStrain[:,ii,1], 'b-',
           timeStamps, plasticStrain[:,ii,1], 'r-')

ax = pylab.subplot(3, 2, 5)
pylab.plot(timeStamps, totalStrain[:,ii,2], 'b-',
           timeStamps, plasticStrain[:,ii,2], 'r-')
ax.set_xlabel("Time (s)")

ax = pylab.subplot(3, 2, 2)
pylab.plot(timeStamps, stress[:,ii,0], 'b-')
ax.set_title("Stress (MPa)")

ax = pylab.subplot(3, 2, 4)
pylab.plot(timeStamps, stress[:,ii,1], 'b-')

ax = pylab.subplot(3, 2, 6)
pylab.plot(timeStamps, stress[:,ii,2], 'b-')
ax.set_xlabel("Time (s)")

pylab.show()

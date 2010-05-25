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

cell = "hex8"
dx = 200
dt = 0.05

outputRoot = "output/%s_%3dm" % (cell,dx)
outdir = "scecfiles/%s_%3dm/" % (cell,dx)

import numpy
import time

from pylith.utils.VTKDataReader import VTKDataReader

# ----------------------------------------------------------------------
timestamps = numpy.arange(50,12001,50)
    

reader = VTKDataReader()
tolerance = 1.0e-6

filename = "%s-fault_t%05d.vtk" % (outputRoot,timestamps[0])
data = reader.read(filename)
vertices = numpy.array(data['vertices'])
ntargets = vertices.shape[0]

# Extract values
nsteps = timestamps.shape[0]
slip_rate = numpy.zeros((nsteps,ntargets,3))  # 3-D array (time, targets, components)
itime = 0
for timestamp in timestamps:
    filename = "%s-fault_t%05d.vtk" % (outputRoot,timestamp)
    data = reader.read(filename)
    fields = data['vertex_fields']
    slip_rate[itime,:,:] = fields['slip_rate'][:,:].squeeze()
    itime += 1

nVertices = slip_rate.shape[1]
ruptime = numpy.zeros((nVertices))
ruptime = 1e+9

ruptimeIndices = (slip_rate[:,:,0]>0.001).nonzero()[0]


# Write data
headerA = \
    "# problem = TPV205\n" + \
    "# author = Surendra N. Somala\n" + \
    "# date = %s\n" % (time.asctime()) + \
    "# code = PyLith\n" + \
    "# code_version = 1.5.0a\n" + \
    "# element_size = %s\n" % dx + \
    "# Contour data in 3 columns of E14.6:\n" + \
    "# Column #1 = Distance along strike from hypocenter (m)\n" + \
    "# Column #2 = Distance down-dip from surface (m)\n" + \
    "# Column #3 = Rupture time (s)\n" + \
    "#\n" + \
    "# Data fields\n" + \
    "j k t\n" + \
    "#\n"


lengthScale = 1000.0
timeScale = 1000.0
distDip = -vertices[:,2] / lengthScale
distStrike = vertices[:,0] / lengthScale
time =  timestamps / timeScale
print "time", time

filename = "%s_ruptime.dat" % (outdir)
fout = open(filename, "w")
fout.write(headerA)
print "distStrike.shape", distStrike.shape
print "distDip.shape", distDip.shape
print "ruptimeIndices.shape", ruptimeIndices.shape
data = numpy.transpose((distStrike, distDip, ruptimeIndices))
numpy.savetxt(fout, data, fmt='%14.6e')
fout.close()

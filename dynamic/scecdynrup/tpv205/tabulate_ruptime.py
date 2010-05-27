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
threshold = 0.001 # threshold for detecting slip has started

filename = "%s-fault_t%05d.vtk" % (outputRoot,timestamps[0])
data = reader.read(filename)
vertices = numpy.array(data['vertices'])
npts = vertices.shape[0]

# Extract values
nsteps = timestamps.shape[0]

# Set default rupture time to a large value (1.0e+30)
rupTime = 1.0e+9 * numpy.ones( (npts,), dtype=numpy.float64)

# Create buffer for current rupture time
tmpTime = numpy.zeros( (npts,), dtype=numpy.float64)

itime = 0
for timestamp in timestamps:
    t = (itime+1)*dt # itime=0, t=dt

    # Get slip rate field
    filename = "%s-fault_t%05d.vtk" % (outputRoot,timestamp)
    data = reader.read(filename)
    fields = data['vertex_fields']
    slipRate = fields['slip_rate'][:,:].squeeze()

    # Compute magnitude of slip rate
    slipRateMag = (slipRate[:,0]**2 + slipRate[:,1]**2)**0.5

    # Set rupture time at locations where threshold is exceeded
    tmpTime[slipRateMag > threshold] = t

    # Get indicates where current time is less than current rupture
    # time (this is only the locations that just started slipping)
    indices = numpy.where(tmpTime < rupTime)[0]

    rupTime[indices] = t

    itime += 1

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
distDip = -vertices[:,2]
distStrike = vertices[:,0]
time =  timestamps / timeScale
print "time", time

filename = "%sruptime.dat" % (outdir)
fout = open(filename, "w")
fout.write(headerA)
data = numpy.transpose((distStrike, distDip, rupTime))
numpy.savetxt(fout, data, fmt='%14.6e')
fout.close()

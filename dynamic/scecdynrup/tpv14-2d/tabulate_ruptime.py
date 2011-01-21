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

cell = "quad4"
dx = 100
dt = 0.05

outputRoot = "output/%s_%3dm_%s" % (cell,dx,"refine")
outdir = "scecfiles/%s_%3dm_%s/" % (cell,dx,"refine")

import numpy
import time

from pylith.utils.VTKDataReader import VTKDataReader

# MAIN FAULT----------------------------------------------------------------------
timestamps = numpy.arange(50,12001,50)
    

reader = VTKDataReader()
threshold = 0.001 # threshold for detecting slip has started

filename = "%s-mainFault_t%05d.vtk" % (outputRoot,timestamps[0])
data = reader.read(filename)
vertices = numpy.array(data['vertices'])
npts = vertices.shape[0]

# Extract values
nsteps = timestamps.shape[0]

# Set default rupture time to a large value (1.0e+9)
rupTime = 1.0e+9 * numpy.ones( (npts,), dtype=numpy.float64)
#rupTime = numpy.zeros( (npts,), dtype=numpy.float64)

# Create buffer for current rupture time
tmpTime = numpy.zeros( (npts,), dtype=numpy.float64)

itime = 0
for timestamp in timestamps:
    t = (itime+1)*dt # itime=0, t=dt

    # Get slip rate field
    filename = "%s-mainFault_t%05d.vtk" % (outputRoot,timestamp)
    data = reader.read(filename)
    fields = data['vertex_fields']
    slipRate = fields['slip_rate'][:,:].squeeze()

    # Compute magnitude of slip rate
    slipRateMag = (slipRate[:,0]**2 + slipRate[:,1]**2)**0.5

    # Set rupture time at locations where threshold is exceeded
    tmpTime[slipRateMag > threshold] = t

    #print "slipRateMag \n", slipRateMag
    #print "slipRateMag > threshold \n ", slipRateMag > threshold

    #print "tmpTime \n", tmpTime[1:50]
    #print "time", t

    # Get indicates where current time is less than current rupture
    # time (this is only the locations that just started slipping)
    #indices = numpy.where((tmpTime < rupTime) and (rupTime < 0.00001))[0]
    #indices = ((tmpTime < rupTime) & (rupTime < testarr))
    indices = numpy.where((tmpTime < rupTime) & (tmpTime > 0.00001))[0]

    #print "indices \n", indices[1:200]


    rupTime[indices] = t

    #print "rupTime \n", rupTime[1:200]

    itime += 1

# print "rupTime \n", rupTime
# rupTime[rupTime < 0.00001] = 1.0e+9

# Write data
headerA = \
    "# problem = TPV14-2D\n" + \
    "# author = Surendra N. Somala\n" + \
    "# code = PyLith\n" + \
    "# code_version = 1.5.1\n" + \
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
distDip = numpy.hstack((vertices[:,2], 15000*(vertices[:,2]+1)))
distStrike = numpy.hstack(( (vertices[:,1] - 2000), (vertices[:,1] - 2000) ))
rupTime1 = numpy.hstack((rupTime, rupTime))
time =  timestamps / timeScale
print "time", time

filename = "%scplot_main.dat" % (outdir)
fout = open(filename, "w")
fout.write(headerA)
data = numpy.transpose((distStrike, distDip, rupTime1))
numpy.savetxt(fout, data, fmt='%14.6e')
fout.close()





# BRANCH FAULT----------------------------------------------------------------------
timestamps = numpy.arange(50,12001,50)
    

reader = VTKDataReader()
threshold = 0.001 # threshold for detecting slip has started

filename = "%s-branchFault_t%05d.vtk" % (outputRoot,timestamps[0])
data = reader.read(filename)
vertices = numpy.array(data['vertices'])
npts = vertices.shape[0]

# Extract values
nsteps = timestamps.shape[0]

# Set default rupture time to a large value (1.0e+9)
rupTime = 1.0e+9 * numpy.ones( (npts,), dtype=numpy.float64)
#rupTime = numpy.zeros( (npts,), dtype=numpy.float64)

# Create buffer for current rupture time
tmpTime = numpy.zeros( (npts,), dtype=numpy.float64)

itime = 0
for timestamp in timestamps:
    t = (itime+1)*dt # itime=0, t=dt

    # Get slip rate field
    filename = "%s-branchFault_t%05d.vtk" % (outputRoot,timestamp)
    data = reader.read(filename)
    fields = data['vertex_fields']
    slipRate = fields['slip_rate'][:,:].squeeze()

    # Compute magnitude of slip rate
    slipRateMag = (slipRate[:,0]**2 + slipRate[:,1]**2)**0.5

    # Set rupture time at locations where threshold is exceeded
    tmpTime[slipRateMag > threshold] = t

    #print "slipRateMag \n", slipRateMag
    #print "slipRateMag > threshold \n ", slipRateMag > threshold

    #print "tmpTime \n", tmpTime[1:50]
    #print "time", t

    # Get indicates where current time is less than current rupture
    # time (this is only the locations that just started slipping)
    #indices = numpy.where((tmpTime < rupTime) and (rupTime < 0.00001))[0]
    #indices = ((tmpTime < rupTime) & (rupTime < testarr))
    indices = numpy.where((tmpTime < rupTime) & (tmpTime > 0.00001))[0]

    #print "indices \n", indices[1:200]


    rupTime[indices] = t

    #print "rupTime \n", rupTime[1:200]

    itime += 1

# print "rupTime \n", rupTime
# rupTime[rupTime < 0.00001] = 1.0e+9

# Write data
headerA = \
    "# problem = TPV14-2D\n" + \
    "# author = Surendra N. Somala\n" + \
    "# code = PyLith\n" + \
    "# code_version = 1.5.1\n" + \
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
distDip = numpy.hstack((vertices[:,2], 15000*(vertices[:,2]+1)))
distStrike = numpy.hstack(( (vertices[:,1] - 2000), (vertices[:,1] - 2000) ))
rupTime1 = numpy.hstack((rupTime, rupTime))
time =  timestamps / timeScale
print "time", time

filename = "%scplot_branch.dat" % (outdir)
fout = open(filename, "w")
fout.write(headerA)
data = numpy.transpose((distStrike, distDip, rupTime1))
numpy.savetxt(fout, data, fmt='%14.6e')
fout.close()

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

outputRoot = "output/quad4_100m"
outdir = "scecfiles/quad4_100m/"
dx = 100

import numpy
import time

from pylith.utils.VTKDataReader import VTKDataReader
from numpy import *

# ----------------------------------------------------------------------
def feq(a,b):
    if numpy.abs(a-b)<0.0001:
        return 1
    else:
        return 0

# ----------------------------------------------------------------------
# Extract Off Fault stations data ( Displacements and Velocities )
# ----------------------------------------------------------------------
nfileNames = numpy.arange(1,1202,5)
filename = "%s_t%04d.vtk" % (outputRoot,nfileNames[0])

dt = 0.05
nsteps = len(nfileNames)
print nsteps

fieldNames = ["displacement","velocity"]
reader = VTKDataReader()
data = reader.read(filename)
values = numpy.array(data['vertices'])
(nvertices, spaceDim) = values.shape

x_OffFltStat = numpy.array([3000.0, 3000.0])
y_OffFltStat = numpy.array([-12000.0, 12000.0]) # CHECK THESE VALUES
Index_OffFltStat = numpy.zeros(2)

# Find the indices of On Fault Stations
nFltStat = -1
for i in xrange(nvertices):
    if (feq(values[i,0],x_OffFltStat[0]) and feq(values[i,1],y_OffFltStat[0])) or \
       (feq(values[i,0],x_OffFltStat[1]) and feq(values[i,1],y_OffFltStat[1])):
        nFltStat += 1
        Index_OffFltStat[nFltStat] = i

Index_OffFltStat = numpy.int_(Index_OffFltStat)
print "Off-fault indices", Index_OffFltStat

# Extract values
disp = numpy.zeros((nsteps,2,3))  # 3-D array (ntime, nstats, ncomponents)
vel = numpy.zeros((nsteps,2,3))
nFile = -1
for i in nfileNames:
    nFile += 1
    filename = "%s_t%04d.vtk" % (outputRoot,i)
    data = reader.read(filename)
    nField = 0
    for name in fieldNames:
        nField += 1
        values = data['vertex_fields'][name]
        if nField == 1:
            disp[nFile,:,:] = values[Index_OffFltStat,:]
        elif nField == 2:
            vel[nFile,:,:] = values[Index_OffFltStat,:]


# ----------------------------------------------------------------------
# Extract Off Fault stations data ( Displacements and Velocities )
# ----------------------------------------------------------------------

headerA = \
    "# problem = TPV205\n" + \
    "# author = BradAagaard\n" + \
    "# date = %s\n" % (time.asctime()) + \
    "# code = PyLith\n" + \
    "# code_version = 1.4.3\n" + \
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
timeScale = 100.0
dip = 7.5
body = x_OffFltStat[:] / lengthScale
strike = y_OffFltStat[:] / lengthScale
time = (nfileNames[:] - 1) / timeScale
print "time", time

nlocs = disp.shape[1]
for iloc in xrange(nlocs):
    pt = locName % (round(10*body[iloc]), 
                    round(10*strike[iloc]),
                    round(10*dip))
    filename = "%sbody%s.dat" % (outdir, pt)
    fout = open(filename, 'w')
    fout.write(headerA)
    fout.write("# time_step = %14.6E\n" % dt)
    fout.write("# num_timesteps = %8d\n" % nsteps)
    fout.write(locHeader % (body[iloc], 
                             strike[iloc], 
                             dip))
    fout.write(headerB)
    data = numpy.transpose((time,
                            +disp[:,iloc,1],
                            +vel[:,iloc,1],
                            -disp[:,iloc,2],
                            -vel[:,iloc,2],
                            -disp[:,iloc,0],
                            -vel[:,iloc,0]))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()

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
# Extract On Fault stations data ( Slip, Slip Rate, Tractions )
# ----------------------------------------------------------------------
nfileNames = numpy.arange(1,1202,5)
filename = "%s-fault_t%04d.vtk" % (outputRoot,nfileNames[0])

dt = 0.05
nsteps = len(nfileNames)
print nsteps

fieldNames = ["slip","slip_rate","traction"]
reader = VTKDataReader()
data = reader.read(filename)
values = numpy.array(data['vertices'])
(nvertices, spaceDim) = values.shape

x_OnFltStat = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
#y_OnFltStat = numpy.array([-12000.0, -7600.0, -4400.0, 0.0, 4400.0, 7600.0, 12000.0]) # CHECK THESE VALUES
y_OnFltStat = numpy.array([-12000.0, -7500.0, -4500.0, 0.0, 4500.0, 7500.0, 12000.0]) # CHECK THESE VALUES
Index_OnFltStat = numpy.zeros(7)

# Find the indices of On Fault Stations
nFltStat = -1
for i in xrange(nvertices):
    if feq(values[i,1],y_OnFltStat[0]) or \
       feq(values[i,1],y_OnFltStat[1]) or \
       feq(values[i,1],y_OnFltStat[2]) or \
       feq(values[i,1],y_OnFltStat[3]) or \
       feq(values[i,1],y_OnFltStat[4]) or \
       feq(values[i,1],y_OnFltStat[5]) or \
       feq(values[i,1],y_OnFltStat[6]):
        nFltStat += 1
        Index_OnFltStat[nFltStat] = i

Index_OnFltStat = numpy.int_(Index_OnFltStat)
print "On-Fault indices", Index_OnFltStat

# Extract values
slip = numpy.zeros((nsteps,7,3))  # 3-D array (ntime, nstats, ncomponents)
slip_rate = numpy.zeros((nsteps,7,3))
traction = numpy.zeros((nsteps,7,3))
nFile = -1
for i in nfileNames:
    nFile += 1
    filename = "%s-fault_t%04d.vtk" % (outputRoot,i)
    data = reader.read(filename)
    nField = 0
    for name in fieldNames:
        nField += 1
        values = data['vertex_fields'][name]
        if nField == 1:
            slip[nFile,:,:] = values[Index_OnFltStat,:]
        elif nField == 2:
            slip_rate[nFile,:,:] = values[Index_OnFltStat,:]
        elif nField == 3:
            traction[nFile,:,:] = values[Index_OnFltStat,:]



# ----------------------------------------------------------------------
# Write On Fault stations data to file ( Slip, Slip Rate, Tractions )
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
    "# Column #2 = horizontal right-lateral slip (m)\n" + \
    "# Column #3 = horizontal right-lateral slip rate (m/s)\n" + \
    "# Column #4 = horizontal right-lateral shear stress (MPa)\n" + \
    "# Column #5 = vertical up-dip slip (m)\n" + \
    "# Column #6 = vertical up-dip slip-rate (m/s)\n" + \
    "# Column #7 = vertical up-dip shear stress (MPa)\n" + \
    "#\n" + \
    "# Data fields\n" + \
    "t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress\n" + \
    "#\n"

locHeader = "# location = on fault, %3.1f km along strike and %3.1f km depth\n"
locName = "st%+04ddp%03d"

lengthScale = 1000.0
timeScale = 100.0
dip = 7.5
strike = y_OnFltStat[:] / lengthScale
time = (nfileNames[:] - 1) / timeScale
print "time", time

# Write data
nlocs = slip.shape[1]
for iloc in xrange(nlocs):
    pt = locName % (round(10*strike[iloc]), 
                    round(10*dip))
    filename = "%sfault%s.dat" % (outdir,pt)
    fout = open(filename, 'w');
    fout.write(headerA)
    fout.write("# time_step = %14.6E\n" % dt)
    fout.write("# num_timesteps = %8d\n" % nsteps)
    fout.write(locHeader % (strike[iloc], dip))
    fout.write(headerB)
    data = numpy.transpose((time, 
                            -slip[:,iloc,0],
                            -slip_rate[:,iloc,0],
                            -traction[:,iloc,0]/1e+6,
                            +slip[:,iloc,1],
                            +slip_rate[:,iloc,1],
                            +traction[:,iloc,1]/1e+6))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()

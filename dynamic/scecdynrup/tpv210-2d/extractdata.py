outputRoot = "output/quad4_200m"

import numpy

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
nfileNames = numpy.arange(1,1201,5)
filename = "%s-fault_t%04d.vtk" % (outputRoot,nfileNames[0])
fieldNames = ["slip","slip_rate","traction"]
reader = VTKDataReader()
data = reader.read(filename)
values = numpy.array(data['vertices'])
(nvertices, spaceDim) = values.shape

x_OnFltStat = numpy.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
y_OnFltStat = numpy.array([-12000.0, -7600.0, -4400.0, 0.0, 4400.0, 7600.0, 12000.0]) # CHECK THESE VALUES
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
slip = numpy.zeros((240,7,3))  # 3-D array (ntime, nstats, ncomponents)
slip_rate = numpy.zeros((240,7,3))
traction = numpy.zeros((240,7,3))
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
#        elif nField == 2:
#            slip_rate[nFile,:,:] = values[Index_OnFltStat,:]
        elif nField == 3:
            traction[nFile,:,:] = values[Index_OnFltStat,:]


# ----------------------------------------------------------------------
# Extract Off Fault stations data ( Displacements and Velocities )
# ----------------------------------------------------------------------
nfileNames = numpy.arange(1,1201,5)
filename = "%s_t%04d.vtk" % (outputRoot,nfileNames[0])
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
disp = numpy.zeros((240,2,3))  # 3-D array (ntime, nstats, ncomponents)
vel = numpy.zeros((240,2,3))
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

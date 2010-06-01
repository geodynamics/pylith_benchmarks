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

# outputRoot = "output/%s_%3dm_%s" % (cell,dx,"refine")
# outdir = "scecfiles/%s_%3dm_%s/" % (cell,dx,"refine")

outputRoot = "output/%s_%3dm" % (cell,dx)
outdir = "scecfiles/%s_%3dm/" % (cell,dx)

import numpy
import time

from pylith.utils.VTKDataReader import VTKDataReader

# ----------------------------------------------------------------------
timestamps = numpy.arange(50,15001,50)
targets = numpy.array([[ 0.0000000, 0.0000000, 0.0000000],
                       [ 0.0000000, 4500.0000000, 0.0000000],
                       [ 0.0000000, 12000.0000000, 0.0000000],
                       [ -750.0000000, 0.0000000, -1299.0381057],
                       [ -1500.0000000, 0.0000000, -2598.0762114],
                       [ -2250.0000000, 0.0000000, -3897.1143170],
                       [ -3750.0000000, 0.0000000, -6495.1905284],
                       [ -3750.0000000, 4500.0000000, -6495.1905284],
                       [ -3750.0000000, 12000.0000000, -6495.1905284],
                       [ -6000.0000000, 0.0000000, -10392.3048454]])
    

reader = VTKDataReader()
tolerance = 1.0e-6

# Get vertices and find indices of target locations
filename = "%s-fault_t%05d.vtk" % (outputRoot,timestamps[0])
data = reader.read(filename)

vertices = numpy.array(data['vertices'])
ntargets = targets.shape[0]
indices = []
for target in targets:
    dist = ( (vertices[:,0]-target[0])**2 + 
             (vertices[:,1]-target[1])**2 +
             (vertices[:,2]-target[2])**2 )**0.5
    min = numpy.min(dist)
    indices.append(numpy.where(dist <= min+tolerance)[0][0])

print "Indices", indices
print "Coordinates of selected points:",vertices[indices,:]

# Extract values
nsteps = timestamps.shape[0]
slip = numpy.zeros((nsteps,ntargets,3))  # 3-D array (time, targets, components)
slip_rate = numpy.zeros((nsteps,ntargets,3))
traction = numpy.zeros((nsteps,ntargets,3))
itime = 0
for timestamp in timestamps:
    filename = "%s-fault_t%05d.vtk" % (outputRoot,timestamp)
#    print "filename", filename
    data = reader.read(filename)
    fields = data['vertex_fields']
    slip[itime,0:ntargets,:] = fields['slip'][indices,:].squeeze()
    slip_rate[itime,0:ntargets,:] = fields['slip_rate'][indices,:].squeeze()
    traction[itime,0:ntargets,:] = fields['traction'][indices,:].squeeze()
    itime += 1


# Write data
headerA = \
    "# problem = TPV210\n" + \
    "# author = Surendra N. Somala\n" + \
    "# date = %s\n" % (time.asctime()) + \
    "# code = PyLith\n" + \
    "# code_version = 1.5.0a\n" + \
    "# element_size = %s\n" % dx
headerB = \
    "# Time series in 8 columns of E14.6:\n" + \
    "# Column #1 = time (s)\n" + \
    "# Column #2 = horizontal right-lateral slip (m)\n" + \
    "# Column #3 = horizontal right-lateral slip rate (m/s)\n" + \
    "# Column #4 = horizontal right-lateral shear stress (MPa)\n" + \
    "# Column #5 = vertical up-dip slip (m)\n" + \
    "# Column #6 = vertical up-dip slip-rate (m/s)\n" + \
    "# Column #7 = vertical up-dip shear stress (MPa)\n" + \
    "# Column #8 = normal stress (MPa)\n" + \
    "#\n" + \
    "# Data fields\n" + \
    "t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress n-stress \n" + \
    "#\n"

locHeader = "# location = on fault, %3.1f km along strike and %3.1f km depth\n"
locName = "st%03ddp%03d"

lengthScale = 1000.0
timeScale = 1000.0
dip = -2*targets[:,0] / lengthScale
strike = targets[:,1] / lengthScale
time =  timestamps / timeScale
print "time", time

for iloc in xrange(ntargets):
    pt = locName % (round(10*strike[iloc]), 
                    round(10*dip[iloc]))
    filename = "%sfault%s.dat" % (outdir,pt)
    fout = open(filename, 'w');
    fout.write(headerA)
    fout.write("# time_step = %14.6E\n" % dt)
    fout.write("# num_timesteps = %8d\n" % nsteps)
    fout.write(locHeader % (strike[iloc], dip[iloc]))
    fout.write(headerB)
    data = numpy.transpose((time, 
                            -slip[:,iloc,0],
                            -slip_rate[:,iloc,0],
                            -traction[:,iloc,0]/1e+6,
                            slip[:,iloc,1],
                            slip_rate[:,iloc,1],
                            traction[:,iloc,1]/1e+6,
                            traction[:,iloc,2]/1e+6))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()

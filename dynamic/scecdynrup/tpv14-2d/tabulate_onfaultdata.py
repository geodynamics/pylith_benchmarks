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

cell = "tri3"
dx = 100
dt = 0.05

outputRoot = "output/%s_%3dm_%s" % (cell,dx,"refine")
outdir = "scecfiles/%s_%3dm_%s/" % (cell,dx,"refine")

import numpy
import time

from pylith.utils.VTKDataReader import VTKDataReader

# ----------------------------------------------------------------------
timestamps = numpy.arange(50,12001,50)
#if dx == 200:
#    targets = numpy.array([[0.0, -12000.0, 0.0],
#                           [0.0,  -7600.0, 0.0],
#                           [0.0,  -4400.0, 0.0],
#                           [0.0,      0.0, 0.0],
#                           [0.0,  +4400.0, 0.0],
#                           [0.0,  +7600.0, 0.0],
#                           [0.0, +12000.0, 0.0]])
#elif dx == 100:
    
targets_main = numpy.array([[0.0,  -2000.0, 0.0],
                            [0.0,  +2000.0, 0.0],
                            [0.0,  +5000.0, 0.0],
                            [0.0,  +9000.0, 0.0]])
targets_main[:,1] = targets_main[:,1] + 2000.0


reader = VTKDataReader()
tolerance = 1.0e-6

# Get vertices and find indices of target locations on MAIN Fault
targets = targets_main
filename = "%s-mainFault_t%05d.vtk" % (outputRoot,timestamps[0])
data = reader.read(filename)

vertices = numpy.array(data['vertices'])
ntargets = targets.shape[0]
indices = []
for target in targets:
    dist = ( (vertices[:,0]-target[0])**2 + 
             (vertices[:,1]-target[1])**2 +
             (vertices[:,2]-target[2])**2 )**0.5
    min = numpy.min(dist)
    indices.append(numpy.where(dist <= min+tolerance)[0])

print "Indices", indices
print "Coordinates of selected points on Main Fault:",vertices[indices,:]

# Extract values of MAIN fault
nsteps = timestamps.shape[0]
slip = numpy.zeros((nsteps,ntargets,3))  # 3-D array (time, targets, components)
slip_rate = numpy.zeros((nsteps,ntargets,3))
traction = numpy.zeros((nsteps,ntargets,3))
itime = 0
for timestamp in timestamps:
    filename = "%s-mainFault_t%05d.vtk" % (outputRoot,timestamp)
    data = reader.read(filename)
    fields = data['vertex_fields']
    slip[itime,0:ntargets,:] = fields['slip'][indices,:].squeeze()
    slip_rate[itime,0:ntargets,:] = fields['slip_rate'][indices,:].squeeze()
    traction[itime,0:ntargets,:] = fields['traction'][indices,:].squeeze()
    itime += 1


# Write data of MAIN fault
headerA = \
    "# problem = TPV14-2D\n" + \
    "# author = Surendra N. Somala\n" + \
    "# code = PyLith\n" + \
    "# code_version = 1.5.1\n" + \
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
    "# Column #8 = normal stress (MPa)\n" + \
    "#\n" + \
    "# Data fields\n" + \
    "t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress n-stress\n" + \
    "#\n"

locHeader = "# location = on fault, %3.1f km along strike and %3.1f km depth\n"
locName = "st%+04ddp%03d"

lengthScale = 1000.0
timeScale = 1000.0
dip = 7.5
strike = (targets[:,1] - 2000) / lengthScale
time =  timestamps / timeScale
print "time", time

for iloc in xrange(ntargets):
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
                            +slip[:,iloc,2],
                            +slip_rate[:,iloc,2],
                            +traction[:,iloc,2]/1e+6,
                            +traction[:,iloc,1]/1e+6))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()





targets_branch = numpy.array([[0.0,  +2000.0, 0.0],
                              [0.0,  +5000.0, 0.0],
                              [0.0,  +9000.0, 0.0]])
targets_branch[:,1] = targets_branch[:,1] + 2000.0



# Get vertices and find indices of target locations on BRANCH Fault
targets = targets_branch
filename = "%s-branchFault_t%05d.vtk" % (outputRoot,timestamps[0])
data = reader.read(filename)

vertices = numpy.array(data['vertices'])
ntargets = targets.shape[0]
indices = []
for target in targets:
    dist = ( (vertices[:,0]-target[0])**2 + 
             (vertices[:,1]-target[1])**2 +
             (vertices[:,2]-target[2])**2 )**0.5
    min = numpy.min(dist)
    indices.append(numpy.where(dist <= min+tolerance)[0])

print "Indices", indices
print "Coordinates of selected points on Branch Fault:",vertices[indices,:]



# Extract values of BRANCH fault
nsteps = timestamps.shape[0]
slip = numpy.zeros((nsteps,ntargets,3))  # 3-D array (time, targets, components)
slip_rate = numpy.zeros((nsteps,ntargets,3))
traction = numpy.zeros((nsteps,ntargets,3))
itime = 0
for timestamp in timestamps:
    filename = "%s-branchFault_t%05d.vtk" % (outputRoot,timestamp)
    data = reader.read(filename)
    fields = data['vertex_fields']
    slip[itime,0:ntargets,:] = fields['slip'][indices,:].squeeze()
    slip_rate[itime,0:ntargets,:] = fields['slip_rate'][indices,:].squeeze()
    traction[itime,0:ntargets,:] = fields['traction'][indices,:].squeeze()
    itime += 1


# Write data of BRANCH fault
headerA = \
    "# problem = TPV14-2D\n" + \
    "# author = Surendra N. Somala\n" + \
    "# code = PyLith\n" + \
    "# code_version = 1.5.1\n" + \
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
    "# Column #8 = normal stress (MPa)\n" + \
    "#\n" + \
    "# Data fields\n" + \
    "t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress n-stress\n" + \
    "#\n"

locHeader = "# location = on fault, %3.1f km along strike and %3.1f km depth\n"
locName = "st%+04ddp%03d"

lengthScale = 1000.0
timeScale = 1000.0
dip = 7.5
strike = (targets[:,1] - 2000) / lengthScale
time =  timestamps / timeScale
print "time", time

for iloc in xrange(ntargets):
    pt = locName % (round(10*strike[iloc]), 
                    round(10*dip))
    filename = "%sbranch%s.dat" % (outdir,pt)
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
                            +slip[:,iloc,2],
                            +slip_rate[:,iloc,2],
                            +traction[:,iloc,2]/1e+6,
                            +traction[:,iloc,1]/1e+6))
    numpy.savetxt(fout, data, fmt='%14.6e')
    fout.close()


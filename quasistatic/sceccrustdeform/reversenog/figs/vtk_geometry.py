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

from enthought.tvtk.api import tvtk
import numpy

# ----------------------------------------------------------------------
def domain():
    l = 24.0
    domain = tvtk.CubeSource()
    domain.set_bounds(0, l, 0, l, -l, 0.0)
    return domain.get_output()

# ----------------------------------------------------------------------
def fault(showTaper=False):
    vertices = numpy.array(
        [ [4.0,  0.0,   0.0], # 0
          [4.0, 12.0,   0.0], # 1
          [4.0, 16.0,   0.0], # 2
          [16.0,  0.0, -12.0], # 3
          [16.0, 12.0, -12.0], # 4
          [20.0,  0.0, -16.0], # 5
          [20.0, 12.0, -16.0], # 6
          [20.0, 16.0, -16.0] ], # 7
        dtype=numpy.float32)
    
    # Setup VTK vertices
    if not showTaper:
        polys = numpy.array(
            [ [0, 3, 1],
              [1, 3, 4],
              [3, 5, 4],
              [4, 5, 6],
              [1, 6, 2],
              [2, 6, 7] ],
            dtype=numpy.int32)
        
        # Setup VTK simplices
        data = [{'name': "fault",
                 'object': tvtk.PolyData(points=vertices, polys=polys)}]
    else:
        polys = numpy.array(
            [ [0, 3, 1],
              [1, 3, 4] ],
            dtype=numpy.int32)
        polysTaper = numpy.array(
            [ [3, 5, 4],
              [4, 5, 6],
              [1, 6, 2],
              [2, 6, 7] ],
            dtype=numpy.int32)
        
        data= [{'name': "fault",
                'object': tvtk.PolyData(points=vertices, polys=polys)},
               {'name': "taper",
                'object': tvtk.PolyData(points=vertices, polys=polysTaper)}]
    return data


# ----------------------------------------------------------------------
def materials():
    l = 24.0
    elastic = tvtk.CubeSource()
    elastic.set_bounds(0, l, 0, l, -l/2.0, 0.0)
    viscoelastic = tvtk.CubeSource()
    viscoelastic.set_bounds(0, l, 0, l, -l, -l/2.0)
    return [{'name': "elastic",
             'object': elastic.get_output()},
            {'name': "viscoelastic",
            'object': viscoelastic.get_output()}]

# ----------------------------------------------------------------------
def setCamera(camera):
    dist = 67.0
    angle = 40.0
    elev = 30.0
    azimuth = 35.0
    clipRange = numpy.array( [5, 100] )
    ptTo = numpy.array( [6.0, 12.0, -19] )
    ptFrom = ptTo + numpy.array( [0.0, -dist, 0.0])
    
    camera.view_angle = angle
    camera.view_up = (0,0,1)
    camera.focal_point = ptTo
    camera.position = ptFrom
    camera.elevation(elev)
    camera.azimuth(azimuth)
    camera.clipping_range = clipRange
    return

    
# ----------------------------------------------------------------------
def setWindow(maya):
    return

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

sim = "tpv14_tri3_100m_gradient"
tBegin = 0.0
tEnd = 6.01
dt = 0.2
exaggeration = 0.1

# ======================================================================
from enthought.mayavi.plugins.app import Mayavi
from enthought.mayavi.sources.vtk_data_source import VTKDataSource
from enthought.tvtk.api import tvtk
import numpy

# ----------------------------------------------------------------------
class SurfData:

  def __init__(self):
    """
    """
    return


  def read(self):
    """
    """
    import tables
    import numpy
    import math

    filename = "output/%s.h5" % sim
    h5 = tables.openFile(filename, 'r')

    self.cells = h5.root.topology.cells[:]
    (ncells, ncorners) = self.cells.shape
    vertices = h5.root.geometry.vertices[:]
    (nvertices, spaceDim) = vertices.shape
    vertices /= 1.0e+3 # convert m to km
    self.vertices = numpy.zeros( (nvertices, 3), dtype=numpy.float64)
    self.vertices[:,0:spaceDim] = vertices[:]

    self.vel = h5.root.vertex_fields.velocity[:]
    self.disp = h5.root.vertex_fields.displacement[:]

    h5.close()

    return


  def initialize(self):
    """
    """
    (nvertices, spaceDim) = self.vertices.shape
    (ncells, ncorners) = self.cells.shape
    
    assert(spaceDim == 3)
    assert(ncorners == 3)
    cellType = tvtk.Triangle().cell_type
    
    dataVtk = tvtk.UnstructuredGrid()
    dataVtk.points = self.vertices
    dataVtk.set_cells(cellType, self.cells)

    self.dataVtk = dataVtk
    return


  def toVtk(self, t):
    """
    """
    dataDt = 0.05
    magMin = 1.0e-6

    (nvertices, spaceDim) = self.vertices.shape

    tstep = int(t / dataDt)
    mag = (self.vel[tstep,:,0]**2 + self.vel[tstep,:,1]**2)**0.5
    mask = mag < magMin
    mag[mask] = magMin

    disp = numpy.zeros( (nvertices, 3), dtype=numpy.float64)
    disp[:,0:2] = self.disp[tstep,:,:]

    self.dataVtk.points = self.vertices + exaggeration*disp
    self.dataVtk.point_data.scalars = numpy.log10(mag)
    self.dataVtk.point_data.scalars.name = "magnitude"
    return self.dataVtk


class PlotScene(Mayavi):

  # PUBLIC METHODS /////////////////////////////////////////////////////

  def run(self):    

    self._setup()
    self.surfdata = SurfData()
    self.surfdata.read()
    self.surfdata.initialize()
    self._plotScene()
    self._annotateScene()
    self._setCamera()
    nsteps = int(1 + (tEnd - tBegin) / dt)
    scene = self.script.engine.current_scene.scene
    scene.disable_render = True
    scene.anti_aliasing_frames = 0
    scene.background = self.colorBg
    scene.foreground = self.colorFg
    scene.disable_render = False
    for istep in xrange(nsteps):
        t = tBegin + istep * dt
        self._updateFrame(t)
        scene.render()
        scene.save_png("frames/%s_%03d.png" % (sim, istep))
    return


  # PRIVATE METHODS ////////////////////////////////////////////////////

  def _setup(self):

    dkslate = (47/255.0, 53/255.0, 72/255.0)
    self.colorFg = (1,1,1)
    self.colorBg = dkslate
    self.colorSurfTrace = (1,1,0)
    self.lutReverse = False

    self.windowSize = (960, 960)
    self.aaframes = 0

    return
  

  def _plotScene(self):
    from enthought.mayavi.sources.vtk_data_source import VTKDataSource
    from enthought.mayavi.filters.extract_vector_norm import ExtractVectorNorm
    from enthought.mayavi.modules.outline import Outline
    from enthought.mayavi.modules.axes import Axes
    from enthought.mayavi.modules.surface import Surface
    from enthought.tvtk.api import tvtk

    script = self.script
    script.new_scene()
    w = script.get_active_window()
    w.size = self.windowSize
    scene = script.engine.current_scene.scene
    scene.disable_render = True
    scene.background = self.colorBg
    scene.foreground = self.colorFg

    t = 0.0
    self.dataVtk = self.surfdata.toVtk(t)
    script.engine.current_object.name = "Velocity"

    script.add_source(VTKDataSource(data=self.dataVtk))
    surf = Surface()
    surf.actor.property.representation = "wireframe"
    script.add_module(surf)

    colorbar = script.engine.current_object.module_manager.scalar_lut_manager
    colorbar.show_scalar_bar = True
    colorbar.scalar_bar.label_format = "%3.1f"
    colorbar.use_default_range = False
    colorbar.data_range = (-3, 1)
    colorbar.number_of_labels = 4
    colorbar.data_name = "Velocity (m/s)"
    colorbar.lut_mode = "hot"
    colorbar.reverse_lut = self.lutReverse

    scalar_bar = colorbar.scalar_bar_widget.representation
    scalar_bar.position2 = (0.05, 0.33)
    scalar_bar.position = (0.05, 0.05)


    return


  def _annotateScene(self):
    """
    """
    from enthought.mayavi.modules.text import Text

    script = self.script

    # Time stamp
    t = 0.0
    timestamp = Text()
    script.add_module(timestamp)
    script.engine.current_object.name = "Time Stamp"
    timestamp.text = "Time = %05.2f s" % t
    timestamp.property.bold = True
    timestamp.property.justification = "centered"
    timestamp.actor.width = 0.16
    timestamp.actor.position = [0.05, 0.96]
    timestamp.property.font_size = 20
    self.timestamp = timestamp
    return


  def _setCamera(self):
    """
    """
    script = self.script
    camera = self.script.engine.current_scene.scene.camera


    dist = 500.0
    ptTo = numpy.array( [0.0, 2.0, 0.0] )

    clipRange = numpy.array( [200, 5000] )
    ptFrom = ptTo + numpy.array( [0.0, 0.0, dist])      

    camera.view_up = (0,1,0)
    camera.focal_point = ptTo
    camera.position = ptFrom
    camera.clipping_range = clipRange
    camera.parallel_scale = 12.0
    camera.parallel_projection = True

    return


  def _updateFrame(self, t):
    """
    """
    self.dataVtk = self.surfdata.toVtk(t)
    self.timestamp.text = "Time = %05.2f s" % t
    return


# ----------------------------------------------------------------------
if __name__ == "__main__":

  app = PlotScene()
  app.main()


# End of file


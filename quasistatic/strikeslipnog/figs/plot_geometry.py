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

from enthought.mayavi.app import Mayavi
import vtk_geometry
from enthought.mayavi.sources.vtk_data_source import VTKDataSource

class PlotGeometry(Mayavi):

  def run(self):
    from enthought.mayavi.modules.outline import Outline
    from enthought.mayavi.modules.axes import Axes
    from enthought.mayavi.modules.surface import Surface
    
    script = self.script
    
    # Create rendering scene
    script.new_scene()
    script.engine.current_scene.scene.background = (1,1,1)
    script.engine.current_scene.scene.foreground = (0,0,0)
    vtk_geometry.setCamera(script.engine.current_scene.scene.camera)

    # Domain (axes and outline)
    script.add_source(VTKDataSource(data=vtk_geometry.domain()))
    script.engine.current_object.name = "Domain"
    outline = Outline()
    script.add_module(outline)
    outline.actor.property.opacity = 0.2
    axes = Axes()
    axes.axes.x_label = "X (km)"
    axes.axes.y_label = "Y (km)"
    axes.axes.z_label = "Z (km)"
    axes.axes.label_format = "%-0.1f"
    script.add_module(axes)

    # Fault surface
    srcs = vtk_geometry.fault(showTaper=True)
    for src in srcs:
      script.add_source(VTKDataSource(data=src['object']))
      script.engine.current_object.name = "Fault %s" % src['name']
      surf = Surface()
      script.add_module(surf)
      surf.actor.property.color = (1,0,0)
      if src['name'] == "taper":
        surf.actor.property.opacity = 0.1
      else:
        surf.actor.property.opacity = 0.3

    # Materials
    srcs = vtk_geometry.materials()
    for src in srcs:
      script.add_source(VTKDataSource(data=src['object']))
      script.engine.current_object.name = "Material %s" % src['name']
      surf = Surface()
      script.add_module(surf)
      surf.actor.property.opacity = 0.1
      if src['name'] == "elastic":
        surf.actor.property.color = (1,1,0)
      elif src['name'] == "viscoelastic":
        surf.actor.property.color = (0,1,1)

    return


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotGeometry()
  app.main()


# End of file


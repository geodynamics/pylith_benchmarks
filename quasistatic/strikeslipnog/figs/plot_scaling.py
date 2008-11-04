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

plotSize = "manual"
color = "lightbg"
fileSuffix = "eps"

# ======================================================================
import pylab
from mypylab.Figure import Figure

from runstats import dataScaling_v1_3 as data

# ----------------------------------------------------------------------
class PlotScaling(Figure):

  def __init__(self):
    if plotSize == "poster":
      fontsize = 21
    elif plotSize == "presentation":
      fontsize = 14
    elif plotSize == "manual":
      fontsize = 10
    else:
      raise ValueError("Unknown plotSize '%s'." % plotSize)
    Figure.__init__(self, color=color, fontsize=fontsize)
    return


  def main(self):

    if plotSize == "poster":
      self.width = 6.5
      self.height = 5.75
      margins = [[0.90, 0, 0.05], [0.70, 0, 0.12]]
    elif plotSize == "presentation":
      self.width = 4.0
      self.height = 5.0
      margins = [[0.7, 0, 0.05], [0.5, 0, 0.1]]
    elif plotSize == "manual":
      self.width = 5.5
      self.height = 5.0
      margins = [[0.6, 0, 0.05], [0.5, 0, 0.25]]
    else:
      raise ValueError("Unknown plotSize '%s'." % plotSize)

    # Create figure
    self.open(self.width, self.height, margins=margins)
    self.axes(1, 1, 1, 1)

    shapes = ["Tet4", "Hex8"]
    colorShapes = {'Tet4': 'orange',
                   'Hex8': 'blue'}

    handles = []
    labels = []
    for shape in shapes:
        nprocs = []
        total = []
        compute = []
        for sim in data[shape]:
            nprocs.append(sim['nprocs'])
            total.append(sim['total'])
            compute.append(sim['compute'])
        h = pylab.loglog(nprocs, total,
                         color=colorShapes[shape],
                         marker='+')
        handles.append(h)
        h = pylab.loglog(nprocs, compute,
                         color=colorShapes[shape],
                         linestyle="--",
                         marker='+')
        handles.append(h)
        pylab.title("Runtime versus Number of Processors")
        pylab.xlabel("Number of Processors")
        pylab.ylabel("Runtime (s)")
        pylab.xlim(0.5, 32)
        pylab.ylim(5.0e+0, 8.0e+2)
        labels += ["%s total" % shape, "%s compute" % shape]

    pylab.legend((handles[0][0], handles[1][0],
                  handles[2][0], handles[3][0]),
                 labels,
                 shadow=True,
                 loc='lower left')

    pylab.show()
    pylab.savefig("benchmark_scaling.%s" % fileSuffix)
    return


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotScaling()
  app.main()


# End of file


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

plotSize = "poster"
color = "lightbg"
fileSuffix = "eps"

# ======================================================================
import pylab
from mypylab.Figure import Figure

from runstats import dataScaling_v1_4 as data

# ----------------------------------------------------------------------
class PlotScaling(Figure):

  def __init__(self):
 
    if plotSize == "poster":
      fontsize = 18
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
      margins = [[0.90, 0, 0.05], [0.70, 0, 0.3]]
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

    #shapes = ["Tet4", "Hex8"]
    #colorShapes = {'Tet4': 'orange',
    #               'Hex8': 'blue'}
    shapes = ["Hex8"]
    colorShapes = {'Hex8': 'blue'}

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
        labels += ["%s total" % shape, "%s compute" % shape]

    time2 = compute[1] # runtime for 2 procs
    strongScaling = [[1.0, 16.0],
                     [2.0*time2, time2/8.0]]
    pylab.plot(strongScaling[0], strongScaling[1],
               linestyle=':',
               color='ltred')

    pylab.title("Runtime versus Number of Processors")
    pylab.xlabel("Number of Processors")
    pylab.ylabel("Runtime (s)")
    pylab.xlim(0.5, 32)
    pylab.ylim(1.0e+2, 1.0e+4)

    #pylab.legend((handles[0][0], handles[1][0],
    #              handles[2][0], handles[3][0]),
    #             labels,
    #             shadow=True,
    #             loc='lower left')
    pylab.legend((handles[0][0], handles[1][0]),
                 labels,
                 shadow=True,
                 loc='lower left')
    pylab.text(4.5, 1.8e+3, 'Strong scaling',
               rotation=-38.0,
               verticalalignment='top',
               horizontalalignment='left',
               color='ltred')

    pylab.show()
    pylab.savefig("benchmark_scaling.%s" % fileSuffix)
    return


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotScaling()
  app.main()


# End of file


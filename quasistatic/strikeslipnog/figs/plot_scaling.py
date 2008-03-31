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

import pylab

from runstats import dataScaling as data

class PlotSummary(object):

    def __init__(self):
        return

    def main(self):

        self._setup()

        iplot = 1
        pylab.subplot(self.nrows, self.ncols, iplot)
        handles = []
        labels = []
        for shape in self.shapes:
            nprocs = []
            total = []
            compute = []
            for sim in data[shape]:
                nprocs.append(sim['nprocs'])
                total.append(sim['total'])
                compute.append(sim['total']-sim['distribute'])
            h = pylab.loglog(nprocs, total,
                           color=self.colorShapes[shape],
                           marker='+')
            handles.append(h)
            h = pylab.loglog(nprocs, compute,
                           color=self.colorShapes[shape],
                           linestyle="--",
                           marker='+')
            handles.append(h)
            pylab.title("Runtime versus Number of Processors",
                        fontsize=self.titleFontSize)
            pylab.xlabel("Number of Processors",
                         fontsize=self.labelFontSize)
            pylab.ylabel("Runtime (s)",
                         fontsize=self.labelFontSize)
            pylab.xticks(fontsize=self.labelFontSize)
            pylab.yticks(fontsize=self.labelFontSize)
            pylab.xlim(0.5, 32)
            pylab.ylim(1.0e+2, 2.0e+3)
            iplot += 1
            labels += ["%s total" % shape, "%s compute" % shape]

        pylab.legend((handles[0][0], handles[1][0],
                      handles[2][0], handles[3][0]),
                     labels,
                     shadow=True,
                     loc='upper right')

        pylab.show()
        pylab.savefig('benchmark_scaling')
        return

    def _setup(self):
        figWidth = 5.5
        figHeight = 5.0
        colors = {'fg': (0,0,0),
                  'bg': (1,1,1),
                  'dkgray': 0.25,
                  'mdgray': 0.5,
                  'ltgray': 0.75,
                  'dkslate': (0.18, 0.21, 0.28),
                  'slate': (0.45, 0.50, 0.68),
                  'ltorange': (1.0, 0.74, 0.41),
                  'orange': (0.96, 0.50, 0.0),
                  'ltred': (1.0, 0.25, 0.25),
                  'red': (0.79, 0.00, 0.01),
                  'ltblue': (0.2, 0.73, 1.0),
                  'blue': (0.12, 0.43, 0.59),
                  'green': (0.37, 0.80, 0.05),
                  'green': (0.23, 0.49, 0.03)}
        from matplotlib.colors import colorConverter
        for key in colors.keys():
            colorConverter.colors[key] = colors[key]
        self.titleFontSize = 18
        self.labelFontSize = 14

        self.nrows = 1
        self.ncols = 1

        self.shapes = ["Tet4", "Hex8"]

        self.width = 1.0/(len(self.shapes)+1)

        self.colorShapes = {'Tet4': 'orange',
                            'Hex8': 'blue'}

        pylab.figure(figsize=(figWidth, figHeight),
                     facecolor='bg',
                     dpi=90)
        pylab.subplots_adjust(left=0.14,
                              right=0.96,
                              bottom=0.10,
                              top=0.91,
                              wspace=0.22,
                              hspace=0.35)
        return


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotSummary()
  app.main()


# End of file


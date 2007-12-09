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

# Hydra (2.2 GHz Opteron)
data = {
    "Tet4 1000m": {
        'ncells': 79756,
        'nvertices': 15625,
        'nflops': 1.01e+09,
        'run_time': 0.0,
        'error': 1.41e-03,
        'niterations': 60,
        'memory': 0.0},

    "Hex8 1000m": {
        'ncells': 13824,
        'nvertices': 15625,
        'nflops': 1.95e+09,
        'run_time': 15.9,
        'error': 0.0,
        'niterations': 37,
        'memory': 0.0},

    "Tet4 500m": {
        'ncells': 661929,
        'nvertices': 117649,
        'nflops': 1.28e+10,
        'run_time': 377.0,
        'error': 4.79e-04,
        'niterations': 106,
        'memory': 2400.0},

    "Hex8 500m": {
        'ncells': 110592,
        'nvertices': 117649,
        'nflops': 2.12e+10,
        'run_time': 154.0,
        'error': 0.0,
        'niterations': 68,
        'memory': 2100.0},


    "Tet4 250m": {
        'ncells': 5244768,
        'nvertices': 912673,
        'nflops': 1.0,
        'run_time': 0.0,
        'error': 0.0,
        'niterations': 0,
        'memory': 0.0},

    "Hex8 250m" : {
        'ncells': 884736,
        'nvertices': 912673,
        'nflops': 1.0,
        'run_time': 0.0,
        'error': 0.0,
        'niterations': 0,
        'memory': 0.0}
    }


class PlotSummary(object):

    def __init__(self):
        return

    def main(self):

        self._setup()

        plots = [{'value': "nvertices",
                  'title': "# Vertices",
                  'log': True,
                  'range': None},
                 {'value': "niterations",
                  'title': "# Iterations in Solve",
                  'log': False,
                  'range': None},
                 {'value': "run_time",
                  'title': "Run Time (s)",
                  'log': False,
                  'range': None},
                 {'value': "error",
                  'title': "Average Error (m)",
                  'log': True,
                  'range': (1e-5, 1e-2)},
                 {'value': "ncells",
                  'title': "# Cells",
                  'log': True,
                  'range': None},
                 {'value': "nflops",
                  'title': "# FLOPS",
                  'log': True,
                  'range': (1e+6, 1e+11)},
                 {'value': "memory",
                  'title': "Peak Memory Uage (MB)",
                  'log': False,
                  'range': None}]
        iplot = 1
        for plot in plots:
            pylab.subplot(self.nrows, self.ncols, iplot)
            offset = 0
            handles = []
            for shape in self.shapes:
                format = shape + " " + "%dm"
                keys = [format % res for res in self.resolutions]
                d = [data[key][plot['value']] for key in keys]
                h = pylab.bar(self.loc0+offset*self.width, d,
                              self.width,
                              log=plot['log'],
                              color=self.colorShapes[shape])
                handles.append(h)
                offset += 1
            pylab.title(plot['title'],
                        fontsize=self.titleFontSize)
            pylab.xticks(self.locs, ["%sm" % res for res in self.resolutions],
                         fontsize=self.labelFontSize)
            pylab.yticks(fontsize=self.labelFontSize)
            if not plot['range'] is None:
                pylab.ylim(plot['range'])
            iplot += 1

        pylab.subplot(self.nrows, self.ncols, iplot)
        pylab.axis('off')
        pylab.legend((handles[0][0], handles[1][0]), self.shapes,
                     shadow=True,
                     loc='center')

        pylab.show()
        #pylab.savefig('summary')
        return

    def _setup(self):
        figWidth = 8
        figHeight = 4
        colors = {'fg': (0,0,0),
                  'bg': (1,1,1),
                  'red': (1,0,0),
                  'green': (0,1,0),
                  'blue': (0,0,1)}
        from matplotlib.colors import colorConverter
        for key in colors.keys():
            colorConverter.colors[key] = colors[key]
        self.titleFontSize = 12
        self.labelFontSize = 10

        self.nrows = 2
        self.ncols = 4

        self.resolutions = [1000, 500, 250]
        self.shapes = ["Tet4", "Hex8"]

        self.width = 1.0/(len(self.shapes)+1)
        self.locs = pylab.arange(len(self.resolutions))
        self.loc0 = self.locs - 0.5*len(self.shapes)*self.width

        self.colorShapes = {'Tet4': 'red',
                            'Hex8': 'blue'}

        pylab.figure(figsize=(figWidth, figHeight),
                     dpi=90)
        pylab.subplots_adjust(left=0.06,
                              right=0.98,
                              bottom=0.05,
                              top=0.93,
                              wspace=0.46,
                              hspace=0.26)
        return


# ----------------------------------------------------------------------
if __name__ == "__main__":
  app = PlotSummary()
  app.main()


# End of file


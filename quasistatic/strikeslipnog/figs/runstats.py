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

# Hydra (2.2 GHz Opteron)
data = {
    "Tet4 1000m": {
        'ncells': 79756,
        'nvertices': 15625,
        'nflops': 9.911e+08,
        'run_time': 42.0,
        'error': 1.41e-03,
        'niterations': 59,
        'memory': 340},

    "Hex8 1000m": {
        'ncells': 13824,
        'nvertices': 15625,
        'nflops': 1.97e+09,
        'run_time': 18.9,
        'error': 6.58e-04,
        'niterations': 38,
        'memory': 293},

    "Tet4 500m": {
        'ncells': 661929,
        'nvertices': 117649,
        'nflops': 1.293e+10,
        'run_time': 380.6,
        'error': 4.79e-04,
        'niterations': 107,
        'memory': 2514.6},

    "Hex8 500m": {
        'ncells': 110592,
        'nvertices': 117649,
        'nflops': 2.16e+10,
        'run_time': 165.5,
        'error': 1.94e-04,
        'niterations': 70,
        'memory': 2205.9},


    "Tet4 250m": {
        'ncells': 5244768,
        'nvertices': 912673,
        'nflops': 0.0,
        'run_time': 0.0,
        'error': 1.30e-04,
        'niterations': 0,
        'memory': 0.0},

    "Hex8 250m" : {
        'ncells': 884736,
        'nvertices': 912673,
        'nflops': 0.0,
        'run_time': 0.0,
        'error': 7.70e-05,
        'niterations': 0,
        'memory': 0.0}
    }

# Hydra (2.2 GHz Opteron)
dataScaling = {
    "Tet4":
    [{'nprocs': 1,
      'total': 380.6,
      'distribute': 0.0},
     {'nprocs': 2,
      'total': 613.0,
      'distribute': 339.4},
     {'nprocs': 4,
      'total': 523.4,
      'distribute': 316.3},
     {'nprocs': 8,
      'total': 508.4,
      'distribute': 317.5},
     {'nprocs': 16,
      'total': 487.8,
      'distribute': 310.0},
     ],
    "Hex8":
     [{'nprocs': 1,
       'total': 165.4,
       'distribute': 0.0},
      {'nprocs': 2,
       'total': 206.4,
       'distribute': 50.4},
      {'nprocs': 4,
       'total': 181.22,
       'distribute': 49.8},
      {'nprocs': 8,
       'total': 181.8,
       'distribute': 52.5},
      {'nprocs': 16,
       'total': 188.0,
       'distribute': 52.2},
      ]
    }

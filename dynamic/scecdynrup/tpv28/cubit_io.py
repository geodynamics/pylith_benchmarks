#!/usr/bin/env python
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
# Charles A. Williams, GNS Science
# Matthew G. Knepley, University of Chicago
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2014 University of California, Davis
#
# See COPYING for license information.
#
# ----------------------------------------------------------------------
#
# PREREQUISITES: numpy, netCDF4

# ----------------------------------------------------------------------
# write_exodus_file
# ----------------------------------------------------------------------
def write_exodus_file(filename, cells, vertices, shape="SHELL4"):
    """
    Write Exodus-II file compatible with CUBIT.

    cells is a 0-based array (ncells, ncorners).

    vertices is (nvertices, dim).

    All cells are placed in a single block.

    Requires netCDF4 module.
    """
    import numpy
    from netCDF4 import Dataset

    len_string = 33

    root = Dataset(filename, 'w', format='NETCDF3_CLASSIC')

    # Set global attributes
    root.api_version = 4.98
    root.version = 4.98
    root.floating_point_word_size = 8
    root.file_size = 0
    root.title = "cubit"

    # Setup dimensions

    # Generic information
    root.createDimension('len_string', len_string)
    root.createDimension('len_line', 81)
    root.createDimension('four', 4)
    root.createDimension('num_qa_rec', 1)
    root.createDimension('time_step', None)

    # Mesh specific information
    (ncells, ncorners) = cells.shape
    (nvertices, dim) = vertices.shape
    root.createDimension('num_dim', dim)
    root.createDimension('num_el_blk', 1)
    root.createDimension('num_nod_per_el1', ncorners)
    root.createDimension('num_att_in_blk1', 1)

    root.createDimension('num_nodes', nvertices)
    root.createDimension('num_elem', ncells)
    root.createDimension('num_el_in_blk1', ncells)

    # Setup variables
    connect1 = root.createVariable('connect1', numpy.int32,
                                   ('num_el_in_blk1', 'num_nod_per_el1',))

    coord = root.createVariable('coord', numpy.float64,
                                ('num_dim', 'num_nodes',))
    
    time_whole = root.createVariable('time_whole', numpy.float64,
                                     ('time_step',))
    
    coor_names = root.createVariable('coor_names', 'S1',
                                     ('num_dim', 'len_string',))
    
    qa_records = root.createVariable('qa_records', 'S1',
                                     ('num_qa_rec', 'four', 'len_string',))
    
    eb_names = root.createVariable('eb_names', 'S1',
                                   ('num_el_blk', 'len_string',))

    elem_map = root.createVariable('elem_map', numpy.int32,
                                   ('num_elem',))

    eb_status = root.createVariable('eb_status', numpy.int32,
                                    ('num_el_blk',))

    eb_prop1 = root.createVariable('eb_prop1', numpy.int32,
                                   ('num_el_blk',))

    attrib1 = root.createVariable('attrib1', numpy.float64,
                                  ('num_el_in_blk1', 'num_att_in_blk1',))

    # Set variable values
    connect1[:] = 1+cells[:]
    connect1.elem_type = shape

    coord[:] = vertices.transpose()[:]

    from netCDF4 import stringtoarr
    if dim == 2:
        coor_names[0,:] = stringtoarr("x", len_string)
        coor_names[1,:] = stringtoarr("y", len_string)
    elif dim == 3:
        coor_names[0,:] = stringtoarr("x", len_string)
        coor_names[1,:] = stringtoarr("y", len_string)
        coor_names[2,:] = stringtoarr("z", len_string)


    qa_records[0,0,:] = stringtoarr("CUBIT", len_string)
    qa_records[0,1,:] = stringtoarr("11.0", len_string)
    qa_records[0,2,:] = stringtoarr("01/01/2000", len_string)
    qa_records[0,3,:] = stringtoarr("12:00:00", len_string)

    elem_map[:] = numpy.arange(1, ncells+1, dtype=numpy.int32)[:]

    eb_status[:] = numpy.ones( (1,), dtype=numpy.int32)[:]

    eb_prop1[:] = numpy.ones( (1,), dtype=numpy.int32)[:]
    eb_prop1.name = "ID"

    attrib1[:] = numpy.ones( (1, ncells), dtype=numpy.int32)[:]

    root.close()


# End of file

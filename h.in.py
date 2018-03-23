#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################################
#
# MODULE:       h.in
#
# AUTHOR(S):    Luís Moreira de Sousa
#
# PURPOSE:      Imports an HexASCII hexagonal raster into GRASS
#
# COPYRIGHT:    (c) 2018 Luís Moreira de Sousa
#
#               This programme is released under the European Union Public
#               Licence v 1.1. Please consult the LICENCE file for details.
#
#############################################################################

#%module
#% description: Loads an HexASCII raster into GRASS.
#% keyword: HexASCII
#% keyword: hexagons
#% keyword: raster
#%end
#%option INPUT
#% key: input
#% description: Input HEXASCII raster.
#%end
#%option OUTPUT
#% key: output
#% description: Name of output raster in GRASS.
#%end

import grass.script as gscript
import numpy as np
from grass.pygrass import raster
from grass.pygrass.raster.buffer import Buffer
from hex_utils.hasc import HASC

def main():
    
    options, flags = gscript.parser()
    input = options['input']
    output = options['output']
    
    if(output is None or output == ""):
        gscript.error(_("[h.in] ERROR: output is a mandatory parameter."))
        exit()
    
    # Load HexASCII raster into memory
    hexASCII = HASC()
    try:
        hexASCII.loadFromFile(input)
    except (ValueError, IOError) as ex:
        gscript.error(_("[h.in] ERROR: Failed to load raster %s: %s" % (input, ex)))
        exit()
        
    # Set region (note that it is tricking GRASS to think it is a squared raster)
    gscript.run_command('g.region', rows=hexASCII.nrows, cols=hexASCII.ncols, res=hexASCII.side)    
        
    # Create RasterRow object and iterate trough rows    
    newRast = raster.RasterRow(output)
    newRast.open('w', 'FCELL')
    for row in range(0, hexASCII.nrows):
        newRow = Buffer(shape=(1,hexASCII.ncols))#, dtype=float, order='F')
        for col in range(0, hexASCII.ncols):
            newRow[0, col] = hexASCII.get(col,row)
        gscript.message(_("[h.in] DEBUG: Importing row: %s" % newRow))
        newRast.put_row(newRow)
    gscript.message(_("[h.in] DEBUG: Imported raster: %s" % (newRast)))
    
    # Close RasterRow to force its creation
    newRast.close()
        
    gscript.message(_("[h.in] SUCCESS: HexASCII raster imported."))


if __name__ == '__main__':
    main()

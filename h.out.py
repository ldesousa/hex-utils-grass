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
#% description: HexASCII raster in the GRASS database.
#%end
#%option OUTPUT
#% key: output
#% description: Path of the HexASCII raster to create on disk.
#%end

import grass.script as gscript
from grass.pygrass import raster
from grass.pygrass import utils
from grass.pygrass.raster.buffer import Buffer
from hex_utils.hasc import HASC

def main():
    
    options, flags = gscript.parser()
    input = options['input']
    output = options['output']
    
    if(input is None or input == ""):
        gscript.error(_("[h.out] ERROR: input is a mandatory parameter."))
        exit()
        
    exists = False
    maps_list = utils.findmaps(type='raster')
    for map in maps_list:
        if input == map[0]:
            exists = True
            break
    if(not exists):
        gscript.error(_("[h.out] ERROR: could not find input map."))
        exit()        
        
    if(output is None or output == ""):
        gscript.error(_("[h.out] ERROR: output is a mandatory parameter."))
        exit()

    rast = raster.RasterRow(input)
    # Set region (note that it is tricking GRASS to think it is a squared raster)
    info = gscript.read_command('r.info', map=input, flags='g')
            
    info = info.split("\n")
    print(info[6])
    
    hexASCII = HASC()
    # This can probably be set from the RasterRow object
    hexASCII.init(  int(info[7].split("=")[1]), #ncols, 
                    int(info[6].split("=")[1]), #nrows, 
                    int(info[3].split("=")[1]), #xll, 
                    int(info[1].split("=")[1]), #yll, 
                    "NA") #nodata)    

    r = 0
    rast.open()
    for row in rast:
        for c in range(0, rast.info.cols):
            hexASCII.set(c, r, row[c]) 
        gscript.message(_("[h.in] DEBUG: Exporting row: %s" % newRow))
        r = r + 1

    gscript.message(_("[h.out] SUCCESS: HexASCII raster exported."))

if __name__ == '__main__':
    main()

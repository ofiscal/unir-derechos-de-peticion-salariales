import numpy as np
import os
import pandas as pd
import re

import python.manipulate_files_defs as defs


example_file = "data/input/agency_responses/Unidad de información y Análisis Financiero/1.10. Formularios Planta anteproyecto 2024.xlsm UIAF.xlsm"

x = pd.read_excel ( example_file )


########################
# Start manipulating it.
########################

# Keeping a copy of each stage makes debugging easy.

x0 = defs.strip_leading_rows  ( x  ) . copy()
x1 = defs.strip_trailing_rows ( x0 ) . copy()
x2 = defs.strip_empty_rows    ( x1 ) . copy()
x3 = defs.assemble_header     ( x2 ) . copy()


#################################
# Convert non-rows to column data
#################################

z = x3.copy()

z ["top kind of empleado"] = np.where (
    ( z["denominación de cargos:1"]
      . str.match ( "|".join ( [ "empleado.* p.blico",
                                 "trabajador.* oficial.*", ] ),
                    case = False ) ),
    z["denominación de cargos:1"] . str.lower(),
    np.nan )

z ["top kind of empleado, temp"] = (
  z ["top kind of empleado"] . copy() )

z ["top kind of empleado"] = (
  z ["top kind of empleado"]
  . fillna ( method = "ffill" ) )

z = ( z[ z["top kind of empleado, temp"] . isnull() ]
      . drop ( columns =
               ["top kind of empleado, temp"] ) )

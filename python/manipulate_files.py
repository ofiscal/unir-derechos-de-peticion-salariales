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
x4 = defs.false_rows_to_column (
  source_column_name = "denominación de cargos:1",
  patterns           = [ "empleado.* p.blico",
                         "trabajador.* oficial.*", ],
  new_column_name    = "empleado kind 1",
  df                 = x3 )

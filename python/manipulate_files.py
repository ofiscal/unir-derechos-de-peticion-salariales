import os
import pandas as pd
import re


example_file = "data/input/agency_responses/Unidad de información y Análisis Financiero/1.10. Formularios Planta anteproyecto 2024.xlsm UIAF.xlsm"

# removes the file extension
basename = os.path.splitext ( example_file ) [0]

x = pd.read_excel ( example_file )

first_interesting_row = (
  x . iloc[:,0] # ASSUMPTION: It's in the first column.
  . str.match ( "denominaci.n", # to identify "Denominación de Cargos"
                case = False )
  . fillna ( False )
  . argmax () )

  . str.match ( up_left_corner_regex,
                case = False )
  . fillna ( False )
  . astype ( int )
  . gt ( 0 )
  . argmax () )

x = x[first_row:]

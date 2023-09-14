import os
import pandas as pd
import re


example_file = "data/input/agency_responses/Unidad de información y Análisis Financiero/1.10. Formularios Planta anteproyecto 2024.xlsm UIAF.xlsm"

x = pd.read_excel ( example_file )


####################################
# Drop the first rows we don't need.
####################################

# The row index of the cell in the first column,
# if any, matching the regex "denominaci.n".
first_denominacion_row : int = (
  x . iloc[:,0] # ASSUMPTION: It's in the first column.
  . str.match ( "denominaci.n", # to identify "Denominación de Cargos"
                case = False )
  . fillna ( False )
  . argmax () )

# Drop all rows before `first_denominacion_row`.
x = x[first_denominacion_row:]


###################################
# Drop the last rows we don't need.
###################################

# True where the first column matches the regex "total".
total_rows : pd.Series = (
  x . iloc[:,0] # ASSUMPTION: It's in the first column.
  . str.match ( "total",
                case = False )
  . fillna ( False ) )

# True for every row which is a total row or followed by one.
total_row_or_followed_by_one : pd.Series = pd.Series (
  ( ( total_rows . index )
    <=
    ( total_rows [ total_rows ] . index # indices where total_rows is True
      . max() ) ),
  index = total_rows . index )

# Discard every row of x for which
# neither it nor any row after it
# matches the regex "total".
x = x[: total_row_or_followed_by_one.argmin() ]


#################
# Drop empty rows
#################

# True for every completely empty row of x.
row_is_empty : pd.Series = (
  x.isnull()
  . apply ( lambda row: row.all(),
            axis = 1 ) ) # to operate on rows, not columns

x = x [ ~ row_is_empty ]

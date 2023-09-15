import numpy as np
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


##############################
# Create header (column names)
##############################

y = x.copy()

for i in [0,1,2]:
  y.iloc[i] = ( # Fill non-missing values forward
    y.iloc[i] . fillna ( method = "ffill" ) )

for i in [0,1,2,3]: # fill remaining missing values with ""
                    # (which will be ignored in column names).
  y.iloc[i] = (
    y.iloc[i] . fillna ( "" ) )

y.columns = (
  y[0:5] # concatentate the first *four* rows
  . apply (
    ( lambda column:
      ":".join ( [ i for i
                   in column . astype(str)
                   if i # drop empty strings
                  ] )
      . lower () # increases the probability of matching column names
                 # across data from different agencies
      . replace ( " \n", " " )
     ),
    axis = 0 ) ) # to apply to columns, not rows

# Drop the rows that defined the header.
y = y.iloc[5:]


#################################
# Convert non-rows to column data
#################################

z = y.copy()

z ["top kind of empleado"] = np.where (
    ( z["denominación de cargos:1"]
      . str.match ( "|".join ( [ "empleado.* p.blico",
                                 "TRABAJADOR.* OFICIAL.*", ] ),
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

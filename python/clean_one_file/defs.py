import numpy as np
import os
import pandas as pd
import re
from   typing import Dict, List, Set
#
from   python.clean_one_file.types import *


def series_matches_regex (
    pattern : str,
    series  : pd.Series
) -> pd.Series:
  return ( series
           . str.match ( pattern,
                         case = False )
           . fillna ( False ) )

denominacion_pattern = "denominaci.n" # hoping for "Denominación de Cargos"

def strip_leading_rows (
    df                  : pd.DataFrame,
    denominacion_column : int,
) -> pd.DataFrame:
  """Strips the rows before the first match of the regex "denominaci.n"."""
  matches = series_matches_regex (
    pattern = denominacion_pattern,
    series = df . iloc [ :,
                         denominacion_column ] )
  if not matches.any():
    raise ValueError (
      Regex_Unmatched ( pattern = denominacion_pattern ) )
  else:
    return df [ matches.argmax(): ] # `argmax` gives the *first* index
                                    # achieving the maximum value (True).

total_pattern = "total.*" # Looking for things like "total empleados".

def strip_trailing_rows ( df : pd.DataFrame
                          ) -> pd.DataFrame:
  matches = series_matches_regex (
    pattern = total_pattern,
    series = df . iloc[:,0] ) # ASSUMPTION: It's in the first column.
  if not matches.any():
    raise ValueError (
      Regex_Unmatched ( pattern = total_pattern ) )
  else:
    last_matching_index = (
      matches [ matches ] # Since `matches` is boolean,
                          # this keeps only the true values
      . index . max() )
    return df [ df.index <= last_matching_index ]

def strip_empty_rows ( df : pd.DataFrame
                       ) -> pd.DataFrame:
  return df [
    ~ df . isnull() # a boolean table
    . apply ( # a boolean series that is
      # True for each entirely-null row
      lambda row: row.all(),
      axis = 1 ) ] # to operate on rows, not columns

def assemble_header ( df : pd.DataFrame
                      ) -> pd.DataFrame:
  n_header_rows = 5

  for i in range(n_header_rows-1):
    # In each header row but the last,
    # fill non-missing values forward.
    # PITFALL: Since the last row is just a series of integers,
    # filling it forward like the rest would destroy information.
    df.iloc[i] = (
      df.iloc[i] . fillna ( method = "ffill" ) )

  for i in range(n_header_rows):
    # Fill remaining missing values with "".
    # These will be ignored in column names.
    df.iloc[i] = (
      df.iloc[i] . fillna ( "" ) )

  df.columns = pd.Index ( # Concatentate those header columns.
    df[0:n_header_rows]
    . apply (
      ( lambda column:
        ":".join ( [ i for i
                     in column . astype(str)
                     if i # drops the empty strings
                    ] )
        . lower () # increases the probability of matching column names
                   # across data from different agencies
        . replace ( " \n", " " )
       ),
      axis = 0 ) ) # to apply to columns, not rows

  # Drop the rows that defined the header.
  return df.iloc[n_header_rows:]

def false_rows_to_column_using_regex (
    source_column_name : str,
    patterns           : List [ str ],
    new_column_name    : str,
    df                 : pd.DataFrame,
) ->                     pd.DataFrame:
  """Creates a new column with the matches to a regex. Fills those matches forward into all unmatched cells. Drops the rows that matched the regex."""

  if not source_column_name in df.columns:
    raise ValueError (
      Column_Absent ( pattern = source_column_name ) )
  patterns_str : str = "|".join ( patterns )
  df [ new_column_name ] = np.where (
    ( df [ source_column_name ]
      . str.match ( patterns_str, case = False ) ),
    df [ source_column_name ] . str.lower(),
    np.nan )
  if not df [ new_column_name ] . any():
    raise ValueError (
      Regex_Unmatched ( pattern = patterns_str ) )
  df [ new_column_name + "-temp" ] = (
    # This copy is not filled forward like the original.
    df [ new_column_name ] . copy() )
  df [ new_column_name ] = (
    df [ new_column_name ]
    . fillna ( method = "ffill" ) )
  return (
    df [ # drop all rows that matched a pattern
      df [ new_column_name + "-temp" ]
      . isnull() ]
    . drop ( columns = [new_column_name + "-temp"] ) )

# TODO ? PITFALL: This duplicates some code in
# `false_rows_to_column_using_regex`.
# It would be better to refactor both into a single function
# that takes a lambda to be run on each row
# that identifies whether it is a false row.
def false_rows_to_column_based_on_missing_values (
    source_column_name         : str, # the new column takes values from here
    missing_values_column_name : str, # missing values here identify rows
                                      # to generate the new column from
    new_column_name            : str,
    df                         : pd.DataFrame,
) ->                             pd.DataFrame:
  """Creates a new column with values from each cell in the source column where the corresponding cell in the missing values column is missing. Fills those valules forward. Deletes the source rows."""

  if not source_column_name in df.columns:
    raise ValueError (
      Column_Absent ( pattern = source_column_name ) )
  if not missing_values_column_name in df.columns:
    raise ValueError (
      Column_Absent ( pattern = missing_values_column_name ) )

  df [ new_column_name ] = np.where (
    df [ missing_values_column_name ] . isnull(),
    df [ source_column_name ] . str.lower(),
    np.nan )
  if not df [ new_column_name ] . any():
    raise ValueError ( Nothing_Missing() )

  df [ new_column_name + "-temp" ] = (
    # This copy is not filled forward like the original.
    df [ new_column_name ] . copy() )
  df [ new_column_name ] = (
    df [ new_column_name ]
    . fillna ( method = "ffill" ) )

  return (
    df [ # drop all rows that matched a pattern
      df [ new_column_name + "-temp" ]
      . isnull() ]
    . drop ( columns = [new_column_name + "-temp"] ) )

def format_tutela_response (
    source_file : File_Load_Instruction
) -> pd.DataFrame:
  return (
    false_rows_to_column_based_on_missing_values (
      source_column_name         = "denominación de cargos:1",
      missing_values_column_name = "grado:2",
      new_column_name            = "empleado kind 2",
      df = false_rows_to_column_using_regex (
        source_column_name = "denominación de cargos:1",
        patterns           = [ "empleado.* p.blico",
                               "trabajador.* oficial.*", ],
        new_column_name    = "empleado kind 1",
        df = assemble_header (
          strip_empty_rows (
            strip_trailing_rows (
              strip_leading_rows (
                pd.read_excel (
                  io    =             source_file . path,
                  sheet =             source_file . sheet ),
                denominacion_column = source_file . denominacion_column
              ) ) ) ) ) ) )

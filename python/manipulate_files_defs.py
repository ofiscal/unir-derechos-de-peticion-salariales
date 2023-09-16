from   dataclasses import dataclass
from   enum import Enum, unique, auto
import numpy as np
import os
import pandas as pd
import re
from   typing import Dict, List, Set


# PITFALL: This can't extend Exception and Enum simultaneously,
# for reasons I don't understand.
# Instead I will return `ValueError`s
# that *contain* these objects.
@dataclass
class Regex_Unmatched:
  pattern : str

@dataclass
class Column_Absent:
  pattern : str


def series_matches_regex (
    pattern : str,
    series  : pd.Series
) -> pd.Series:
  return ( series
           . str.match ( pattern,
                         case = False )
           . fillna ( False ) )

denominacion_pattern = "denominaci.n" # hoping for "Denominación de Cargos"

def strip_leading_rows ( df : pd.DataFrame
                         ) -> pd.DataFrame:
  """Strips the rows before the first match of the regex "denominaci.n"."""
  matches = series_matches_regex (
    pattern = denominacion_pattern,
    series = df . iloc[:,0] ) # ASSUMPTION: It's in the first column.
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

  df.columns = ( # Concatentate those header columns.
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
  df [ new_column_name ] = np.where (
    ( df [ source_column_name ]
      . str.match ( "|".join ( patterns ),
                    case = False ) ),
    df [ source_column_name ] . str.lower(),
    np.nan )
  if not df [ new_column_name ] . any():
    raise ValueError (
      Regex_Unmatched ( pattern = source_column_name ) )
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

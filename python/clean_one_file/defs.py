import numpy as np
import os
import pandas as pd
import re
from   typing import Dict, List, Set
#
from   python.types import *


denominacion_pattern = ".*denominaci.n.*cargo.*"
  # "Denominación de Cargos", or something close.
libre_pattern        = ".*libre.*nombramiento.*"
total_pattern = "total.*"
  # Totals like "total empleados" are redundant and unneeded.

def series_matches_regex (
    pattern : str,
    series  : pd.Series
) -> pd.Series:
  return ( series
           . str.match ( pattern,
                         case = False )
           . fillna ( False ) )

def strip_leading_rows (
    df                  : pd.DataFrame, # loses its first few rows
    denominacion_column : int, # column that determines number of rows dropped
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

def strip_trailing_rows ( df : pd.DataFrame
                          ) -> pd.DataFrame:
  """Strips the rows after the first match
  of `total_pattern` in the first column."""
  matches = series_matches_regex (
    pattern = total_pattern,
    series = df . iloc[:,0] ) # PITFALL: Assumes it's in column 0
  if not matches.any():
    raise ValueError (
      Regex_Unmatched ( pattern = total_pattern ) )
  else:
    last_matching_index = (
      matches [ matches ] # Since `matches` is Boolean,
                          # this keeps only the true values.
      . index . max() )
    return df [ df.index <= last_matching_index ]

def strip_empty_rows ( df : pd.DataFrame
                       ) -> pd.DataFrame:
  return df [ ~ # Negate the whole indexing series.
                # PITFALL: Depends on the somewhat obscure fact that
                # rows can be selected from a frame via a boolean series.
                # It behaves how you'd expect -- even if the index is sparse.
              ( df . isnull() # True where `df` lacks data, False elsewhere.
                . apply ( # Creates a boolean series that is
                          # True for each entirely-null row.
                  lambda row: row.all(),
                  axis = 1 ) ) ] # to operate on rows, not columns

def mk_header_and_drop_header_rows (
    df : pd.DataFrame
)     -> pd.DataFrame:
  """
  PURPOSE:
  Some rows are what I'm calling "header rows".
  That means they include information that should be in the header
  (that is, it should be the column names), not in ordinary rows.
  In the output, the header (column names) are good,
  and the "header rows" it was created from are deleted.

  TODO | PITFALL:
  This algorithm is flawed.
  Looking at the output, it's obvious that headers are mangled.
  If I recall correctly (a nontrivial assumption)
  it's because filling downward is not always appropriate;
  sometimes you should fill rightward.
  """
  n_header_rows = 5

  if True: # Modify the header rows.

    for i in range(n_header_rows-1):
      # In each header row but the last,
      # fill non-missing values forward.
      # PITFALL: Since the last row is just a series of integers,
      # filling it forward like the rest would destroy information.
      # Therefore the range above terminates one unit early.
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

  return df.iloc[
    # Drop the rows that defined the header.
    n_header_rows:]

# TODO ? PITFALL: This duplicates some code in
# `false_rows_to_column_based_on_missing_values`.
# It would be better to refactor both into a single function
# that takes a lambda to be run on each row
# that identifies whether it is a false row.
def false_rows_to_column_using_regex (
    source_column_name : str, # The column to match against.
    patterns           : List [ str ], # Patterns to match.
    new_column_name    : str, # Created from the matches.
    df                 : pd.DataFrame,
) ->                     pd.DataFrame:
  """Creates a new column with the matches to a regex.
  Fills those matches forward into all unmatched cells.
  Drops the rows that matched the regex.

  PITFALL: This makes sense if and only if the regex-matching row
  describes a quality that applies to every row below it,
  until the next regex-matching row.
  """

  if not source_column_name in df.columns:
    raise ValueError (
      Column_Absent ( pattern = source_column_name ) )
  patterns_str : str = "|".join ( patterns )
    # Moving the disjunction logic from Python into the regex
    # is probably efficient, because
    # the regex is probably implemented in something fast.
  df [ new_column_name ] = np.where ( # if-then-else
    ( df [ source_column_name ]
      . str.match ( patterns_str, case = False ) ),
    df [ source_column_name ] . str.lower(),
    np.nan )
  if not df [ new_column_name ] . any():
    raise ValueError (
      Regex_Unmatched ( pattern = patterns_str ) )
  temp_column_name = new_column_name + "-temp"
  df [ temp_column_name ] = (
    # This temporary copy is not filled forward.
    # It is used to know which rows to drop.
    df [ new_column_name ] . copy() )
  df [ new_column_name ] = (
    df [ new_column_name ]
    . fillna ( method = "ffill" ) )
  return (
    df [ # Keep only rows that matched no pattern.
      df [ temp_column_name ]
      . isnull () ]
    . drop ( columns = [ temp_column_name ] ) )

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
  """Creates a new column such that,
  wherever the missing values column is missing,
  the new column is equal to the source column,
  and everywhere else the new column's value is missing.
  Then it fills those values (in the new column) forward.
  Last, it deletes the source rows.
  """

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

  temp_column_name = new_column_name + "-temp"
  df [ temp_column_name ] = (
    # This temporary copy is not filled forward.
    # It is used to know which rows to drop.
    df [ new_column_name ] . copy() )
  df [ new_column_name ] = (
    df [ new_column_name ]
    . fillna ( method = "ffill" ) )

  return (
    df [ # Keep only rows that matched no pattern.
      df [ temp_column_name ]
      . isnull() ]
    . drop ( columns = [ temp_column_name ] ) )

def format_tutela_response (
    agency_root : str, # the `path` of `source_file` is relative to this
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
        df = mk_header_and_drop_header_rows (
          strip_empty_rows (
            strip_trailing_rows (
              strip_leading_rows (
                pd.read_excel (
                  io         = os.path.join ( agency_root,
                                              source_file . path ),
                  sheet_name =                source_file . sheet ),
                denominacion_column = source_file . denominacion_column
              ) ) ) ) ) ) )

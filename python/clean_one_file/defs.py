import numpy as np
import os
import pandas as pd
import re
from   typing import Dict, List, Set
#
from   python.types import *


denominacion_pattern = ".*denominaci.n.*cargo.*"
  # "Denominación de Cargos", or something close.
grado_pattern        = "grado.*:2"
libre_pattern        = ".*libre.*nombramiento.*"
total_pattern        = "total.*"
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

def increment_int_after_last_dash ( cell : str
                                   ) -> str:
  """Given a string ending in "-x" where x is an integer, this returns the same string but ending in an integer one greater. If the string ends in a dash, it appends 0. If it contains no dash, it appends "-0". If it contains a dash but the portion after the dash is not an integer, it appends -0.
  The test suite gives an example of each case.
  """
  s = pd.Series ( list ( cell ) ) # a series of characters
  is_dash : pd.Series = s [ s . str.match ("-") ] # a series of bools
  if len(is_dash) < 1: # There are no dashes in `cell`.
                       # Maybe it is empty. Regardless, append -0.
    return cell + "-0"
  elif cell[-1] == "-": # `cell` ends in a dash, so append 0.
    return cell + "0"
  else:
    index_of_last_dash = ( is_dash
                           . index [-1] )
    tail = ( ( s [ index_of_last_dash + 1 :] )
             . str.cat () )
    try: tail_as_int = int(tail)
    except: # `tail` cannot be converted to an int, so append `-0`
      return cell + "-0"
    return ( # increment `tail` in `cell`
      cell [ : index_of_last_dash + 1 ] +
      str ( tail_as_int + 1 ) )

def fill_header_frame (
    df : pd.DataFrame # A (multi-row) "header frame".
) -> pd.Index: # A true header, as wide as the input data frame.
  """First, missing values are filled down from the top, then they are filled rightward, and finally the rows in each column are concatenated to give a name for that column. If the top-left cell is nonempty, this ensures that every cell will be nonempty."""
  return pd.Index (
    df
    . fillna ( method = "ffill" ) # fill down
    . transpose ()
    . fillna ( method = "ffill" ) # fill rightward
    . transpose ()
    . astype ( str )
    . apply ( ( lambda row: # concatenate each column's rows
                ":"
                . join ( list ( row ) )
                . replace ( "\n", " " ) ),
              axis = "rows" ) )

def mk_header_and_drop_header_rows (
    df : pd.DataFrame
)     -> pd.DataFrame:
  """Creates a formal column name header
  from the rows that were serving that function
  in the original .xlsx documents,
  and drops those rows."""
  n_header_rows = 5
  df.columns = fill_header_frame (
    df.iloc [:n_header_rows] )
  return df[n_header_rows:]

# TODO ? PITFALL: This duplicates some code in
# `false_rows_to_column_based_on_missing_values`.
# It would be better to refactor both into a single function
# that takes a lambda to be run on each row
# that identifies whether it is a false row.
def false_rows_to_column_using_regex (
    source_column_regex : str,          # The column to match against.
      # (More accurately, a regex that should uniquely match one column,
      # against which to match.)
    patterns            : List [ str ], # Patterns to match.
    new_column_name     : str,          # Created from the matches.
    df                  : pd.DataFrame,
) ->                      pd.DataFrame:
  """Creates a new column with the matches to a regex.
  Fills those matches forward into all unmatched cells.
  Drops the rows that matched the regex.

  PITFALL: This makes sense if and only if the regex-matching row
  describes a quality that applies to every row below it,
  until the next regex-matching row.
  """

  source_column_matches =  (
    pd.Series ( df.columns )
    . str.match ( source_column_regex,
                  case = False ) )
  if not source_column_matches . any ():
    raise ValueError (
      Column_Absent ( pattern = source_column_regex ) )
  source_column_name = \
    pd.Series ( df . columns ) [source_column_matches ] . iloc [0]

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
    source_column_regex         : str, # The new column takes values
      # from the column (there should be only one) matching this regex.
    missing_values_column_regex : str, # Missing values in the first column
      # (there should be only one) matching this regex
      # identify rows to generate the new column from.
    new_column_name             : str,
    df                          : pd.DataFrame,
) ->                              pd.DataFrame:
  """Creates a new column such that,
  wherever the missing values column is missing,
  the new column is equal to the source column,
  and everywhere else the new column's value is missing.
  Then it fills those values (in the new column) forward.
  Last, it deletes the source rows.
  """

  source_column_matches =  (
    pd.Series ( df.columns )
    . str.match ( source_column_regex,
                  case = False ) )
  missing_values_column_matches = (
    pd.Series ( df.columns )
    . str.match ( missing_values_column_regex,
                  case = False ) )

  if not source_column_matches . any ():
    raise ValueError (
      Column_Absent ( pattern = source_column_regex ) )
  if not missing_values_column_matches . any ():
    raise ValueError (
      Column_Absent ( pattern = missing_values_column_regex ) )

  source_column_name         = \
    pd.Series ( df . columns ) [source_column_matches        ] . iloc [0]
  missing_values_column_name = \
    pd.Series ( df . columns ) [missing_values_column_matches] . iloc [0]

  df [ new_column_name ] = np.where (
    df [ missing_values_column_name ] . isnull(),
    df [ source_column_name ] . str.lower(),
    np.nan )
  if not df [ new_column_name ] . any ():
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
      source_column_regex         = denominacion_pattern,
      missing_values_column_regex = grado_pattern,
      new_column_name             = "empleado kind 2",
      df = false_rows_to_column_using_regex (
        source_column_regex = denominacion_pattern,
        patterns            = [ "empleado.* p.blico",
                                "trabajador.* oficial.*", ],
        new_column_name     = "empleado kind 1",
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

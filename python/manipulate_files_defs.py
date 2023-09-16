from   dataclasses import dataclass
from   enum import Enum, unique, auto
import numpy as np
import os
import pandas as pd
import re


# PITFALL: This can't extend Exception and Enum simultaneously,
# for reasons I don't understand.
# Instead I will return `ValueError`s that *contain* `ManipError`s.
@dataclass
class Failure_to_Match:
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
      Failure_to_Match ( pattern = denominacion_pattern ) )
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
      Failure_to_Match ( pattern = total_pattern ) )
  else:
    last_matching_index = (
      matches [ matches ] # Since `matches` is boolean,
                          # this keeps only the true values
      . index . max() )
    return df [ df.index <= last_matching_index ]

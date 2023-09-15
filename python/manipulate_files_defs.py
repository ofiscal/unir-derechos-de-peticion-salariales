from   enum import Enum, unique, auto
import numpy as np
import os
import pandas as pd
import re


# PITFALL: This can't extend Exception and Enum simultaneously,
# for reasons I don't understand.
# Instead I will return `ValueError`s that *contain* `ManipError`s.
@unique
class ManipError (Enum):
  No_Denominacion = auto ()

def series_matches_regex (
    pattern : str,
    series  : pd.Series
) -> pd.Series:
  return ( series
           . str.match ( pattern,
                         case = False )
           . fillna ( False ) )

def strip_leading_rows ( df : pd.DataFrame
                         ) -> pd.DataFrame:
  """Strips the rows before the first match of the regex "denominaci.n"."""
  matches = series_matches_regex (
    pattern = "denominaci.n", # hoping for "Denominación de Cargos"
    series = df . iloc[:,0] ) # ASSUMPTION: It's in the first column.
  if not matches.any():
    raise ValueError ( ManipError.No_Denominacion )
  else:
    return df [ matches.argmax(): ] # `argmax` gives the *first* index
                                    # achieving the maximum value (True).

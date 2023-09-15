from   enum import Enum, unique, auto
import numpy as np
import os
import pandas as pd
import re


# PITFALL: This can't extend Exception and Enum simultaneously,
# for reasons I don't understand.
# Instead I will return `Exception`s that *contain* `ManipError`s.
@unique
class ManipError (Enum):
  No_Denominacion = auto ()

def matches_denominacion_series ( s : pd.Series
                                 ) -> pd.Series:
  return (
    s . str.match (
      "denominaci.n", # hoping for "Denominación de Cargos"
      case = False )
    . fillna ( False ) )

def strip_leading_rows ( df : pd.DataFrame
                         ) -> pd.DataFrame:
  """Strips the rows before the first match of the regex "denominaci.n"."""
  s = matches_denominacion_series (
    df . iloc[:,0] ) # ASSUMPTION: It's in the first column.
  if not s.any():
    raise Exception ( ManipError.No_Denominacion )
  else:
    return df [ s.argmax(): ] # PITFALL: argmax gives the *first* index
                              # achieving the maximum value (True).

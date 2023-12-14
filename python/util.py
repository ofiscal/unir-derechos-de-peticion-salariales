import numpy as np
import pandas as pd


def near ( a,
           b,
           tolerance_relative = 0.01,
           tolerance_absolute = 1,
          ) -> bool:
  return ( ( ( (1 + tolerance_relative) * a > b) &
             ( (1 + tolerance_relative) * b > a) )
           |
           ( (tolerance_absolute + a > b) &
             (tolerance_absolute + b > a) ) )

def nullish (
    x,
    tolerance_absolute = 0.4, # less than 1/2, so that it works for ints
) -> bool:
  if x is np.nan:
    return True
  if str(x) == "nan": # PITFALL: Ugly hack. Used because, despite all logic,
    # `x is np.nan` returns False if `x` is missing (that is, np.nan)
    # when this function is being applied to a series of floats.
    return True
  if type(x) == str:
    return x == ""
  if type(x) in [float,int]:
    return near ( 0, x, tolerance_absolute = tolerance_absolute )

def str_to_float (s : pd.Series) -> pd.Series:
  return (s . astype ( str )
          . str.replace ( "[, ]",       "",    regex=True )
          .     replace ( ["","nan"],   np.nan )
          . astype ( float ) )

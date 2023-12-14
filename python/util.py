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

def str_to_float (s : pd.Series) -> pd.Series:
  return (s . astype ( str )
          . str.replace ( "[, ]",       "",    regex=True )
          .     replace ( ["","nan"],   np.nan )
          . astype ( float ) )

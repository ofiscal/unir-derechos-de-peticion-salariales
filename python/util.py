import pandas as pd


def str_to_float (s : pd.Series) -> pd.Series:
  return (s . astype ( str )
          . str.replace ( "[, ]",       "",    regex=True )
          .     replace ( ["","nan"],   np.nan )
          . astype ( float ) )

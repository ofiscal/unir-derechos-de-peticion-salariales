from   os import path
import pandas as pd
import re
#
import python.explore.successes.defs as successes_defs
from   python.util import near


def add_synthetic_total (df : pd.DataFrame) -> pd.DataFrame:
  df [ "gasto total synth"] = (
    df [[ 'salario',
          'remuneraciones',
          'contribuciones',
          'prestaciones', ]]
    . sum ( axis = "columns" ) )
  return df

def agencies_at_each_quantile_of_each_numeric_var (
    together : pd.DataFrame, # all agencies we can read
) -> pd.DataFrame:

  quantiles = [0,0.25,0.5,0.75,1]
  res = pd.DataFrame (
    [],
    columns = [ x
                for cn in successes_defs . cop_columns
                for x in [cn, cn + " file"] ],
    index = quantiles )

  for cn in successes_defs . num_columns:
    for q in quantiles: # a quantile
      qcop = together[cn] . quantile (q) # a COP value
      res.loc [ q, cn ] = qcop
      nearest_below_index = (
        # There might be no value for which together[cn]
        # is exactly equal to qcop,
        # so instead I find the maximum of values below it.
        together [ together[cn] <= qcop ]
        [cn] . idxmax () )
      res.loc [ q, cn + " file" ] = (
        together [ together.index == nearest_below_index ]
        ["agency"]
        . iloc[0] )

  res . transpose() . to_excel (
    "agencies_at_each_quantile_of_each_numerical_var.xlsx" )

  return res

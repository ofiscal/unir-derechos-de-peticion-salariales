import numpy as np
import os
import pandas as pd
import re


def matches_denominacion_series ( s : pd.Series
                                 ) -> pd.Series:
  return (
    s . str.match (
      "denominaci.n", # hoping for "Denominación de Cargos"
      case = False )
    . fillna ( False ) )

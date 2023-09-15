import numpy as np
import pandas as pd
import re

import python.manipulate_files_defs as defs


def test_matches_denominacion_series ():
  assert (
    defs.matches_denominacion_series (
      pd.Series ( [ "Denominación de Cargos",
                    "Empleados Públicos" ] ) )
    . equals (
      pd.Series ( [ True, False ] ) ) )

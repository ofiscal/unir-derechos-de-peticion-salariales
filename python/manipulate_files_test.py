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

def test_strip_leading_rows ():
  assert (
    strip_leading_rows (
      pd.DataFrame ( { 0 : ["denominación de cargos","moo","bark"] } ) )
    . reset_index ( drop = True )
    . equals (
      pd.DataFrame ( { 0 : ["moo","bark"] } ) ) )

  if True: # Test that Exception-raising works.
    try:
      strip_leading_rows (
        pd.DataFrame ( { 0 : ["no","match","here"] } ) )
    except Exception ( ManipError.No_Denominacion ): # The test passed.
      pass
    else: # The test failed.
      assert False

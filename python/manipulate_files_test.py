import numpy as np
import pandas as pd
import re
#
import python.manipulate_files_defs as defs


def test_series_matches_regex ():
  assert (
    defs.series_matches_regex (
      pattern = ".*x.*",
      series = pd.Series ( [ "axa",
                             "y" ] ) )
    . equals (
      pd.Series ( [ True, False ] ) ) )

def test_strip_leading_rows ():
  if True: # Test the case of good data
    good_data = pd.DataFrame (
      { 0 : ["strip", "this", "garbage",
             "denominación de cargos","moo","bark",] } )
    assert ( defs.strip_leading_rows ( good_data )
             . equals ( good_data[3:] ) )

  if True: # Test the case of bad data --
           # i.e. that Exception-raising works.
    try:
      defs.strip_leading_rows (
        pd.DataFrame ( { 0 : ["no","match","here"] } ) )
    except ValueError as e:
      # PITFALL: Enums cannot be compared directly!
      # (They are all equal if they're all of the same type.)
      # Must call `value` first.
      assert e.args[0].pattern == defs.denominacion_pattern
    else:
      assert False # This would be test failure.

def test_strip_trailing_rows ():
  if True: # Test the case of good data
    good_data = pd.DataFrame (
      { 0 : [ "denominación de cargos",
              "accountant",
              "bandido",
              "pintor",
              "total meh",
              "total bleh",
              "strip",
              "this",
              "garbage", ] } )
    assert ( defs.strip_trailing_rows ( good_data )
             . equals ( good_data[:-3] ) )

  if True: # Test the case of bad data --
           # i.e. that Exception-raising works.
    try:
      defs.strip_trailing_rows (
        pd.DataFrame ( { 0 : ["no","match","here"] } ) )
    except ValueError as e:
      # PITFALL: Enums cannot be compared directly!
      # (They are all equal if they're all of the same type.)
      # Must call `value` first.
      assert e.args[0].pattern == defs.total_pattern
    else:
      assert False # This would be test failure.

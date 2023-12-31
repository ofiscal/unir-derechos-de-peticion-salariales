import numpy as np
from   numpy import nan
import pandas as pd
import re
#
from   python.clean_one_file.defs import *


def test_fill_last_header_row ():
  assert (
    fill_last_header_row (
      pd.Series ( ["","",0,"",1,""] ) )
    . equals (
      pd.Series ( ["-0","-1","0","0-0","1","1-0" ] ) ) )

def test_increment_int_after_last_dash ():
  assert increment_int_after_last_dash ("") == "-0"
  assert increment_int_after_last_dash ("a") == "a-0"
  assert increment_int_after_last_dash ("a-0") == "a-1"
  assert increment_int_after_last_dash ("a-9") == "a-10"
  assert increment_int_after_last_dash ("a-9") == "a-10"
  assert increment_int_after_last_dash ("a-9-1") == "a-9-2"
  # Degenerate cases
  assert increment_int_after_last_dash ("a-") == "a-0"
  assert increment_int_after_last_dash ("a-b") == "a-b-0"

def test_fill_header_frame ():
  assert (

    fill_header_frame (
      pd.DataFrame ( { 0 : ["x", nan, nan],
                       1 : [nan, nan, "c"],
                       2 : [nan, nan, nan],
                       3 : [nan, "a", nan] } ),
      n_header_rows = 3 )

    . equals (
      pd.Index ( [ "x:x:-0",
                   "x:x:c",
                   "x:x:c-0",
                   "x:a:c-1" ] ) ) )

def test_series_matches_regex ():
  assert (
    series_matches_regex (
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
    assert ( strip_leading_rows ( good_data,
                                  denominacion_column = 0 )
             . equals ( good_data[3:] ) )

  if True: # Test the case of bad data --
           # i.e. that Exception-raising works.
    try:
      strip_leading_rows (
        pd.DataFrame ( { 0 : ["no","match","here"] } ),
        denominacion_column = 0 )
    except ValueError as e:
      # PITFALL: Enums cannot be compared directly!
      # (They are all equal if they're all of the same type.)
      # Must call `value` first.
      assert e.args[0].pattern == denominacion_pattern
    else:
      assert False

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
    assert ( strip_trailing_rows ( good_data )
             . equals ( good_data[:-3] ) )

  if True: # Test the case of bad data --
           # i.e. that Exception-raising works.
    try:
      strip_trailing_rows (
        pd.DataFrame ( { 0 : ["no","match","here"] } ) )
    except ValueError as e:
      # PITFALL: Enums cannot be compared directly!
      # (They are all equal if they're all of the same type.)
      # Must call `value` first.
      assert e.args[0].pattern == total_pattern
    else:
      assert False

def test_strip_empty_rows ():
  df = pd.DataFrame ( [ [ nan, nan ],
                        [ 3  , nan ],
                        [ 3  , 4 ] ] )
  assert ( strip_empty_rows ( df )
           . equals ( df[1:] ) )

def test_mk_header_and_drop_header_rows ():
  assert (

    mk_header_and_drop_header_rows (
      pd.DataFrame ( [
        [ # The first nan here becomes "".
          # All the others in the first three rows are filled with
          # the previous non-nan value.
          nan   , nan , "3"   , nan     , nan      ],
        [ "1"   , nan , "3"   , "4"     , nan      ],
        [ "1"   , "2" , nan   , nan     , "5"      ],
        [ # this row has no effect on the resulting names
          nan   , nan , "3"   , nan     , nan      ],
        [ # Tricky: Even the nan after the 4 becomes ""
          # in this row, unlike the others.
          nan   , nan , nan   , "4"     , nan      ],
        # The above rows describe the header. The rest should be unchanged.
        [ "none", "of", "this", "should", "change" ], ] ) )

    . equals (
      pd.DataFrame (
        [ [ "none", "of", "this", "should", "change" ] ],
        index = [5],
        columns = ['nan:1:1:1:-0',
                   'nan:1:2:2:-1',
                     '3:3:3:3:-2',
                     '3:4:4:4:4',
                     '3:4:5:5:4-0'] ) ) )

def test_false_rows_to_column_using_regex ():
  assert (
    false_rows_to_column_using_regex (
      source_column_regex = "source",
      patterns            = ["a","b"],
      new_column_name     = "sink",
      df = pd.DataFrame ( {
        "source" : ["1","2","a","4","b","6","7"],
        "more"   : [ 1 , 2 , 3 , 4 , 5 , 6 , 7 ],
      } ) )
    . reset_index ( drop = True )
    . equals (
      pd.DataFrame ( {
        "source" : [ "1","2","4","6","7" ],
        "more"   : [  1 , 2 , 4 , 6 , 7  ],
        "sink"   : [ nan,nan,"a","b","b" ],
      } ) ) )

  try:
    false_rows_to_column_using_regex (
      source_column_regex = "source",
      patterns            = ["a","b"],
      new_column_name     = "sink",
      df = pd.DataFrame ( {
        "badly named source" : ["1","2","a","4","b","6","7"],
        "more"   :             [ 1 , 2 , 3 , 4 , 5 , 6 , 7 ],
      } ) )
  except ValueError as e:
    assert e.args[0] == Column_Absent ( "source" )
  else:
    assert False

  try:
    patterns           = ["a","b"]
    false_rows_to_column_using_regex (
      source_column_regex = "source",
      patterns            = patterns,
      new_column_name     = "sink",
      df = pd.DataFrame ( {
        "source" : ["-","-","-","-","-","-","-"],
        "more"   : [ 1 , 2 , 3 , 4 , 5 , 6 , 7 ],
      } ) )
  except ValueError as e:
    assert e.args[0] == Regex_Unmatched (
      "|".join ( patterns ) )
  else:
    assert False

def test_false_rows_to_column_based_on_missing_values ():
  assert (

    false_rows_to_column_based_on_missing_values (
      source_column_regex         = "source",
      missing_values_column_regex = "missing",
      new_column_name             = "sink",
      df = pd.DataFrame ( {
        "source"  : ["1","2","3"  ,"4","5","6"  ,"7"],
        "missing" : ["1","2",nan  ,"4","5", nan  ,"7"],
      } ) )
    . reset_index ( drop = True )

    . equals (
      pd.DataFrame ( {
        "source"  : [ "1", "2", "4", "5","7"],
        "missing" : [ "1", "2", "4", "5","7"],
        "sink"    : [ nan, nan, "3", "3","6"],
        } ) ) )

  try:
    false_rows_to_column_based_on_missing_values (
      source_column_regex         = "source",
      missing_values_column_regex = "missing",
      new_column_name             = "sink",
      df = pd.DataFrame ( { # irrelevant data, aside from column names
        "badly named source"  : [ 1 , 2 , 3   , 4 , 5 , 6   , 7 ],
        "missing"             : [ 1 , 2 , nan , 4 , 5 , nan , 7 ],
      } ) )
  except ValueError as e:
    assert e.args[0] == Column_Absent ( "source" )
  else:
    assert False

  try:
    false_rows_to_column_based_on_missing_values (
      source_column_regex         = "source",
      missing_values_column_regex = "missing",
      new_column_name             = "sink",
      df = pd.DataFrame ( { # irrelevant data, aside from column names
        "source"  :             ["1","2","3"  ,"4","5","6"  ,"7"],
        "badly named missing" : [ 1 , 2 , nan , 4 , 5 , nan , 7 ],
      } ) )
  except ValueError as e:
    assert e.args[0] == Column_Absent ( "missing" )
  else:
    assert False

  try:
    false_rows_to_column_based_on_missing_values (
      source_column_regex         = "source",
      missing_values_column_regex = "missing",
      new_column_name             = "sink",
      df = pd.DataFrame ( {
        "source"  : ["1","2","3","4","5","6","7"],
        "missing" : ["1","2","3","4","5","6","7"],
      } ) )
  except ValueError as e:
    assert e.args[0] == Nothing_Missing()
  else:
    assert False

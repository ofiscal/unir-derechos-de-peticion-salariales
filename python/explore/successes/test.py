import os
import pandas  as pd
import pickle
import pytest
from   typing  import *
#
from   python.explore.successes.defs  import *
import python.paths                   as paths
from   python.types                   import *


def test_columns_matching_regexes_if_one_to_one_correspondence ():
  df = pd.DataFrame ( [], columns = ["a","ab","c","cd"] )
  assert ( columns_matching_regexes_if_one_to_one_correspondence ( df, ["ab","cd"] )
           . equals ( df[["ab","cd"]] ) )

  with pytest.raises(ValueError) as excinfo:
    columns_matching_regexes_if_one_to_one_correspondence ( df, ["a.*","ab"] )
  print(excinfo.value)
  assert ( str(excinfo.value) ==
           # PITFALL: Must compare on strings because no ValueError
           # is == to any other ValueError, regardless of their contents.
           str ( ValueError ( "`columns_matching_regexes_if_one_to_one_correspondence`: wrong number (should be 1) of column name matches to at least one regex.",
                              [ ("a.*", # matches too many
                                 ["a","ab"] ) ] ) ) )

  with pytest.raises(ValueError) as excinfo:
    columns_matching_regexes_if_one_to_one_correspondence ( df, ["x","y"] )
  assert ( str(excinfo.value) ==
           str ( ValueError ( "`columns_matching_regexes_if_one_to_one_correspondence`: wrong number (should be 1) of column name matches to at least one regex.",
                              [ ("x", # matches none
                                 [] ),
                                ("y", # matches none
                                 [] ),
                               ] ) ) )

def test_spreadsheets_with_fn_matches ():
  df = pd.DataFrame ( {
    "file"   : ["a", "a","b",  "b" , "b"],
    "column" : ["a1","a2","b3","b4", "b5"] } )

  assert (
    spreadsheets_with_fn_matches ( colnames_by_file = df,
                                   expr = "a.*",
                                   fn = lambda x: x > 1 )
    . equals (
      pd.DataFrame ( { "file"    : ["a"],
                       "columns" : [2] } ) ) )

  swfm = spreadsheets_with_fn_matches (
    # Nothing in `df` satisfies these conditions,
    # so the returned frame is empty -- but since matches are found,
    # there are at least column names in the returned frame.
    #
    # PITFALL: Unbelievably, Pandas says that this does not `.equals`
    # pd.DataFrame ( [], columns = ["file","columns"] )
    # so instead I have to test the columns and index separately.
    colnames_by_file = df,
    expr = "a.*",
    fn = lambda x: x > 2 )
  assert list ( swfm.columns ) == ["file","columns"]
  assert len ( swfm.index ) == 0

  assert (
    spreadsheets_with_fn_matches ( colnames_by_file = df,
                                   expr = ".",
                                   fn = lambda x: x > 1 )
    . equals (
      pd.DataFrame ( {
        "file"    : ["a","b"],
        "columns" : [2,3] } ) ) )

  assert (
    spreadsheets_with_fn_matches (
      # Nothing in `df` satisfies these conditions,
      # so the returned frame is empty.
      colnames_by_file = df,
      expr = "x",
      fn = lambda x: x == 0 )
    . equals (
      pd.DataFrame ( [], columns = [] ) ) )

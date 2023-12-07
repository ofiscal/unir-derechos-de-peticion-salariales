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

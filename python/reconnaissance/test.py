import pandas as pd
#
import python.reconnaissance.defs as defs


def test_number_of_matches_and_first_column_to_match ():
  assert (
    defs.number_of_matches_and_first_column_to_match (
      expr = ".*a.*",
      df = pd.DataFrame ( {"left noise"  : ["x","ba"],
                           "right noise" : ["ab","x"],
                           "caps"        : ["AB","X"],
                           "no match"    : ["y","x"],
                           "two matches" : ["a","a"] } ) )
    == ( 5,    # 5 matches total
         0 ) ) # the first column has the first match
  assert (
    defs.number_of_matches_and_first_column_to_match (
      expr = ".*a.*",
      df = pd.DataFrame ( {"no match"    : ["y","x"],
                           "caps"        : ["AB","X"],
                           "right noise" : ["ab","x"],
                           "two matches" : ["a","a"] } ) )
    == ( 4,    # 4 matches total
         1 ) ) # the second column has the first match

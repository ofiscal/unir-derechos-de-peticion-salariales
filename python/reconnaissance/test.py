import pandas as pd
#
import python.reconnaissance.defs as defs


def test_count_cells_matching_expr_in_sheet ():
  assert (
    defs.count_cells_matching_expr_in_sheet (
      expr = ".*a.*",
      df = pd.DataFrame ( {"left noise"  : ["x","ba"],
                           "right noise" : ["ab","x"],
                           "caps"        : ["AB","X"],
                           "no match"    : ["y","x"],
                           "two matches" : ["a","a"] } ) )
    == ( 5,    # 5 matches total
         0 ) ) # the first column has the first match
  assert (
    defs.count_cells_matching_expr_in_sheet (
      expr = ".*a.*",
      df = pd.DataFrame ( {"no match"    : ["y","x"],
                           "caps"        : ["AB","X"],
                           "right noise" : ["ab","x"],
                           "two matches" : ["a","a"] } ) )
    == ( 4,    # 4 matches total
         1 ) ) # the second column has the first match

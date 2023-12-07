import os
import pandas as pd
import pickle
from   typing import *
#
import python.paths as paths
from   python.types import *


column_name_regexes = [
  ( ".*"                                               +
    ".*".join ( [ "denom.*cargo" for _ in range(4) ] ) +
    ".*" )                              , # Perfect.
  "grado[^-]*"                          , # 1 multiple match. Taking the last match solves it.
  "no.*cargo.*:3$"                      , # Perfect.
  "salario.*comun.*subtotal.*"          , # Perfect.
  ".*remuneraciones.*remun.*subtotal.*" , # Perfect
  ".*inherentes.*total.*10"             , # Perfect
  "prestac.*social.*relac.*total.*"     , # 1 multiple and 2 not found
  ".*total.*:.*gastos.*:.*personal.*"   , # Many multi-matches. Taking the first match might work, but first see what happens if I drop the first empty column and everything after it that follows a match to "total.*gasto.*personal.*"
]

def mk_colnames_by_file ( successes : pd.DataFrame
                         ) ->         pd.DataFrame:
  """Create `colnames_by_file`, a data frame
  with two columns: ["column [name]", "file"]."""
  colnames_by_file_list = []
  for k in successes.keys():
    df = pd.DataFrame ( { "column" : successes[k] . columns } )
    df["file"] = k
    colnames_by_file_list . append ( df )
  colnames_by_file = (
    pd.concat ( # default `axis` : preserve width and grow length
      colnames_by_file_list )
    . reset_index ( drop=True ) )
  assert ( len ( colnames_by_file["file"] . unique() ) ==
           len ( list ( successes.keys() ) ) )
  return colnames_by_file

def summarize_matches_to_expr (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr          : str,
): # pure IO (printing)
  # How many unique column names matching some regexes
  df = colnames_by_file . copy ()
  df["match"] = ( df["column"]
                  . str.match ( expr,
                                case = False ) )
  df["one"] = 1
  agg : pd.DataFrame = ( # columns = [ "file",
                         #             "[number of] matches" ]
    df [ df["match"] ] # only rows that match
    [["file","one"]]
    . groupby ( "file" )
    . sum ()
    . rename ( columns = {"one" : "matches"} )
    . reset_index () )
  if True: # make `agg2` with columns = [ "[number of] matches",
           #                              "[number of] files" ]
    agg2 : pd.DataFrame = agg.copy()
    agg2["one"] = 1
    agg2 : pd.DataFrame  = (
      agg2 [["matches","one"]]
      . groupby ( "matches" )
      . sum ()
      . rename ( columns  = { "one" : "files" } ) )
  print ()
  print (expr)
  print ( "Unique files with a match:",
          len ( agg["file"] . unique () ) )
  print ( "How the number of matches varies across files: " )
  # print ( agg["matches"] . describe () )
  print ( agg2 )

def find_matches (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr             : str,
) -> List [ str ]:
  """All unique matches, regardless of source file."""
  return list ( colnames_by_file
                [ colnames_by_file["column"]
                  . str.match ( expr,
                                case = False ) ]
                ["column"]
                . unique () )

def spreadsheets_with_fn_matches (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr             : str,
    fn               : Callable [[int],bool],
) -> pd.DataFrame:
  """ `spreadsheets_with_fn_matches (colnames_by_file, expr, fn)` returns a series of filenames such that the number of columns in the sheet associated with that filename satisfies `fn`."""
  df = ( colnames_by_file . copy ()
         [ colnames_by_file["column"]
           . str.match ( expr,
                         case = False ) ] )
  df["one"] = 1
  agg = ( df [["file", "one"]]
         . groupby ( "file" )
         . sum ()
         . reset_index ()
         . rename ( columns = {"one" : "columns"} ) )
  return agg [ agg [ "columns" ] . apply ( fn ) ]

def columns_matching_regexes_if_one_to_one_correspondence (
    df : pd.DataFrame,
    exprs   : List [ str ], # regexes for column names
) -> pd.DataFrame: # A subset of the columns of `df`.
  """Returns the subset of the columns in `df` that match one of the regexes in `exprs`, IFF exactly one column matches each regex. If anything else happens, this raises a `ValueError`."""
  expr_match_pair_list : \
    List [ List [ Tuple [ str,
                          List [str] ] ] ] = \
    [ ( expr,  # the regex
        list ( # the matches
          pd.Series ( df.columns )
          [ pd.Series ( df.columns )
            . str.match ( expr ) ] ) )
      for expr in exprs ]
  non_unit_matches = [ m for m in expr_match_pair_list
                       if len ( m[1] ) != 1 ]
  try:
    assert not non_unit_matches # it is empty
  except:
    raise ValueError (
      "`columns_matching_regexes_if_one_to_one_correspondence`: wrong number (should be 1) of column name matches to at least one regex.",
      non_unit_matches )
  return df [ [ expr
                for (expr,_) in expr_match_pair_list ] ]

def count_matches_in_spreadsheets_with_fn_matches (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr             : str,
    fn               : Callable [[int],bool],
) -> pd.DataFrame:
  """ `count_matches_in_spreadsheets_with_fn_matches (colnames_by_file, expr, fn)` returns a spreadsheet with columns ["file"    : str,
                                      "columns" : int],
  that shows all files for which the number n of matches satisfies `fn`. For instance, if `fn = lambda x: x > 1`, it only returns agencies for which the number of matches is greater than 1."""
  df = ( colnames_by_file . copy ()
         [ colnames_by_file["column"]
           . str.match ( expr,
                         case = False ) ] )
  df["one"] = 1
  agg = ( df [["file", "one"]]
         . groupby ( "file" )
         . sum ()
         . reset_index ()
         . rename ( columns = {"one" : "columns"} ) )
  return agg [ agg [ "columns" ] . apply ( fn ) ]

def matches_in_spreadsheets_with_multiple_matches (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr             : str,
) -> pd.DataFrame:
  match_counts = \
    count_matches_in_spreadsheets_with_fn_matches (
      colnames_by_file = colnames_by_file,
      expr             = expr,
      fn               = lambda x: x > 1, )
  colnames_by_file_limited = \
    colnames_by_file . merge ( match_counts [["file"]],
                            on = "file",
                            how = "inner" )
  return ( colnames_by_file_limited
           [ colnames_by_file_limited ["column"]
             . str.match ( expr, case = False ) ] )

def files_with_no_column_matching_expr (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr             : str,
) -> pd.DataFrame:
  df = colnames_by_file . copy ()
  df["does match"] = ( df["column"]
                       . str.match ( expr,
                                     case = False )
                       . astype ( int ) ) # convert from bool
  agg = ( df . groupby ("file")
          . sum ()
          . rename ( columns = {"does match" : "matches"} ) )
  return agg [ agg["matches"] < 1 ]

def summarize_expr_in_column_names (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr             : str,
): # pure IO
  print ( expr )
  print ( summarize_matches_to_expr (
    colnames_by_file     = colnames_by_file,
    expr                 = expr ) )
  print (
    "Files with more than one match:\n",
    count_matches_in_spreadsheets_with_fn_matches (
      colnames_by_file   = colnames_by_file,
      expr               = expr,
      fn                 = lambda x: x > 1, ) )
  print (
    "Matches_in_spreadsheets_with_multiple_matches:\n",
    ( matches_in_spreadsheets_with_multiple_matches
      ( colnames_by_file = colnames_by_file,
        expr             = expr )
      ["column"] . unique () ) )

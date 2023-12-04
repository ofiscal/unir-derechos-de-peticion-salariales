import os
import pandas as pd
import pickle
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

def mk_names_by_file ( successes : pd.DataFrame
                      ) ->         pd.DataFrame:
  """Create `names_by_file`, a data frame
  with two columns: ["column [name]", "file"]."""
  names_by_file_list = []
  for k in successes.keys():
    df = pd.DataFrame ( { "column" : successes[k] . columns } )
    df["file"] = k
    names_by_file_list . append ( df )
  names_by_file = (
    pd.concat ( # default `axis` : preserve width and grow length
      names_by_file_list )
    . reset_index ( drop=True ) )
  assert ( len ( names_by_file["file"] . unique() ) ==
           len ( list ( successes.keys() ) ) )
  return names_by_file

def summarize_matches_to_expr (
    names_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr          : str,
): # pure IO (printing)
  # How many unique column names matching some regexes
  df = names_by_file . copy ()
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

def find_matches ( expr : str ) -> pd.Series:
  """All unique matches, regardless of source file."""
  return ( names_by_file
           [ names_by_file["column"]
             . str.match ( expr,
                           case = False ) ]
           ["column"]
          . unique () )

def count_matches_in_spreadsheets_with_multiple_matches (
    names_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr          : str,
) -> pd.DataFrame: # Columns ["file"    : str,
                   #          "columns" : int].
  df = ( names_by_file . copy ()
         [ names_by_file["column"]
           . str.match ( expr,
                         case = False ) ] )
  df["one"] = 1
  agg = ( df [["file", "one"]]
         . groupby ( "file" )
         . sum ()
         . reset_index ()
         . rename ( columns = {"one" : "columns"} ) )
  return agg [ agg [ "columns" ] > 1 ]

def matches_in_spreadsheets_with_multiple_matches (
    names_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr : str,
) -> pd.DataFrame:
  match_counts = \
    count_matches_in_spreadsheets_with_multiple_matches (
      names_by_file = names_by_file,
      expr          = expr )
  names_by_file_limited = \
    names_by_file . merge ( match_counts [["file"]],
                            on = "file",
                            how = "inner" )
  return ( names_by_file_limited
           [ names_by_file_limited ["column"]
             . str.match ( expr, case = False ) ] )

def files_with_no_column_matching_expr ( expr : str ):
  df = names_by_file . copy ()
  df["does match"] = ( df["column"]
                       . str.match ( expr,
                                     case = False )
                       . astype ( int ) ) # convert from bool
  agg = ( df . groupby ("file")
          . sum ()
          . rename ( columns = {"does match" : "matches"} ) )
  return agg [ agg["matches"] < 1 ]

def summarize_expr_in_column_names (
    names_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr          : str,
): # pure IO
  print ( expr )
  print ( summarize_matches_to_expr (
    names_by_file = names_by_file,
    expr          = expr ) )
  print ( count_matches_in_spreadsheets_with_multiple_matches (
    names_by_file = names_by_file,
    expr          = expr ) )
  print ( matches_in_spreadsheets_with_multiple_matches
          ( names_by_file = names_by_file,
            expr          = expr )
          ["column"] . unique () )

# Interactively inspect `python.main.successes`

import os
import pandas as pd
import pickle
#
import python.paths as paths


if True: # Choose one
  if False: # Including but disabling this import
            # squashes a `pytest` complaint that `successes` is not defined.
            # I don't actually evaluate the import because it's slow,
            # and I have already evaluated `python.main` in the REPL.
    from python.main import successes
  if True:
    # Load (deserialize) data from `python.main`.
    # This lets me skip running `main`.
    with open ( os.path.join ( paths.latest_pickle_path,
                               "successes.pickle", ),
                "rb") as handle:
        successes = pickle . load ( handle )

if True: # Create `names_by_file`, a data frame
         # with two columns: "column name" and "file"
  names_by_file_list = []
  for k in successes.keys():
    df = pd.DataFrame ( { "column" : successes[k] . columns } )
    df["file"] = k
    names_by_file_list . append ( df )
  names_by_file = (
    pd.concat ( # default `axis` : preserve width and grow length
      names_by_file_list )
    . reset_index ( drop=True ) )
  del (k, df, names_by_file_list)
  assert ( len ( names_by_file["file"] . unique() ) ==
           len ( list ( successes.keys() ) ) )

def summarize_matches_to_expr ( expr : str ): # pure IO (printing)
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
    expr : str
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
    expr : str,
) -> pd.DataFrame:
  match_counts = \
    count_matches_in_spreadsheets_with_multiple_matches ( expr )
  names_by_file_limited = \
    names_by_file . merge ( match_counts [["file"]],
                            on = "file",
                            how = "inner" )
  return ( names_by_file_limited
           [ names_by_file_limited ["column"]
             . str.match ( expr, case = False ) ] )

def summarize_expr_in_column_names ( expr : str ):
  print ( expr )
  print ( summarize_matches_to_expr ( expr ) )
  print ( count_matches_in_spreadsheets_with_multiple_matches ( expr ) )
  print ( matches_in_spreadsheets_with_multiple_matches ( expr )
          ["column"] . unique () )

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

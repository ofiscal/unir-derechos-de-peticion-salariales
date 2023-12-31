import os
import pandas as pd
import pickle
from   typing import *
#
import python.paths as paths
from   python.types import *


column_name_regexes : Dict [ str, str ] =  {
  # PITFALL: The order of this dictionary
  # matters for the definitions of these variables:
  #   column_names
  #   cop_columns
  #   num_columns
  "cargo" : ( ".*"                                +
              ".*".join ( [ "denom.*cargo"
                            for _ in range(4) ] ) +
              ".*" )                                         ,
  "nivel 1"        : "empleado kind 1"                       ,
  "nivel 2"        : "empleado kind 2"                       ,
  "grado"          : "grado[^-]*"                            ,
  "# cargos"       : "no.*cargo.*:3$"                        ,
  "sueldo basico"  : ".*b.sico.*anual.*"                     ,
  "salario"        : "salario.*total.*total.*total.*"        ,
  "remuneraciones" : "remuneraciones.*total.*total.*total.*" ,
  "contribuciones" : ".*inherentes.*total.*10"               ,
  "prestaciones"   : "prestac.*social.*relac.*total.*"       ,
  "gasto total"    : ".*total.*:.*gastos.*:.*personal.*"     ,
}

column_names = list ( column_name_regexes.keys() )
cop_columns = column_names [-6:] # the last 6 columns are COP-valued
num_columns = (
  [ "# cargos",
    # "grado", # TODO: Supposed to be numeric, but needs much cleaning.
   ] +
  column_names [-6:] )


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
    expr             : str,
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
) -> pd.DataFrame: # columns: ["file","n columns"]
  """ `spreadsheets_with_fn_matches (colnames_by_file, expr, fn)` returns a series of filenames such that the number of columns in the sheet associated with that filename satisfies `fn`.

  PITFALL: The name is a bit misleading, because if no columns in a file match the expr, then that file will not appear in the results -- even if `fn` is `lambda x: x == 0`.
  """
  df = ( colnames_by_file . copy ()
         [ colnames_by_file["column"]
           . str.match ( expr,
                         case = False ) ] )
  df["one"] = 1
  agg = ( df [["file", "one"]]
         . groupby ( "file" )
         . sum ()
         . reset_index ()
         . rename ( columns = {"one" : "n columns"} ) )
  return agg [ agg [ "n columns" ] . apply ( fn ) ]

def spreadsheets_with_1_match_to_each_expr (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    exprs            : List [str],
) -> Set [ str ]: # strings from the "file" column of `colnames_by_file`
  sets_of_matching_files : List [ Set [ str ] ] = [
    set (
      spreadsheets_with_fn_matches ( colnames_by_file = colnames_by_file,
                                     expr = expr,
                                     fn = lambda x: x == 1 )
      ["file"] )
    for expr in exprs ]
  return set.intersection ( *sets_of_matching_files )

def columns_matching_regexes_if_one_to_one_correspondence (
    df    : pd.DataFrame,
    exprs : List [ str ], # regexes for column names
) -> pd.DataFrame: # A subset of the columns of `df`.
  """Returns the subset of the columns in `df` that match one of the regexes in `exprs`, IFF exactly one column matches each regex. If anything else happens, this raises a `ValueError`."""
  expr_match_pair_list : \
    List [ List [ Tuple [ str,
                          List [str] ] ] ] = \
    [ ( expr,  # the regex
        list ( # the matches
          pd.Series ( df.columns )
          [ pd.Series ( df.columns )
            . str.match ( expr,
                          case = False ) ] ) )
      for expr in exprs ]
  non_unit_matches = [ m for m in expr_match_pair_list
                       if len ( m[1] ) != 1 ]
  try:
    assert not non_unit_matches # it is empty
  except:
    raise ValueError (
      "`columns_matching_regexes_if_one_to_one_correspondence`: wrong number (should be 1) of column name matches to at least one regex.",
      non_unit_matches )
  return df [ [ match
                for (_,[match]) in expr_match_pair_list ] ]

def subset_columns_by_regex_and_concatenate (
    dfs_by_file : Dict [ str, # original Excel filename
                         pd.DataFrame ],
    exprs       : Dict [ str, str ], # (name : regex) for each column name
) -> pd.DataFrame:
  dfs : List [ pd.DataFrame ] = [] # accumulator
  for f,df0 in dfs_by_file.items():
    df = ( columns_matching_regexes_if_one_to_one_correspondence (
             df = df0,
             exprs = list ( exprs . values () ) )
          . copy () )
    df.columns = list ( exprs . keys () ) # rename columns for
                                          # homogeneity across files
    df [ "Excel file" ] = f
    dfs.append ( df )
  return pd.concat ( dfs ) . reset_index ( drop = True )

def count_matches_in_spreadsheets_with_fn_matches (
    colnames_by_file : pd.DataFrame, # columns: ["column [name]", "file"]
    expr             : str,
    fn               : Callable [[int],bool],
) -> pd.DataFrame:
  """ `count_matches_in_spreadsheets_with_fn_matches (colnames_by_file, expr, fn)` returns a spreadsheet with columns ["file"      : str,
                                         "n columns" : int],
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
         . rename ( columns = {"one" : "n columns"} ) )
  return agg [ agg [ "n columns" ] . apply ( fn ) ]

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

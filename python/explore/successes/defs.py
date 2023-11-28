# Interactively inspect `python.main.successes`

import pandas as pd
import pickle
if False: # Including but disabling this import
          # squashes a `pytest` complaint that `successes` is not defined.
          # I don't actually evaluate the import because it's slow,
          # and I have already evaluated `python.main` in the REPL.
  from python.main import successes


# Load (deserialize) data from `python.main`.
# This lets me skip running `main`.
with open ( "successes.pickle", "rb") as handle:
    successes = pickle . load ( handle )

# An exemplar: The first element of successes.
k0 = list(successes.keys()) [0]
v0 = successes[k0]
c0 = list(v0.columns)

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

# How many files were read successfully
len ( names_by_file["file"] . unique() )

# How many unique column names
len ( names_by_file["column"] . unique() )

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

exprs = [ # columns we want
  ".*denom.*cargo.*"   ,
  "grado.*"            , # INTENTIONAL : no leading .*
  ".*no.*cargo.*"      ,
  ".*salario.*"        ,
  ".*remuneraciones.*" ,
  ".*inherentes.*"     ,
  ".*prestac.*social.*",
  ".*total.*gasto.*"   , ]

for expr in exprs: summarize_matches_to_expr ( expr )
del(expr)

# When multiple columns match in a file,
# what are those columns?

def find_spreadsheets_with_multiple_matches (
    expr : str
) -> pd.DataFrame:
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

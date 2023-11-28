# Interactively inspect `python.main.successes`

import pandas as pd
if False: # Including but disabling this import
          # squashes a `pytest` complaint that `successes` is not defined.
          # I don't actually evaluate the import because it's slow,
          # and I have already evaluated `python.main` in the REPL.
  from python.main import successes


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

# How many unique column names matching some regexes
for expr in [".*denom.*cargo.*",
             ".*grado.*",
             ".*no.*cargo.*",
             ".*total.*gasto.*" ]:
  df = names_by_file . copy ()
  df["match"] = ( df["column"]
                  . str.match ( expr,
                                case = False ) )
  df["one"] = 1
  agg = ( # columns = [ "file",
          #             "[number of] matches" ]
    df [ df["match"] ] # only rows that match
    [["file","one"]]
    . groupby ( "file" )
    . sum ()
    . rename ( columns = {"one" : "matches"} )
    . reset_index () )
  if True:
    agg2 = agg.copy()
    agg2["one"] = 1
    agg2 = ( # columns = [ "[number of] matches",
             #             "[number of] files" ]
      agg2 [["matches","one"]]
      . groupby ( "matches" )
      . sum ()
      . rename ( columns  = { "one" : "files" } ) )
  print ()
  print (expr)
  print ( "unique files with a match:",
          len ( agg["file"] . unique () ) )
  print ( "how the number of matches varies across files: " )
  print ( agg["matches"] . describe () )
  print ( agg2 )

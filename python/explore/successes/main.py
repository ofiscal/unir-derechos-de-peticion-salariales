# Interactively inspect `python.main.successes`

import os
import pandas as pd
import pickle
from   typing import Dict
#
import python.paths as paths
from   python.types import *
import python.explore.successes.defs as defs


successes_strategy = Definition_Strategy.Load_from_pickle

if True: # Define `successes`
  if successes_strategy == Definition_Strategy.Already_defined:
    pass
  elif successes_strategy == Definition_Strategy.Create:
    # PITFALL: SLOW.
    # Run the code that defines `successes`.
    from python.main import successes, file_load_instructions
  elif successes_strategy == Definition_Strategy.Load_from_pickle:
    with open ( os.path.join ( paths.latest_pickle_path,
                               "successes.pickle", ),
                "rb") as handle:
      successes : Dict [ str, pd.DataFrame ] = \
        pickle . load ( handle )
    with open ( os.path.join ( paths.latest_pickle_path,
                               "load_instructions.pickle", ),
                "rb") as handle:
      load_instructions : Dict [ str, pd.DataFrame ] = \
        pickle . load ( handle )

names_by_file : pd.DataFrame = \
  defs.mk_names_by_file ( successes )


###############
# Futz around #
###############

# How many files were read successfully
len ( names_by_file["file"] . unique() )

# How many unique column names
len ( names_by_file["column"] . unique() )

# An exemplar: The first element of successes.
k0 = list(successes.keys()) [0]
v0 = successes[k0]
c0 = list(v0.columns)

# Pretty good -- 114 have well-behaved column names.
for expr in defs.column_name_regexes:
  print ()
  defs.summarize_expr_in_column_names (
    names_by_file = names_by_file,
    expr = expr)

expr = ".*total.*:.*gastos.*:.*personal.*"
defs.summarize_expr_in_column_names (
  names_by_file = names_by_file,
  expr          = expr )

( defs.matches_in_spreadsheets_with_multiple_matches
  ( names_by_file = names_by_file,
    expr          = expr ) )
( defs.matches_in_spreadsheets_with_multiple_matches
  ( names_by_file = names_by_file,
    expr          = expr )
  ["column"] . unique() )
( defs.matches_in_spreadsheets_with_multiple_matches
  ( names_by_file = names_by_file,
    expr          = expr )
  ["file"] . unique() )

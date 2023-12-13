import pandas as pd
import re
from   typing import *
#
import python.explore.successes.defs as defs
import python.paths as paths
from   python.types import *
from   python.util import str_to_float


def join_successfully_read_excel_files (
    successes : Dict [ str, # path to agency file
                       pd.DataFrame ]
    ) -> pd.DataFrame:

  colnames_by_file : pd.DataFrame = \
    defs.mk_colnames_by_file ( successes )

  extra_nice : List[str] = list (
    defs.spreadsheets_with_1_match_to_each_expr (
      colnames_by_file = colnames_by_file,
      exprs = list ( defs.column_name_regexes
                     . values () )
    ) )

  together : pd.DataFrame = defs.subset_columns_by_regex_and_concatenate (
    dfs_by_file = { k : successes[k]
                    for k in extra_nice },
    exprs = defs.column_name_regexes )

  for colname in ( list ( defs.column_name_regexes . keys() )
                   [2:] ): # The first two aren't floats.
    together[colname] = str_to_float (
      together[colname] )

  together["agency"] = (
    together["Excel file"]
    . apply (
      lambda path:
      re.sub (
        "^[^a-zA-Z]*", # find the longest leading substring with no alphas
        "",            # and delete it
        path.split ("/") [0]
      ) ) )

  return together

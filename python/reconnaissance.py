# WHAT THIS DOES:
# (More might be added to this.)
# Determine how many "Denominación de Cargos" and "Libre Nombramiento"
# cells a sheet has.
# Build tables identifying,
# for each sheet of each Excel file from each agency,
# how many of those cells it has.
#
# WHY:
# A summary planta file (which we don't want)
# looks like a person-level planta file (which we want),
# in that both contain "denominación de cargos" cells.
# But the summary file includes a "libre nombramiento" cell too,
# whereas the person-level ones don't.
#
# Therefore this program looks for sheets
# with a denominación de cargos cell and no libre nombramiento cell.
# A sheet is defined as "nice" if it has denominación de cargos
# and does not have libre nombramiento.
# The sheet reports are partitioned into three groups:
# agencies with no nice sheet, agencies with exactly one,
# and agencies with more than one.
#
# But a fourth kind of sheet is also reported on:
# sheets with too many denominación de cargos cells.
# The idea here is to catch sheets where someone might have
# included both tables. Hopefully nobody did that.

from   dataclasses import dataclass
import os
import pandas as pd
import re
from   typing import Dict, List, Tuple
#
from   python.clean_one_file.defs import denominacion_pattern, libre_pattern
import python.find_files.defs as find_files
from   python.paths import agency_root
from   python.types import *


unit_of_observation = [ "agency", "file", "sheet" ]

def count_cells_matching_expr_in_sheet (
    expr : str,
    df   : pd.DataFrame,
) ->  int:
  return ( df
           . astype ( str )
           . applymap ( lambda s:
                        bool ( re.match ( expr,
                                          s,
                                          flags = re.IGNORECASE ) ) )
           . astype (int)
           . sum() . sum() ) # two-dimensional sum

def all_denom_and_libre_cell_counts (
    limit   : int  = 0, # How many agencies to scan (default = all).
    verbose : bool = False, # For debugging.
    # TODO: Exceptions would be friendlier than debugging the verbose output.
    # Ideally, use both, as printing filenames is helpful
    # for gauging the speed of the algorithm.
) -> pd.DataFrame:
  """Returns a frame with
columns = unit_of_observation + ["denom_cells", "libre_cells"].
"""
  paths = find_files.paths_from_argument_to_filenames_matching_pattern (
    pattern = ".*\\.xls[a-zA-Z]*$", # excludes lock files, which end in #
      # (and which go stale on Linux when LibreOffice exits abnormally).
    path0 = "data/input/agency_responses/" )
  eds = find_files.excel_descendents_by_agency ( paths )

  acc = pd.DataFrame ( [],
                       columns = ( unit_of_observation +
                                   ["denom_cells", "libre_cells"] ) )
  for k in list ( eds.keys() ) [-limit:]:
    for v in eds[k]:
      filename = os.path.join ( agency_root, k, v )
      if verbose: print(filename)
      for sn in pd.ExcelFile (filename) . sheet_names:
        new_row = pd.Series (
          { "agency"            : k,
            "file"              : v,
            "sheet"             : sn,
            "denom_cells" : count_cells_matching_expr_in_sheet (
              expr = denominacion_pattern,
              df   = pd.read_excel ( io         = filename,
                                     sheet_name = sn ) ),
            "libre_cells" : count_cells_matching_expr_in_sheet (
              expr = libre_pattern,
              df   = pd.read_excel ( io         = filename,
                                     sheet_name = sn ) ),
           } )
        acc = pd.concat ( [ acc,
                            pd.DataFrame ( new_row ) . transpose() ],
                          axis = "rows" )
  acc["nice"] = ( ( ( acc["denom_cells"] == 1 ) &
                    ( acc["libre_cells"] == 0 ) )
                  . astype ( int ) )
  return acc

def denom_cell_reports (
    limit : int = 0, # How many agencies to scan (default = all).
    verbose : bool = False,
) -> Dict [ str, pd.DataFrame ]:
  df = all_denom_and_libre_cell_counts ( limit   = limit,
                                         verbose = verbose, )
  g = ( df [ ["agency", "nice"] ]
        . groupby ( "agency" )
        . agg ( sum )
        . reset_index () )
  g = g.rename ( columns = { "nice" : "nice_sheets" } )
  df = df.merge ( g, on = "agency" )
  return {
    # The following three groups do not overlap.
    "sheets_of_agencies_with_no_nice_sheet" :
      df [   df ["nice_sheets"] == 0 ],
    "nice_sheets_of_agencies_with_one_nice_sheet" :
      df [ ( df ["nice_sheets"] == 1 ) &
           ( df ["nice" ]       == 1 ) ],
    "nice_sheets_of_agencies_with_multiple_nice_sheets" :
      df [ ( df ["nice_sheets"] >  1 ) &
           ( df ["nice" ]       == 1 ) ],

    # These (non-nice) sheets could be from any of the agencies
    # described in the preceding three tables,
    # and might even overlap with sheets in the first of those partitions.
    "sheets_with_multiple_denom_cells" :
      df [   df ["denom_cells"] > 1 ] }

# A quick way to test that.
#   rs = denom_cell_reports ( limit = 1 )

# PURPOSE:
# (More might be added to this.)
# Determine how many "denominación de cargos" cells a file has.
# If more than one, we'll have more work to do.

from   dataclasses import dataclass
import os
import pandas as pd
import re
from   typing import Dict, List, Tuple
#
from   python.clean_one_file.defs import denominacion_pattern
import python.find_files.defs as find_files
from   python.types import *


def count_sheet_denom_cells ( df : pd.DataFrame
                       ) ->  int:
  return ( df
           . astype ( str )
           . applymap ( lambda s:
                        bool ( re.match ( denominacion_pattern,
                                          s,
                                          flags = re.IGNORECASE ) ) )
           . astype (int)
           . sum() . sum() ) # two-dimensional sum

def all_denom_cell_counts (
    limit : int = 0 # How many agencies to scan (default = all).
) -> pd.DataFrame:
  """Returns a frame with
columns = ["agency", "file", "sheet", "sheet_denom_cells"].
"""
  paths = find_files.paths_from_argument_to_filenames_matching_pattern (
    pattern = ".*\\.xls.*",
    path0 = "data/input/agency_responses/" )
  eds = find_files.excel_descendents_by_agency ( paths )

  acc = pd.DataFrame (
    [],
    columns = ["agency", "file", "sheet", "sheet_denom_cells"] )
  for k in list ( eds.keys() ) [-limit:]:
    for v in eds[k]:
      filename = os.path.join ( find_files.agency_response_folder, k, v )
      for sn in pd.ExcelFile (filename) . sheet_names:
        new_row = pd.Series (
          { "agency"            : k,
            "file"              : v,
            "sheet"             : sn,
            "sheet_denom_cells" : count_sheet_denom_cells (
              pd.read_excel ( io         = filename,
                              sheet_name = sn ) )
           } )
        acc = pd.concat ( [ acc,
                            pd.DataFrame ( new_row ) . transpose() ],
                          axis = "rows" )
  return acc

def denom_cell_report (
    limit : int = 0 # How many agencies to scan (default = all).
) -> Tuple [
    # The unit of observation in each of these frames is a sheet.
    pd.DataFrame,    # agencies with no            denom cell
    pd.DataFrame,    # agencies with exactly   one denom cell
    pd.DataFrame, ]: # agencies with more than one denom cell
  df = all_denom_cell_counts ( limit = limit )
  g = ( df.groupby ( "agency" )
        . agg ( sum )
        . reset_index () )
  g = g.rename (
    columns = {"sheet_denom_cells" : "agency_denom_cells"} )
  df = df.merge (
    g [[ "agency", "agency_denom_cells" ]],
    on = "agency" )
  return ( df [ df ["agency_denom_cells"] == 0 ],
           df [ ( df ["agency_denom_cells"] == 1 ) &
                ( df ["sheet_denom_cells" ] >  0 ) ],
           df [ ( df ["agency_denom_cells"] >  1 ) &
                ( df ["sheet_denom_cells" ] >  0 ) ],


#######################################################
# SOON TO BE REPLACED
# The code below does not scan all files or all sheets.
#######################################################

( planta_candidates,
  multiple_planta_file_agencies,
  no_planta_file_agencies
 ) = find_files.planta_candidates_and_ambiguous_agencies ()

file_results : Dict [ str, # filename
                      Dict [ str, # sheet name
                             int # number of "denom cargo" cells
                            ] ] = {}
for f in planta_candidates:
  ef = pd.ExcelFile ( f )
  sheet_results : Dict [ str, int ] = {}
  for sn in ef.sheet_names:
    sheet_results [ sn ] = count_denom_cells (
      pd.read_excel ( io         = f,
                      sheet_name = sn ) )
  file_results [f] = sheet_results

s = pd.Series (
  [ sum ( file_results[k] . values() )
    for k in file_results.keys() ] )

s.describe()

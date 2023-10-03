# PURPOSE:
# (More might be added to this.)
# Determine how many "denominación de cargos" cells a file has.
# If more than one, we'll have more work to do.

from   dataclasses import dataclass
import pandas as pd
import re
#
from   python.clean_one_file.defs import denominacion_pattern
from   python.find_files.defs import planta_candidates_and_ambiguous_agencies


def count_denom_cells ( df : pd.DataFrame
                       ) ->  int:
  return ( df
           . astype ( str )
           . applymap ( lambda s:
                        bool ( re.match ( denominacion_pattern,
                                          s,
                                          flags = re.IGNORECASE ) ) )
           . astype (int)
           . sum() . sum() ) # two-dimensional sum

( planta_candidates,
  multiple_planta_file_agencies,
  no_planta_file_agencies
 ) = planta_candidates_and_ambiguous_agencies ()

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

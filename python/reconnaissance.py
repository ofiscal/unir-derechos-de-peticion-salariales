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
                        bool ( re.match( denominacion_pattern,
                                         s ) ) )
           . astype (int)
           . sum() . sum() ) # two-dimensional sum

@dataclass
class Sheet_recon:
  sheet       : int
  denom_cells : int

@dataclass
class File_recon:
  filename    : str
  sheet       : int

( planta_candidates,
  multiple_planta_file_agencies,
  no_planta_file_agencies
 ) = planta_candidates_and_ambiguous_agencies ()

file_results = {}
for f in planta_candidates:
  n_sheets = len ( pd.ExcelFile( f )
                 . sheet_names )
  sheet_results = {}
  for s in range( n_sheets ):
    sheet_results [ f ] = Sheet_recon (
      sheet       = s,
      denom_cells = count_denom_cells (
        pd.read_excel ( io         = f,
                        sheet_name = s ) ) )
  sheet_recons = { k:v
                   for k,v in sheet_results.items()
                   if v.denom_cells > 0 }

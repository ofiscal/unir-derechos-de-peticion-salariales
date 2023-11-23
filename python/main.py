from   typing import Dict, List, Set, Tuple
#
import python.collect as collect
import python.exceptions.discoveries as discoveries
import python.find_files.defs as find_files
import python.paths as paths
import python.reconnaissance as recon
from   python.types import *


reports = recon.denom_cell_reports (
  limit = 0, # process everything
  verbose = True, )
for k, df in reports.items():
  df.to_csv ( k + ".csv" )


##################
# Needs rewriting
##################

# Define some paths.
( planta_candidates,             # files we want to ingest
  multiple_planta_file_agencies, # agencies with >1 file named "planta"
  no_planta_file_agencies        # agencies with no file named "planta"
 ) = find_files.planta_candidates_and_ambiguous_agencies ()

if True: # Test that all are accounted for.
  lengths = [ len(x) for x in [
    planta_candidates,
    multiple_planta_file_agencies,
    no_planta_file_agencies ] ]
  assert sum ( lengths ) == len ( find_files.agencies )

( successes, errors
 ) = collect.formatted_responses_and_errors (
   agency_root = paths.agency_root,
   source_files = (
     discoveries.exceptional_instruction_list
     + [ # non-exceptions
       File_Load_Instruction ( c )
       for c in planta_candidates
       if not c in ( discoveries.exceptional_instruction_dict
                     . keys () )
     ] ) )

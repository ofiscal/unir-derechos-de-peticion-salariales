from python.find_files.defs import (
  planta_candidates_and_ambiguous_agencies,
  agencies )
from python.collect import collect_formatted_responses
from typing import Dict, List, Set, Tuple


# Define some paths
( planta_candidates,             # files we want to ingest
  multiple_planta_file_agencies, # agencies with >1 file named "planta"
  no_planta_file_agencies        # agencies with no file named "planta"
 ) = planta_candidates_and_ambiguous_agencies ()

if True: # test that all are accounted for
  lengths = [ len(x) for x in [
    planta_candidates,
    multiple_planta_file_agencies,
    no_planta_file_agencies ] ]
  assert sum ( lengths ) == len ( agencies )

( successes, errors
 ) = collect_formatted_responses ( planta_candidates )

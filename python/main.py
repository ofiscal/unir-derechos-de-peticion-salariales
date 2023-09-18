from python.find_files.defs import planta_candidates_and_ambiguous_agencies
from python.collect import collect_formatted_responses
from typing import Dict, List, Set, Tuple


# Define some paths
( planta_candidates,             # files we want to ingest
  multiple_planta_file_agencies, # agencies with >1 file named "planta"
  no_planta_file_agencies        # agencies with no file named "planta"
 ) = planta_candidates_and_ambiguous_agencies ()

( successes, errors
 ) = collect_formatted_responses ( planta_candidates )

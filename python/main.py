from python.find_files import unique_planta_candidates
from python.collect import collect_formatted_responses
from typing import Dict, List, Set


planta_paths : List[str] = unique_planta_candidates ()
( successes, errors ) = (
  collect_formatted_responses ( planta_paths ) )

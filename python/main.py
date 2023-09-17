from python.find_files import unique_planta_candidates
from python.collect import collect_formatted_responses


planta_paths = unique_planta_candidates ()
( successes, errors ) = (
  collect_formatted_responses ( planta_paths ) )

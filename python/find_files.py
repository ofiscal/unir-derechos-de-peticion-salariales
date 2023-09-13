import os
import pandas as pd
import re
from   typing import List, Set, Dict


agency_responses = "data/input/agency-responses/"

def searchDirectory (
    pattern : str, # a regex
    path0 : str = ".",
    recursionCount = 0
) -> List[str]:
  """Case-insensitive basename regex matching."""
  # Inspired by
  # https://stackoverflow.com/questions/44805898/recursively-look-for-files-and-or-directories
  acc = [] # accumulates results
  dirs = os.listdir ( path0 )
  for dir in dirs:
    path1 = os.path.join ( path0, dir)
    if os.path.isdir ( path1 ):
      acc = ( acc +
              searchDirectory ( # recurse
                pattern = pattern,
                path0 = path1 ) )
    if re.search ( pattern, path1, re.IGNORECASE):
      acc.append ( path1 )
  return acc

# From 175 agencies, this identifies 161 candidate files.
planta_files = searchDirectory (
  pattern = "planta.*\.xls.$",
  path0 = agency_responses
)

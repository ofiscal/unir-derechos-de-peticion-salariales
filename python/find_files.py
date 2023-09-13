from   dataclasses import dataclass
import os
import pandas as pd
from   pathlib import Path
import re
from   typing import List, Set, Dict


agency_responses = "data/input/agency_responses/"

def searchDirectory (
    pattern : str, # a regex
    path0 : str = ".",
    recursionCount = 0
) -> List [ str ]:
  """Case-insensitive basename regex matching."""
  # Inspired by
  # https://stackoverflow.com/questions/44805898/recursively-look-for-files-and-or-directories
  acc : List [ str ] = [] # accumulates results
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

@dataclass
class genealogy:
  # Pairs would work too, but this type is easier to reason about.
  descendent : str # a path to an the Excel tables in `agency_responses`
  agency     : str # an immediate descendent of `agency_responses`

def genealogy_from_table ( descendent : str
                          ) -> genealogy:
  return genealogy (
    descendent = descendent,
    agency = os.path.join (
      *(Path ( descendent ) . parts [:4]) ) )

genealogies_by_agency : Dict [ str,
                               List [ genealogy ] ] = {}
for g in [ genealogy_from_table ( f )
           for f in planta_files ]:
  if not g.agency in genealogies_by_agency.keys ():
    genealogies_by_agency [ g.agency ] = [g]
  else:
    genealogies_by_agency [ g.agency ] = (
      genealogies_by_agency [ g.agency ]
      + [g] )

# Every file with a name suggesting it is the planta file of interest,
# such that the agency that sent it to us
# sent no other files that might be the one we want
# (based also on filename).
agencies_with_a_unique_planta_candidate : List [ str ] = [
  v[0] . descendent
  for v in genealogies_by_agency.values ()
  if len(v) == 1 ]

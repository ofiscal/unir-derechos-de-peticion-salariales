from   dataclasses import dataclass
import os
import pandas as pd
from   pathlib import Path
import re
from   typing import List, Set, Dict


agency_response_folder = "data/input/agency_responses/"

@dataclass
class genealogy:
  """
WHAT A GENEALOGY IS:
This describes the filesystem hierarchy.
In each `genealogy`, the `descendent` will descend from the `agency`.
The `agency` field in every `genealogy`
will be a child of `agency_response_folder`.

WHY I NEED TO USE `GENEALOGY`:
Not every `planta` file is a child (immediate descendent)
of the agency folder it belongs to --some are buried deep.

Pairs would work too, allowing me to avoid defining a class,
but this type is easier for a reader to reason about,
because they can ignore the order of the fields. """
  descendent : str # path to an Excel table in `agency_response_folder`
  agency     : str # child (immediate descendent) of `agency_response_folder`

def basenames_matching_pattern_in_folder (
    pattern : str, # a regex
    path0 : str = ".",
    recursionCount = 0
) -> List [ str ]:
  """Finds all files whose basenames match `pattern` in `path0` ignoring case."""
  # Inspired by
  # https://stackoverflow.com/questions/44805898/recursively-look-for-files-and-or-directories
  acc : List [ str ] = [] # accumulates results
  dirs = os.listdir ( path0 )
  for dir in dirs:
    path1 = os.path.join ( path0, dir)
    if os.path.isdir ( path1 ):
      acc = ( acc +
              basenames_matching_pattern_in_folder ( # recurse
                pattern = pattern,
                path0 = path1 ) )
    if re.search ( pattern, path1, re.IGNORECASE):
      acc.append ( path1 )
  return acc

def genealogy_from_table ( descendent : str
                          ) -> genealogy:
  return genealogy (
    descendent = descendent,
    agency = os.path.join (
      *(Path ( descendent ) . parts [:4]) ) )

def build_genealogies_by_agency (
    paths : List[str]
) -> Dict [ str,
            List [ genealogy ] ]:
  acc : Dict [ str,
               List [ genealogy ] ] = {}
  for g in [ genealogy_from_table ( f )
             for f in paths ]:
    if not g.agency in acc.keys ():
      acc [ g.agency ] = [g]
    else:
      acc [ g.agency ] = (
        acc [ g.agency ]
        + [g] )
  return acc

def unique_planta_candidates () -> List [ str ]:
  """ Every file with a name suggesting it is the planta file of interest,
such that the agency that sent it to us
sent no other files that might be the one we want
(based also on filename)."""
  return [
    v[0] . descendent
    for v in (
        build_genealogies_by_agency (
          basenames_matching_pattern_in_folder ( # returns the planta files
            pattern = # must match both "xlsx" and "xlsm" extensions
            "planta.*\.xls.$",
            path0 = agency_response_folder ) )
        . values() )
    if len(v) == 1 ]

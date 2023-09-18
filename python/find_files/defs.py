from   dataclasses import dataclass
from   glob import glob
import os
import pandas as pd
from   pathlib import Path
import re
from   typing import Dict, List, Set, Tuple


agency_response_folder = "data/input/agency_responses/"
agencies = glob ( # all child folders, i.e. all agencies
    agency_response_folder + "/*/" )

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
    elif re.search ( pattern, path1, re.IGNORECASE):
      acc.append ( path1 )
  return acc

def genealogy_from_path_to_table ( descendent : str
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
  for g in [ genealogy_from_path_to_table ( f )
             for f in paths ]:
    if not g.agency in acc.keys ():
      acc [ g.agency ] = [g]
    else:
      acc [ g.agency ] = (
        acc [ g.agency ]
        + [g] )
  return acc

def planta_candidates_and_ambiguous_agencies () -> Tuple [
    List [ str ],
    List [ str ],
    List [ str ], ]:
  """ Returns three lists of paths:
( planta_candidates,             # files we want to ingest
  multiple_planta_file_agencies, # agencies with >1 file named "planta"
  no_planta_file_agencies        # agencies with no file named "planta

The files in the first list do not correspond to agencies,
but rather to tables located within that agency folder.
A file is in that first list if it includes the word "planta" in its name,
and it is the *only* file in that agency's folder to do so."""
  genealogies = (
    build_genealogies_by_agency (
      basenames_matching_pattern_in_folder ( # returns the planta files
        pattern = # must match .xls, .xlsx and .xlsm extensions
                  # PITFALL: \. will be deprecated soon,
                  # as an invalid escape sequence; \\. is preferred.
                  # See https://stackoverflow.com/a/66666859/916142
        "planta.*\\.xls.*$",
        path0 = agency_response_folder ) ) )
  planta_candidates = [
    v[0] . descendent for v in genealogies . values() if len(v) == 1 ]
  multiple_planta_file_agencies = [
    v[0] . agency     for v in genealogies . values() if len(v) != 1 ]
  no_planta_file_agencies = list (
    {   os.path.normpath ( a ) for a in agencies }
    - { os.path.normpath ( a ) for a in genealogies . keys() } )
  return ( planta_candidates,
           multiple_planta_file_agencies,
           no_planta_file_agencies )

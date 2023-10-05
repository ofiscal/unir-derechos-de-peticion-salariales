from   dataclasses import dataclass
from   glob import glob
import os
import pandas as pd
from   pathlib import Path
import re
from   typing import Dict, GenericAlias, List, Set, Tuple


agency_response_folder = "data/input/agency_responses/"
agencies = glob ( # all child folders, i.e. all agencies
    agency_response_folder + "/*/" )

Agency     : GenericAlias = str # a child (immediate descendent) of
                                # `agency_response_folder`
Descendent : GenericAlias = str # a path from an agency to an Excel file

@dataclass
class Genealogy:
  """
WHAT A `Genealogy` IS:
This describes the filesystem hierarchy.
In each `Genealogy`, the `descendent` will descend from the `agency`.
The `agency` field in every `Genealogy`
will be a child of `agency_response_folder`.

WHY I NEED TO USE `Genealogy`:
Not every `planta` file is a child (immediate descendent)
of the agency folder it belongs to --some are buried deep.

Pairs would work too, allowing me to avoid defining a class,
but this type is easier for a reader to reason about,
because they can ignore the order of the fields. """
  descendent : Descendent
  agency     : Agency

def paths_from_cwd_to_files_with_names_matching_pattern (
    pattern : str, # a regex
    path0 : str = ".",
    recursionCount = 0
) -> List [ str ]:
  """Calling this on (pattern, path0)
returns a list of paths (relative to the current working directory)
to files whose names match `pattern`, ignoring case."""
  # Inspired by
  # https://stackoverflow.com/questions/44805898/recursively-look-for-files-and-or-directories
  acc : List [ str ] = [] # accumulates results
  dirs = os.listdir ( path0 )
  for dir in dirs:
    path1 = os.path.join ( path0, dir)
    if os.path.isdir ( path1 ):
      acc = ( acc +
              paths_from_cwd_to_files_with_names_matching_pattern ( # recurse
                pattern = pattern,
                path0 = path1 ) )
    elif re.search ( pattern, path1, re.IGNORECASE):
      acc.append ( path1 )
  return acc

def paths_from_argument_to_files_with_names_matching_pattern (
    pattern : str, # a regex
    path0 : Agency = ".",
) -> List [ Descendent ]:
  """Calling this on (pattern, path0)
returns a list of paths (relative to `path0`)
to files whose names match `pattern`, ignoring case.

PITFALL: This probably only works if `path0` is within
(and defined relative to) the current working directory.

PITFALL: This is really more general than the aliases
in the type signature suggest,
but I'll only use it for agencies and their descendents.
"""
  return [
    ( path [
        # Strip the first len(path0) characters,
        len ( path0 ) : ]
      . lstrip ("/") ) # Strip leading slash. (This seems clearer
                       # than using `len (path0) + 1` above.)
    for path in paths_from_cwd_to_files_with_names_matching_pattern (
        pattern = pattern,
        path0 = path0 ) ]

def genealogy_from_path_from_agencies_root_to_agency_table (
    path : str # path relative to root of agencies input folder
) -> Genealogy:
  """Unlike a similarly-named and soon to be deleted function, this provides a Genealogy in which the `descendent` path is relative to the `agency`."""
  return Genealogy (
    descendent = os.path.join ( * Path ( path ) . parts [1:] ),
    agency     =                  Path ( path ) . parts [0]
  )

def excel_descendents_by_agency (
    Paths : List [str] # paths relative to the input agency root
) ->    Dict [ Agency, List [ Descendent ] ]:
  acc : Dict [ Agency, List [ Descendent ] ] = {}
  for g in [ genealogy_from_path_from_agencies_root_to_agency_table ( f )
             for f in paths ]:
    if not g.agency in acc.keys ():
      acc [ g.agency ] = [g.descendent]
    else:
      acc [ g.agency ] = (
        acc [ g.agency ]
        + [g.descendent] )
  return acc


#####################
# SOON TO BE REPLACED

# This code uses the earlier idiom, in which each `Genealogy`
# defines the `descendent` relative to the current working directory,
# rather than the `agency`.
#####################

def genealogy_from_path_from_project_root_to_agency_table (
    descendent : str
) -> Genealogy:
  return Genealogy (
    descendent = descendent,
    agency = os.path.join (
      *(Path ( descendent )
        . parts [:4] # PITFALL: This is brittle -- it assumes
                     # all agencies are in `data/input/agency_responses/`.
        ) ) )

def build_genealogies_by_agency (
    paths : List[str]
) -> Dict [ str,
            List [ Genealogy ] ]:
  acc : Dict [ str,
               List [ Genealogy ] ] = {}
  for g in [ genealogy_from_path_from_project_root_to_agency_table ( f )
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
      paths_from_cwd_to_files_with_names_matching_pattern (
        # returns the planta files
        pattern = ( # Name must match "planta" or "1.10".
                    # Extension must match .xls, .xlsx or .xlsm.
                    #
                    # PITFALL: \. might work as well as \\. for now,
                    # but is deprecated. See
                    # https://stackoverflow.com/a/66666859/916142
          "(cargos|n[oó]mina|planta|1\\.10|110).*\\.xls.*$" ),
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

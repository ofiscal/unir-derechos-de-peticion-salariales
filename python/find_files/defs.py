# TODO ? This entire module might be obsolete.
# For why, see the comment above
#   `planta_candidates_and_ambiguous_agencies`

from   dataclasses import dataclass
from   glob import glob
import os
import pandas as pd
from   pathlib import Path
import re
from   typing import Dict, List, Set, Tuple
#
from   python.paths import agency_root
from   python.types import *


agencies : List[str] = glob (
  # Full path to each child of agency_root.
  agency_root + "/*/" )

def agency_names_cleaned (
) -> pd.DataFrame: # One column, "agency"
  """Returns the list of agencies, as implied by the names of the folders under the agency root, after stripping off all initial characters that are not alphabetical."""
  root_length = len ( agency_root . split("/") )
  return (
    pd.DataFrame (
      { "agency" :
        [ re.sub (
            "^[^a-zA-Z]*", # find the longest leading substring with no alphas
            "",            # and delete it
            path . split("/") [root_length] ) # in the first segment of path after the agency root
          for path in agencies ] } )
    . sort_values ("agency") )

# TODO | PITFALL: Why do I have both of the following functions?
#   paths_from_cwd_to_filenames_matching_pattern
#   paths_from_argument_to_filenames_matching_pattern
# They have very different implementations. but they seem to do
# at least almost and maybe exactly the same thing.

def paths_from_cwd_to_filenames_matching_pattern (
    pattern : str       , # a regex
    path0   : str = "." ,
) -> List [ str ]:
  """Calling this on (pattern, path0)
returns a list of paths (relative to the current working directory)
to files with names matching `pattern`, ignoring case."""
  # Inspired by
  # https://stackoverflow.com/questions/44805898/recursively-look-for-files-and-or-directories
  acc : List [ str ] = [] # accumulates results
  dirs = os.listdir ( path0 )
  for dir in dirs:
    path1 = os.path.join ( path0, dir)
    if os.path.isdir ( path1 ):
      acc = ( acc +
              paths_from_cwd_to_filenames_matching_pattern ( # recurse
                pattern = pattern,
                path0 = path1 ) )
    elif re.search ( pattern, path1, re.IGNORECASE):
      acc.append ( path1 )
  return acc

def paths_from_argument_to_filenames_matching_pattern (
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
    for path in paths_from_cwd_to_filenames_matching_pattern (
        pattern = pattern,
        path0 = path0 ) ]

def genealogy_from_path_from_agencies_root_to_agency_table (
    path : str # path relative to root of agencies input folder
) -> Genealogy:
  """Provides a Genealogy in which the `descendent` path
  is relative to the `agency`.
  (There is a similarly-named and soon to be deleted function,
  which IIRC provides an absolute
  (i.e. from the project root) path.)"""
  return Genealogy (
    descendent = os.path.join ( * Path ( path ) . parts [1:] ),
    agency     =                  Path ( path ) . parts [0]
  )

def excel_descendents_by_agency (
    paths : List [str] # paths relative to the input agency root
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
  """ Given the path from the project root ("absolute path") to an agency table, this returns a `Genealogy`."""
  return Genealogy (
    descendent = descendent,
    agency = os.path.join (
      *(Path ( descendent )
        . parts [:4] # PITFALL: Assumes the path to each agency goes
                     # `data/input/agency_responses/<agency>`
                     # (which I believe).
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

# TODO : This is now obsolete, thanks to `python.reconnaissance`.
# It and everything it alone depends on should probably be removed.
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
      paths_from_cwd_to_filenames_matching_pattern (
        # returns the planta files
        pattern = ( # Name must match "planta" or "1.10".
                    # Extension must match .xls, .xlsx or .xlsm.
                    #
                    # PITFALL: \. might work as well as \\. for now,
                    # but is deprecated. See
                    # https://stackoverflow.com/a/66666859/916142
          "(cargos|n[oó]mina|planta|1\\.10|110).*\\.xls.*$" ),
        path0 = agency_root ) ) )
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

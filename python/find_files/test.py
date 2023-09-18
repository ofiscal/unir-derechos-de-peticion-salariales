from python.find_files.defs import *


def test_planta_candidates_and_ambiguous_agencies ():
  ( planta_candidates,             # files we want to ingest
    multiple_planta_file_agencies, # agencies with >1 file named "planta"
    no_planta_file_agencies        # agencies with no file named "planta"
   ) = planta_candidates_and_ambiguous_agencies ()
  assert ( len ( planta_candidates ) +
           len ( multiple_planta_file_agencies ) +
           len ( no_planta_file_agencies ) ==
           len ( agencies ) )

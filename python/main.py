# HOW TO USE THIS:
# The comment "CONFIGURE THIS" identifies a line you might want to change.
#
# PURPOSE:
# Defines three objects:
#   recon_reports : Which agencies have how many well-behaved sheets.
#   successes     : Data sets successfully read.
#   errors        : Data sets that could not be read, and why.

import os
import pandas as pd
import pickle
from   typing import Dict, List, Set, Tuple
#
import  python.collect                 as collect
import  python.exceptions.discoveries  as discoveries
import  python.find_files.defs         as find_files
import  python.join_files as join
import  python.paths                   as paths
import  python.reconnaissance.defs     as recon
from    python.types                   import *


# CONFIGURE THESE
recon_strategy     = Definition_Strategy.Load_from_pickle
successes_strategy = Definition_Strategy.Load_from_pickle


if True: # Define `recon_reports` which states which sheets look friendly.
         # Choose a strategy.
  if recon_strategy == Definition_Strategy.Create: # PITFALL: Slow.
    # Rebuild it.
    # Also save some products it implies.
    recon_reports = recon.denom_cell_reports (
      limit = None, # a limit of None (or 0) means "process everything"
      verbose = True, )

    for k, df in recon_reports.items():
      df.to_csv (
        os.path.join ( "data/output",
                       k + ".csv" ) )

    ( recon_reports
      ["nice_sheets_of_agencies_with_multiple_nice_sheets"]
      [[ "agency",
         "file",
         "sheet", ]]
      . to_excel ( "which-sheet-to-use-for-each-agency.xlsx",
                   index = False ) )

  if recon_strategy == Definition_Strategy.Load_from_pickle:
    # Unpickle (deserialize) a saved image of it.
    with open ( os.path.join ( paths.latest_pickle_path,
                               "recon_reports.pickle", ),
                "rb") as handle:
        recon_reports = pickle . load ( handle )

instructions_for_nice_agencies = list (
  recon_reports["nice_sheets_of_agencies_with_one_nice_sheet"]
  . apply ( lambda row :
            File_Load_Instruction (
              path = os.path.join ( row["agency"],
                                    row["file"], ),
              sheet = row["sheet"],
              denominacion_column = row["denom_column"], ),
            axis = "columns" ) )

load_instructions = (
  # TODO: Here I'm giving precedence to the earlier,
  # manually generated instructions.
  # Try the reverse and see if there are more successes that way.
  [ i for i in instructions_for_nice_agencies
    if not i.path in (
        discoveries.exceptional_instruction_dict
        . keys () ) ]
  + discoveries.exceptional_instruction_list )

if True:
  if successes_strategy == Definition_Strategy.Create: # PITFALL: Slow.
    ( successes, errors
     ) = collect.formatted_responses_and_errors (
       agency_root       = paths.agency_root,
       load_instructions = load_instructions )

  if successes_strategy == Definition_Strategy.Load_from_pickle:
    # Unpickle (deserialize) a saved image of each.
    with open ( os.path.join ( paths.latest_pickle_path,
                               "successes.pickle", ),
                "rb") as handle:
        successes = pickle . load ( handle )
    with open ( os.path.join ( paths.latest_pickle_path,
                               "errors.pickle", ),
                "rb") as handle:
        errors = pickle . load ( handle )

together = join.join_successfully_read_excel_files (
  successes = successes )

for (name, obj) in [
    ( "recon_reports"     , recon_reports),
    ( "load_instructions" , load_instructions ),
    ( "successes"         , successes ),
    ( "errors"            , errors ),
    ( "together"          , together ),
]:
  with open ( name + ".pickle",
              "wb") as handle:
    # PITFALL: Might want to move these into `pickle/x` for some value of `x`.
    pickle.dump ( obj,
                  handle,
                  protocol = pickle.HIGHEST_PROTOCOL )

together.to_excel ( "together.xlsx",
                    index = False )

import os
import pandas as pd
import pickle
from   typing import Dict, List, Set, Tuple
#
import  python.collect                 as collect
import  python.exceptions.discoveries  as discoveries
import  python.find_files.defs         as find_files
import  python.paths                   as paths
import  python.reconnaissance.defs     as recon
from    python.types                   import *


if True: # recon: Determine which sheets look friendly.
         # THIS IS SLOW.
  recon_reports = recon.denom_cell_reports (
    limit = None, # a limit of None (or 0) means "process everything"
    verbose = True, )

  if False: # Maybe instead of that,
            # simply unpickle (deserialize) saved data.

    with open ( "pickles/Wednesday/9df594e7e714518c0763d3e5459f454cec3f408c/recon_reports.pickle",
                "rb") as handle:
        recon_reports = pickle . load ( handle )

  for k, df in recon_reports.items():
    df.to_csv (
      os.path.join ( "data/output",
                     k + ".csv" ) )

instructions_for_nice_agencies = list (
  recon_reports["nice_sheets_of_agencies_with_one_nice_sheet"]
  . apply ( lambda row :
            File_Load_Instruction (
              path = os.path.join ( row["agency"],
                                    row["file"], ),
              sheet = row["sheet"],
              denominacion_column = row["denom_column"], ),
            axis = "columns" ) )

( successes, errors
 ) = collect.formatted_responses_and_errors (
   agency_root = paths.agency_root,
   source_files = (
     # TODO: Here I'm giving precedence to the earlier,
     # manually generated instructions.
     # Try the reverse and see if there are more successes that way.
     [ i for i in instructions_for_nice_agencies
       if not i.path in (
           discoveries.exceptional_instruction_dict
           . keys () ) ]
     + discoveries.exceptional_instruction_list
   ) )

for (name, obj) in [
    ( "successes"     , successes ),
    ( "errors"        , errors ),
    ( "recon_reports" , recon_reports),
]:
  with open( name + ".pickle", "wb") as handle:
    pickle.dump ( obj,
                  handle,
                  protocol = pickle.HIGHEST_PROTOCOL )

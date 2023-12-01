# Interactively inspect `python.main.recon_reports`

import os
import pandas as pd
import pickle
#
import python.paths as paths


if False: # Load (deserialize) data from `python.main`.
          # This lets me skip running `main`.

  with open ( os.path.join ( paths.latest_pickle_path,
                             "recon_reports.pickle", ),
              "rb") as handle:
    recon_reports = pickle . load ( handle )

for k in recon_reports.keys(): print(k)

recon_reports["sheets_of_agencies_with_no_nice_sheet"]             . transpose ()
recon_reports["nice_sheets_of_agencies_with_one_nice_sheet"]       . transpose ()
recon_reports["nice_sheets_of_agencies_with_multiple_nice_sheets"] . transpose ()
recon_reports["sheets_with_multiple_denom_cells"]                  . transpose ()

for k in recon_reports.keys():
  print()
  print(k)
  print( len ( recon_reports [k]
               ["agency"]
               . unique () ) )

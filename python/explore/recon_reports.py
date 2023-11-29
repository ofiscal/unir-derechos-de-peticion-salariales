# Interactively inspect `python.main.recon_reports`

import os
import pandas as pd
import pickle


latest = "pickles/Wednesday/3b4243eeb8ce4144ecb910b7ec4d3ac036da0d03"

if False: # Load (deserialize) data from `python.main`.
          # This lets me skip running `main`.

  with open ( os.path.join ( latest,
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

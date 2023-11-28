# Interactively inspect `python.main.recon_reports`

for k in reports.keys(): print(k)

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

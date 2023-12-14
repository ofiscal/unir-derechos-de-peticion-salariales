import os
import pickle
#
import python.explore.together.defs  as defs
import python.paths                  as paths
from   python.types                  import *
from   python.util                   import *


if True: # Define `together`.
  # CUSTOMIZE THIS
  together_strategy = Definition_Strategy.Load_from_pickle

  if together_strategy == Definition_Strategy.Load_from_pickle:
    # Unpickle (deserialize) a saved image of it.
    with open ( os.path.join ( paths.latest_pickle_path,
                               "together.pickle", ),
                "rb") as handle:
      together = pickle . load ( handle )

if True: # determine which agencies have negative COP values
  together["something negative"] = (
    ( (together ["sueldo basico" ] < 0) |
      (together ["salario"]        < 0) |
      (together ["remuneraciones"] < 0) |
      (together ["contribuciones"] < 0) |
      (together ["prestaciones"]   < 0) |
      (together ["gasto total"]    < 0) )
    . astype ( int ) )

  print ( "\nAgencies with at least one row with a negative COP value:\n",
          ( together
            [ together ["something negative"] > 0 ]
            ["agency"] . unique() ) )

if True: # Identify most of the "nullish" rows.
  df = (
    together [[
      "cargo", "grado", "# cargos",
      'salario', 'remuneraciones', 'contribuciones', 'prestaciones',
      "gasto total" ]]
    . copy()
    . applymap ( nullish ) )
  together["nullish"] = df.all ( axis = "columns" )
    # I'm defining that so it can be inspected if need be.

if True: # Drop some things.
  together = together[ together["nullish"] < 1 ]
  together = together.drop (
    columns = ["nullish","something negative","Excel file"] )

if True:
  print ( "\nRows with missing \"# cargos\":\n",
          together [ together ["# cargos"]
                     . isnull () ] )

if True: # Build, examine synthetic gasto total.
  together = defs.add_synthetic_total (together)

  together["gasto total consistent"] = (
    together . apply (
      lambda row: near ( row["gasto total"],
                         row["gasto total synth"],
                         tolerance_relative = 0.1,
                         tolerance_absolute = 1e4 ),
      axis = "columns" )
    . astype ( int ) )

  inconsistent = together [ together["gasto total consistent"] < 1 ]
  print ( "\n# of inconsistent rows:\n",
          len (inconsistent) )
  print ( "\n# of agencies with inconsistent rows:\n",
          len ( inconsistent ["agency"]
                . unique () ) )
  print ( "\nInconsistent rows:\n",
          inconsistent [[ "agency", "cargo",
                          "gasto total", "gasto total synth" ]] )

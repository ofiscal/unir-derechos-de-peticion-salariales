import os
import pickle
#
import python.paths as paths
from   python.types import *
from   python.util  import *


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

  ( together
    [ together ["something negative"] > 0 ]
    ["agency"] . unique() )

if True: # examine synthetic gasto total
  together = add_synthetic_total (together)

  together["good"] = (
    together . apply (
      lambda row: near ( row["gasto total"],
                         row["gasto total synth"],
                         tolerance_relative = 0.1,
                         tolerance_absolute = 1e4 ),
      axis = "columns" )
    . astype ( int ) )

together [["cargo",
           # "grado",
           "# cargos",
           # "sueldo basico",
           "salario",
           "remuneraciones",
           "contribuciones",
           "prestaciones",
           "gasto total",
           # "Excel file",
           "agency",
           "gasto total synth",
           "good", ]]

import numpy as np
import os
import pandas as pd
import re
from   typing import Dict, List, Set, Tuple
#
from python.find_files import unique_planta_candidates
from python.manipulate_files_defs import *


def format_tutela_response (
    source_file : str
) -> pd.DataFrame:
  return (
    false_rows_to_column_based_on_missing_values (
      source_column_name         = "denominación de cargos:1",
      missing_values_column_name = "grado:2",
      new_column_name            = "empleado kind 2",
      df = false_rows_to_column_using_regex (
        source_column_name = "denominación de cargos:1",
        patterns           = [ "empleado.* p.blico",
                               "trabajador.* oficial.*", ],
        new_column_name    = "empleado kind 1",
        df = assemble_header (
          strip_empty_rows (
            strip_trailing_rows (
              strip_leading_rows (
                pd.read_excel (
                  source_file ) ) ) ) ) ) ) )

def collect_formatted_responses (
    source_files : List [str]
) -> Tuple [ Dict [ str, pd.DataFrame ],
             Dict [ str, Exception    ], ]:
  errors     : Dict [ str, Exception    ] = {}
  successes  : Dict [ str, pd.DataFrame ] = {}
  for f in source_files:
    try:
      df = format_tutela_response ( f )
    except Exception as e:
      errors[f] = e
    else:
      successes[f] = df
  return ( successes, errors )

ps = unique_planta_candidates ()
( successes, errors ) = (
  collect_formatted_responses ( ps ) )

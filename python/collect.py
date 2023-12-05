import pandas as pd
from   typing import Dict, List, Set, Tuple
#
from   python.clean_one_file.defs import format_tutela_response
from   python.types import *


def formatted_responses_and_errors (
    agency_root : str, # The `path` in each element of `load_instructions`
                       # is relative to this folder
    load_instructions : List [ File_Load_Instruction ]
) -> Tuple [ Dict [ str, pd.DataFrame ],
             Dict [ str, Exception    ], ]:
  errors     : Dict [ str, Exception    ] = {}
  successes  : Dict [ str, pd.DataFrame ] = {}
  for i in load_instructions:
    try:
      df = format_tutela_response ( agency_root      = agency_root,
                                    load_instruction = i, )
    except Exception as e:
      errors    [i.path] = e
    else:
      successes [i.path] = df
  return ( successes, errors )

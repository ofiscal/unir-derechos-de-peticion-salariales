import pandas as pd
from   typing import Dict, List, Set, Tuple
#
from   python.clean_one_file.defs import format_tutela_response
from   python.types import *


def formatted_responses_and_errors (
    agency_root : str, # the `path` of each element of `source_files`
                       # is relative to this
    source_files : List [ File_Load_Instruction ]
) -> Tuple [ Dict [ str, pd.DataFrame ],
             Dict [ str, Exception    ], ]:
  errors     : Dict [ str, Exception    ] = {}
  successes  : Dict [ str, pd.DataFrame ] = {}
  for f in source_files:
    try:
      df = format_tutela_response ( agency_root = agency_root,
                                    source_file = f )
    except Exception as e:
      errors    [f.path] = e
    else:
      successes [f.path] = df
  return ( successes, errors )

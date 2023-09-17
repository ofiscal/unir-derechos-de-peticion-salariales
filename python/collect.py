import pandas as pd
from   typing import Dict, List, Set, Tuple
#
from python.clean_one_file.defs import format_tutela_response


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

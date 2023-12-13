# Interactively inspect `python.main.successes`

import numpy as np
import os
import pandas as pd
import pickle
from   typing import *
#
import python.explore.successes.defs as defs
import python.paths as paths
from   python.types import *
from   python.util import str_to_float


successes_strategy = Definition_Strategy.Load_from_pickle

if True: # Define `successes`
  if successes_strategy == Definition_Strategy.Already_defined:
    pass
  elif successes_strategy == Definition_Strategy.Create:
    # PITFALL: SLOW.
    # Run the code that defines `successes`.
    from python.main import successes, file_load_instructions
  elif successes_strategy == Definition_Strategy.Load_from_pickle:
    with open ( os.path.join ( paths.latest_pickle_path,
                               "successes.pickle", ),
                "rb") as handle:
      successes : Dict [ str, pd.DataFrame ] = \
        pickle . load ( handle )
    with open ( os.path.join ( paths.latest_pickle_path,
                               "load_instructions.pickle", ),
                "rb") as handle:
      load_instructions : Dict [ str, pd.DataFrame ] = \
        pickle . load ( handle )

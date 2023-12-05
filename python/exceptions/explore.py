from   typing import Dict, List, Set, Tuple
#
from   python.collect import format_tutela_response
import python.exceptions.discoveries as discoveries
from   python.find_files.defs import (
  planta_candidates_and_ambiguous_agencies,
  agencies )
from   python.types import *


########################################
# Define successes and errors, if needed
# (i.e. run main.py)
########################################

define_successes_and_errors = False

if define_successes_and_errors:
  exec(open("python/main.py").read())

  # inspect some of it
  for i,k in list ( successes.items() ) [:5]:
    print()
    print(i)
    print(k)


##########################################
# Inspect a class of error, or all of them
##########################################

for e in errors.values(): print(e.__repr__())

def error_class ( error_repr : str
                 ) -> Dict [str, BaseException]:
  return { k:v for k,v in errors.items()
           if ( v.__repr__() == error_repr ) }

denominacion_errors : Dict [str, BaseException] = error_class (
  "ValueError(Regex_Unmatched(pattern='denominaci.n'))" )

grado_errors : Dict [str, BaseException] = error_class (
  "ValueError(Column_Absent(pattern='grado:2'))" )

for s in grado_errors.keys(): print(s)


#############################################
# Try reading and formatting individual files
#############################################

good = "data/input/agency_responses/UNIDAD ADMINISTRATIVA ESPECIAL DEL SERVICIO PÚBLICO DE EMPLEO/361300. 1.10. Formularios Planta anteproyecto 2024_UAESPE_Topes.xlsm"
bad = "data/input/agency_responses/Ministerio de Cultura/33-01-01 MINCULTURA Formulario 1.10. Planta anteproyecto 2024.xlsm"

format_tutela_response (
  File_Load_Instruction ( bad ) )

df . iloc [ :, denominacion_column ]

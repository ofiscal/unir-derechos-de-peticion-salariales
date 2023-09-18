# HOW TO USE THIS:
# Run main.py first.

# for e in errors.values(): print(e.__repr__())

def error_class ( error_repr : str
                 ) -> Dict [str, BaseException]:
  return { k:v for k,v in errors.items()
           if ( v.__repr__() == error_repr ) }

denominacion_errors : Dict [str, BaseException] = error_class (
  "ValueError(Regex_Unmatched(pattern='denominaci.n'))" )

grado_errors : Dict [str, BaseException] = error_class (
  "ValueError(Column_Absent(pattern='grado:2'))" )

for s in grado_errors.keys(): print(s)

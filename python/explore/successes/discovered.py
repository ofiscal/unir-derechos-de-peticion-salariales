# How many files were read successfully
len ( names_by_file["file"] . unique() )

# How many unique column names
len ( names_by_file["column"] . unique() )

# An exemplar: The first element of successes.
k0 = list(successes.keys()) [0]
v0 = successes[k0]
c0 = list(v0.columns)

for expr in [
   "denom.*cargo.*:1",                    # Perfect.
   "grado.*",                             # Perfect.
   "no.*cargo.*",                         # 3 misfits
   "salario.*comun.*subtotal.*",          # Perfect.
   ".*remuneraciones.*remun.*subtotal.*", # Perfect
   ".*inherentes.*total.*",               # 1 misfit
   "prestac.*social.*relac.*total.*",     # 1 misfit
   ".*total.*:.*gastos.*:.*personal.*",
   ( ".*" + # TODO -- A lot of spreadsheets seem to have
     # multiple, identical column names that match.
     # Filling forward the last row of the header column
     # should help.
     ".*:.*".join( [ "total.*gastos.*personal"
                     for _ in range(4) ] )
     + ".*" ),
  ]:
  print ()
  summarize_expr_in_column_names (expr)

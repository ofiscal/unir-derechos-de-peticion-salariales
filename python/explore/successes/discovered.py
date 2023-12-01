# How many files were read successfully
len ( names_by_file["file"] . unique() )

# How many unique column names
len ( names_by_file["column"] . unique() )

# An exemplar: The first element of successes.
k0 = list(successes.keys()) [0]
v0 = successes[k0]
c0 = list(v0.columns)

for expr in [
    ( ".*"                                               +
      ".*".join ( [ "denom.*cargo" for _ in range(4) ] ) +
      ".*" )                              , # Perfect.
    "grado[^-]*"                          , # 1 multiple match.
                                            # Taking the last match solves it.
    "no.*cargo.*:3$"                      , # Perfect.
    "salario.*comun.*subtotal.*"          , # Perfect.
    ".*remuneraciones.*remun.*subtotal.*" , # Perfect
    ".*inherentes.*total.*10"             , # Perfect
    "prestac.*social.*relac.*total.*"     , # 1 multiple and 2 not found
    ".*total.*:.*gastos.*:.*personal.*"   , # Many multi-matches. Taking the first match might work, but first see what happens if I drop the first empty column and everything after it that follows a match to "total.*gasto.*personal.*"
]:
  print ()
  summarize_expr_in_column_names (expr)


###############
# Futz around #
###############

expr = ".*total.*:.*gastos.*:.*personal.*"
summarize_expr_in_column_names (expr)

matches_in_spreadsheets_with_multiple_matches ( expr )
matches_in_spreadsheets_with_multiple_matches ( expr )["column"] . unique()
matches_in_spreadsheets_with_multiple_matches ( expr )["file"] . unique()

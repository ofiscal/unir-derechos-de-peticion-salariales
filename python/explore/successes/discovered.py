# In
#   "Superintendencia Financiera/1.10 Formulario Planta Anteproyecto 2024 SUPERFINANCIERA.xlsx"
# there are two `grado` columns, because I fill the first one forward
# into the empty second one.
# It is the second of those that matters.

count_matches_in_spreadsheets_with_multiple_matches ( "grado.*" )

expr = "no.*cargo.*"
count_matches_in_spreadsheets_with_multiple_matches (expr)
matches_in_spreadsheets_with_multiple_matches (
  count_matches_in_spreadsheets_with_multiple_matches (expr),
  expr )

# Excellent: All 121 data sets have exactly 1 of these.
expr = ".*inherentes.*total.*"
find_matches ( expr )
summarize_matches_to_expr ( expr )
count_matches_in_spreadsheets_with_multiple_matches (expr)
matches_in_spreadsheets_with_multiple_matches (
  count_matches_in_spreadsheets_with_multiple_matches (expr),
  expr )

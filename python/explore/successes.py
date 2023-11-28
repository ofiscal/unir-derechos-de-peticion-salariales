# Interactively inspect `python.main.successes`

k0 = list(successes.keys()) [0]
v0 = successes[k0]
c0 = list(v0.columns)

( pd.Series ( [ c
                for v in successes.values()
                for c in v.columns ] )
  . unique () )

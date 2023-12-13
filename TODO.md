# Explore `together : pd.DataFrame`

## Negative values

Which agencies give negative values?
What do those rows look like?

## Do the four subtotals sum to the total?

## The rows where `# cargos == 0`

What do they look like?
Where do they come from?

## Empty rows

What do they look like?
Where do they come from?

# Enable overriding, for specific column-file pairs, the default regex.

to identify that column.

Write a fucntion to merge two `File_Load_Instruction`s.
The first argument takes precedence.
Use this function to merge the automatically-generated instructions
with a manual one, so that the manual one only needs to identify
the regex in question, not specify everything else about the file.

# Determine which problems to solve by hand (changing the data) and which automatically.

See `python/explore/successes/discovered.py`.

# Skip everything in `agencias_with_no_problem_we_can_solve`.

# See if "MINISTERIO DE EDUCACIÓN NACIONAL" looks unreadable because sheets are hidden.

see `python/exceptions/discoveries.py`

# Expand paths consumed.

There are around 170 agencies that responded.
Currently the code identifies 139 planta files to interpret --
namely, the 139 files that include "planta" in the name
and are the *only* descendent of that angency's folder that do so.

Maybe the regular expression used to identify them can be expanded somewhat,
to take in more files.
But that is unlikely to provide a complete solution.
Files which are still not found after doing that
will need to be identified manually.

# Handle the errors.

Some work on this has been done;
see the two files matching the path `python/error_hunting.*`.

`python/main.py` generates not just a dictionary called `successes`
of 118 successesfully interpreted data frames,
but also a dictionary called `errors` of 21 errors.
Each error is associated in that dictionary with the file that generated it.
Those errors need to be chased down.

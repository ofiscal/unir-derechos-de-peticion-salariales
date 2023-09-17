# expand paths consumed

There are around 170 agencies that responded.
Currently the code identifies 139 planta files to interpret --
namely, the 139 files that include "planta" in the name
and are the *only* descendent of that angency's folder that do so.

Maybe the regular expression used to identify them can be expanded somewhat,
to take in more files.
But that is unlikely to provide a complete solution.
Files which are still not found after doing that
will need to be identified manually.

# handle the errors

`python/main.py` generates not just a dictionary called `successes`
of 118 successesfully interpreted data frames,
but also a dictionary called `errors` of 21 errors.
Each error is associated in that dictionary with the file that generated it.
Those errors need to be chased down.

# verify the successes

It cannot be assumed that the successes correspond perfectly
to what we want. This will require comparing them, with human eyeballs,
to the data they come from.
But some statistical / data science finesse
could definitely make that work easier.

# unite the successes

We can't assume that they all speak exactly the same language --
they might vary slightly in column names,
or in the terms they use to identify employee roles,
or various other things.
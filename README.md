# The purpose of this code

This repo is meant to assemble a homogeneous,
navigable database from the 170-ish results of our tutelas presupuestales.


# How to set this code up

Check out the project.
It will populate `data/master/`with the master spreadsheet.
It does not come with the other responses to our tutelas,
due to space constraints, so copy those into `data/input/agency_responses`.


# What it does so far

I recommend running it interactively.
Copy the code from `python/main.py` into the Python repl of your choice,
from the root folder of the project. This will define some objects:

`planta_candidates` is a list of paths to the Excel tables
that the code will attempt to interpret.

`multiple_planta_file_agencies` is a list of (paths to)
agencies with more than one file named "planta".

`no_planta_file_agencies` is a list of (paths to)
agencies with no file named "planta".

`successes` is a dictionary whose keys are values in `planta_candidates`,
and whose values are Pandas data frames.

`errors` is a dictionary whose keys are again paths to tables,
and whose values are the first error raised
while that table was being processed.
Most of these errors are raised by the code itself --
for instance, when a regex it was hoping to find is never matched.
But other errors might be raised by Pandas --
in particular, "Can only use .str accessor with string values!"


# How to understand the code and data

There is no single overview of this repo.
Rather, README documents are scattered around each part of it,
documenting what needs to be understood locally.
The way to learn what's what is to explore those.
The code is well documented internally,
both with traditional comments, and critically,
with type signatures. Those type signatures are important!
If you understand a function's name and type signature,
you'll often not have to read anything else --
neither the comments nor the code within the function's definition.


# What's next

See the document `TODO.md`, next door to this `README.md` file.


# How to test this code

Use mypy and pytest.

Currently, since the only test file is `python/clean_one_file/test.py`,
this is sufficient for `pyest`:
```
PYTHONPATH=.:$PYTHONPATH pytest python/clean_one_file/test.py
```

(Defining the PYTHONPATH to include the current directory
might not be necessary on yor system but it certainly is on mine.)

And since `python/main.py` imports every file except the test file,
this is sufficient for `mypy`:
```
mypy python/main.py
```

As more files are added, these instructions might become stale,
but the basic idea will remain the same:
use mypy and pytest.

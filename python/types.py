from dataclasses import dataclass
from typing_extensions import TypeAlias


Agency     : TypeAlias = str # a child (immediate descendent) of
                             # `agency_response_folder`
Descendent : TypeAlias = str # a path from an agency to an Excel file

@dataclass
class Genealogy:
  """
WHAT A `Genealogy` IS:
This describes the filesystem hierarchy.
In each `Genealogy`, the `descendent` will descend from the `agency`.
The `agency` field in every `Genealogy`
should be a child of `agency_response_folder`.

WHY I NEED TO USE `Genealogy`:
Not every `planta` file is a child (immediate descendent)
of the agency folder it belongs to --some are buried deep.

Pairs would work too, allowing me to avoid defining a class,
but this type is easier to reason about and edit,
because one ignore the order of the fields. """
  descendent : Descendent
  agency     : Agency

@dataclass
class File_Load_Instruction:
  """
  WHAT IT IS:
  A `File_Load_Instruction` explains how to find what is, hopefully,
  the first column of the table of interest.

  WHY IT IS NEEDED:
  For most files, once we know the file's path,
  we can assume that sheet 0 is the sheet of interest
  (Excel files can have many sheets),
  and within that sheet, column 0 encodes the "denominacion" column --
  but there are exceptions. This type can encode those exceptions.
  """
  path                : str     # from root of repo to file
  sheet               : Union[int, str] = 0 # `int` is 0-indexed.
                                            # `str` is a sheet name.
  denominacion_column : int = 0 # 0-indexed


########################
# Errors
########################

# PITFALL: These types can't extend Exception and Enum simultaneously,
# for reasons I don't understand.
# Instead I will return `ValueError`s (which extend `Exception`)
# that *contain* these types. These types are not `Enum`s,
# but collectively they can be thought of as an Enum,
# in the sense that they are
# all the ways I know of for parsing to fail.
@dataclass
class Regex_Unmatched:
  pattern : str

@dataclass
class Column_Absent:
  pattern : str

@dataclass
class Nothing_Missing:
  pass

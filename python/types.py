from   dataclasses import dataclass
from   typing import GenericAlias


Agency     : GenericAlias = str # a child (immediate descendent) of
                                # `agency_response_folder`
Descendent : GenericAlias = str # a path from an agency to an Excel file

@dataclass
class Genealogy:
  """
WHAT A `Genealogy` IS:
This describes the filesystem hierarchy.
In each `Genealogy`, the `descendent` will descend from the `agency`.
The `agency` field in every `Genealogy`
will be a child of `agency_response_folder`.

WHY I NEED TO USE `Genealogy`:
Not every `planta` file is a child (immediate descendent)
of the agency folder it belongs to --some are buried deep.

Pairs would work too, allowing me to avoid defining a class,
but this type is easier for a reader to reason about,
because they can ignore the order of the fields. """
  descendent : Descendent
  agency     : Agency

@dataclass
class File_Load_Instruction:
  """For most files, once we know the file's path,
  we can assume that table sheet 0 is the sheet of interest,
  and within it, column 0 encodes the "denominacion" column --
  but there are exceptions. This type can encode those exceptions.
  """
  path                : str     # from root of repo to file
  sheet               : int = 0 # 0-indexed
  denominacion_column : int = 0 # 0-indexed


########################
# Errors
########################

# PITFALL: This can't extend Exception and Enum simultaneously,
# for reasons I don't understand.
# Instead I will return `ValueError`s
# that *contain* these objects.
@dataclass
class Regex_Unmatched:
  pattern : str

@dataclass
class Column_Absent:
  pattern : str

@dataclass
class Nothing_Missing:
  pass

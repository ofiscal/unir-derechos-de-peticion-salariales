from   dataclasses import dataclass


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

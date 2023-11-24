# PURPOSE:
# This program encodes exceptional data discovered manually.
# These include agencies which provided no planta file,
# agencies which provided multiple candidates,
# and planta files for which the sheet or
# (within that sheet) the denominacion column
# are in an unusual place.

from typing import Dict, List, Set, Tuple
#
from python.types import *


exceptional_instruction_list : List [ File_Load_Instruction ] = [
  File_Load_Instruction (
    path = "MINISTERIO DE SALUD Y PROTECCION SOCIAL/190101. formato 4 y 4a 117123-.xls" ),
  File_Load_Instruction (
    path = "150800 - Defensa Civil/Defensa Civil/1.09 Formularios Anteproyecto 2024 DCC v1.xlsx",
    sheet = 4 ),
  File_Load_Instruction (
    path = "DPS/1.10. Formularios planta anteproyecto 2024 DPS.xlsm",
    sheet = 1 ),
  File_Load_Instruction (
    path = "RNEC/1.10 Formularios planta anteproyecto 2024 RNEC.xlsx",
    sheet = 1 ),
  File_Load_Instruction (
    path = "211200 ANM/1.10/Formulario planta anteproyecto 2024.xlsx",
    sheet = 2 ),
  File_Load_Instruction (
    path = "323100 CAM/1.10/1.10. Formularios Planta anteproyecto 2024.cleaned.xlsm.xlsx",
    sheet = 1 ),
  File_Load_Instruction (
    path = "ESAP/05-03-00 ESAP Formulario 1.10. Planta anteproyecto 2024.xlsm",
    sheet = 1 ),
  File_Load_Instruction (
    path = "COLOMBIA COMPRA EFICIENTE/1.10/1.10 Formularios Planta Anteproyecto 2024.cleaned.xlsm.xlsx",
    sheet = 2 ),
  File_Load_Instruction (
    path = "Unidad de Gestión Pensional y Parafiscales/1.10. Formularios Planta anteproyecto 2024.UGPP.xlsx",
    sheet = 2 ),
  File_Load_Instruction (
    path = "160101 - Policía Gestión General/1.10  FOMULARIO 4 - 4A PLANTA - 160101 - 2024.xlsx",
    denominacion_column = 1 ),
  File_Load_Instruction (
    path = "DEPARTAMENTO NACIONAL DE PLANEACION/1.10/Formularios Planta anteproyecto DNP 2024 F.cleaned.xlsm.xlsx",
    denominacion_column = 1 ),
]

exceptional_instruction_dict : Dict [ str, File_Load_Instruction ] = {
  # This spends a little bit of space redundantly (on the keys),
  # to make it easy to find the instruction for a given path.
  v . path : v
  for v in exceptional_instruction_list }

agencies_with_incomplete_planta_file = [
  "INCI",
  "Ministerio de Cultura",
]

agencies_with_no_planta_file = [
  "FONDO ROTATORIO DEL DANE",
  "FUTIC",
  "2904 FEAB",
  "Instituto Nacional de Formación Técnica Profesional San Andrés y Providencia",
  "FRR",
]

agencies_with_multiple_planta_files = [
 '121100 USPEC',
 '150113 - DIVRI',
 '321100 CORPOCALDAS',
 '210900 Unidad de Planeacion Minero Energètica - UPME',
 '110400 - Migración Colombia',
 'Dirección de Sustitución de Cultivos Ilícitos',
 '170101 Ministerio de Agricultura y Desarrollo Rural',
 '170106 UNIDAD DE PLANEACION RURAL',
 '151600 - Supervigilancia',
 '150105 - Fuerza Aérea',
 'Unidad de información y Análisis Financiero',
 'SUPERINTENDENCIA DE SERVICIOS PÚBLICOS DOMICILIARIOS',
 'AGENCIA DE RENOVACION DEL TERRITORIO',
 '210113 CREG',
 '151100 - Caja de Retiro de la Policia Nacional',
 '211000 IPSE',
 '110101- MINISTERIO DE RELACIONES EXTERIORES',
 '150112 - Dimar',
 '120400 SUPERNOTARIADO',
 '420101 - DNI',
 'DPS',
 '321000 CORPOURABA',
 '151201 -  FONPOLICÍA',
 '170200  Instituto Colombiano Agropecuario -ICA',
  '211100 ANH',
]

folders_to_ignore_because_empty = [
  "DP Maria del Mar Pizarro",
  "171600  Unidad Administrativa Especial de la Gestión de Restitución-",
]

agencies_with_unreadable_planta_file = [
  # This is very strange -- on reading this file,
  # Pandas shows something different from what Excel or Google Sheets show.
  "MINISTERIO DE EDUCACIÓN NACIONAL",
]

agencias_with_no_problem_we_can_solve = (
  agencies_with_incomplete_planta_file +
  agencies_with_no_planta_file         +
  agencies_with_multiple_planta_files  +
  agencies_with_unreadable_planta_file
)

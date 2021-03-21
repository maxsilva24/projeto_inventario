# from io import BytesIO

# import openpyxl

# xlsx_book = openpyxl.load_workbook(BytesIO(arq), read_only=True)

# dataset_tab = tablib.Dataset()


import tablib
import os
from max_sis_if.resources import ItemInventarioResource
from max_sis_if.models import ItemInventario
from io import BytesIO
import openpyxl
# from tqdm import tqdm
end_arquivo = os.path.join(os.getcwd(),'arquivos_tmp','2021_planilha_inventario_final_Macro2.xlsm')   
# end_arquivo = os.path.join(os.getcwd(),'arquivos_tmp','2021_planilha_inventario_teste_Macro.xlsm')   
# end_arquivo = os.path.join(os.getcwd(),'arquivos_tmp','2021_planilha_inventario_Max_final_2.xlsx')   
# end_arquivo = os.path.join(os.getcwd(),'arquivos_tmp','2021_planilha_inventario_curta.xlsx')   
arq = open(end_arquivo, 'rb').read()
xlsx_book = openpyxl.load_workbook(BytesIO(arq), read_only=True, data_only=True)
dataset_tab = tablib.Dataset()
# dataset_tab.xlsx = open(end_arquivo, 'rb').read()
sheet = xlsx_book.active

# obtain generator
rows = sheet.rows
dataset_tab.headers = [cell.value for cell in next(rows)]

for row in rows:
    row_values = [cell.value for cell in row]
    dataset_tab.append(row_values)
    
# print(dataset_tab)
# print(dataset_tab.headers)
# inteRec = ItemInventarioResource()
result = ItemInventarioResource().import_data(dataset_tab, dry_run=False, raise_errors=True )
# tqdm( ItemInventarioResource().import_data(dataset_tab, dry_run=True ))
print(result.has_errors())
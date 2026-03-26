import xlrd
from openpyxl import Workbook

def convert_xls_to_xlsx(xls_file_path, xlsx_file_path):
    # Open the XLS file
    xls_workbook = xlrd.open_workbook(xls_file_path)
    xls_sheet = xls_workbook.sheet_by_index(0)

    # Create a new XLSX workbook and sheet
    xlsx_workbook = Workbook()
    xlsx_sheet = xlsx_workbook.active

    # Copy data from XLS to XLSX
    for row in range(xls_sheet.nrows):
        for col in range(xls_sheet.ncols):
            xlsx_sheet.cell(row=row+1, column=col+1).value = xls_sheet.cell_value(row, col)

    # Save the XLSX file
    xlsx_workbook.save(xlsx_file_path)

# Example usage
convert_xls_to_xlsx('input.xls', 'output.xlsx')
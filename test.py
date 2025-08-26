import gspread

gc = gspread.service_account(filename="service_account.json")
sh = gc.open("OHPS Server DB")

print(sh.worksheet("타법").col_values(1))

def sheet_read(sheet, cell):
    sh = gc.open("OHPS Server DB").worksheet(sheet)
    return sh.get(cell)

def sheet_write(sheet, cell, text):
    sh = gc.open("OHPS Server DB").worksheet(sheet)
    sh.update_acell(cell, text)

while True:
    comnd = input("read or write >> ")
    if comnd == "read":
        print(sh.worksheets())
        a = input("which sheet >> ")
        print(sh.worksheet(a).get_all_values())
        b = input("which cell >> ")
        print(sheet_read(a, b))
    elif comnd == "write":
        print(sh.worksheets())
        a = input("which sheet >> ")
        print(sh.worksheet(a).get_all_values())
        b = input("which cell >> ")
        c = input("thing to write >> ")
        sheet_write(a, b, c)
        print(sh.worksheet(a).get_all_values())
import gspread

account = gspread.service_account()

# Quest 시트
file = account.open("OHPS Server DB")
sheet = file.worksheet('퀘스트ㅣQuest')

i = 17
while i+79 < sheet.row_count:
    pos1 = 'A' + str(i) + ':H' + str(i+7)
    pos2 = 'A' + str(i+80) + ':H' + str(i+87)
    pos3 = 'A' + str(i + 80) + ':H' + str(i + 80)
    pos4 = 'A' + str(i + 87) + ':H' + str(i + 87)
    sheet.copy_range(pos1, pos2, "PASTE_FORMAT")
    sheet.format(pos3, {"borders": {"top": {"style": "DOUBLE", "color": {"red": 0, "green": 0, "blue": 0}}}})
    i += 8
    sheet.format(pos4, {"borders": {"bottom": {"style": "SOLID_THICK", "color": {"red": 0, "green": 0, "blue": 0}}}})
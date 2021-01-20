#non-included libraries
import openpyxl #excel outputs

import db_inter

def json_dump(db,filename): #json text dump
    dump = open(filename+'.txt', 'w')
    dump.write(str(db.dump()))
    dump.close()

def excel_dump(db,filename): #excel spreadsheet dump
    doc = openpyxl.Workbook() 
    sheet = doc['Sheet']
    sheet.title = 'Bulwark Output'
    net_src = db_inter.db_spreadsheet_format(db)
    nets = list(net_src.keys())
    sets = list(net_src.values())
    if len(nets) == 1:
        excel_set_format(sheet,nets[0],sets[0])
    elif len(nets) > 1:
        for each in nets:
            tempsheet = doc.create_sheet(each[0])
            tempsheet.title = each[0]
            excel_set_format(tempsheet,each[0],net_src[each])

        doc.remove_sheet(sheet)
    
    doc.save(filename+'.xlsx')

        

def excel_set_format(sheet,net,single): #formats a subnet for the single sheet
    sheet.title = net
    sheet['A1'] = "IP"
    sheet['B1'] = "Hostname(s)"
    sheet['C1'] = "Open Ports"

    count = 0
    while count < len(single):
        sheet['A'+str(count+2)] = single[count][0]
        sheet['B'+str(count+2)] = single[count][1]
        sheet['C'+str(count+2)] = single[count][3]
        count+=1
    

#non-included libraries
import sys #literally just for exiting
import PyInquirer #the cli
from PyInquirer import prompt, Separator #more cli stuff

import scan
import db_inter
import output

class bulwark: #class for the database system. makes things easier here
    def __init__(self, filename):
        self.filename= filename

    def db_init(self): #start the db
        db_inter.db_start(self)

    def db_clear(self): #clears the db
        db_inter.db_clear(self)

    def insert(self,source): #inserts data into the db
        parsed_data = scan.scan_file(source)
        db_inter.db_insert(parsed_data,self)

    def export(self,formats): #handles many export formats
        filename = ''
        if 'JSON (FILE)' in formats:
            if filename == '':
                filename = file_location('Enter the name of the file(s) to be written to. (No extension)')
            output.json_dump(self,filename)
        if 'EXCEL SPREADSHEET' in formats:
            if filename == '':
                filename = file_location('Enter the name of the file(s) to be written to. (No extension)')
                output.excel_dump(self,filename)
        if 'JSON (CLI)' in formats:
            print(db_inter.db_export(self))
            input("Press Enter to continue...")

    def dump(self): #dumps data
        return db_inter.db_export(self)


#default db as a global for passing around
default_db = None


# this block was the old cli. just here in case
'''
if "--h" in sys.argv: #checks for stuff during startup. options listed here
    response = """bulwark is a cybersecurity collaboration tool developed by Sean "Bradley" Manly for the UB NetDef Club and personal use. 

    Options:
        --c > Create a new table (use for first time startup and for clearing the targets)

        --h > Display help
        
        --s > Scan XML and output (--s scan.xml)
        
        --i > Insert XML scan into the database (--i scan.xml)"""
    print(response)
    sys.exit()
if "--c" in sys.argv:
    db_inter.db_start()
    print('NEW DATABASE STARTED')
if "--s" in sys.argv:
    name_loc = sys.argv.index("--s")+1
    print(scan.scan_file(sys.argv[name_loc]))
if "--i" in sys.argv:
    name_loc = sys.argv.index("--i")+1
    parsed_data = scan.scan_file(sys.argv[name_loc])
    db_inter.db_insert(parsed_data)
'''

def about(): #info
    print('\n\nWelcome to Bulwark, an nmap scan aggregation tool.\nThis tool was developed by Sean "Brad" Manly.')
    interaction()

def interaction(): #the main interaction loop
    if default_db == None:
        print("NO DATABASE SELECTED")
    else:
        print("CURRENT DATABASE: " + default_db.filename)
    print("What would you like to do?\n")
    interact_question = {
        'type':'list',
        'name':'action',
        'message':'Choose an option below.',
        'choices': ['New Database','Clear Database','Change Database',"Parse Scan","Insert Scan",'Export Data',"Exit Bulwark"]}

    answer = prompt(interact_question)

    bulwark_go(answer['action'])

def bulwark_go(action): #executes the ineraction's outcome
    global default_db

    #JUST A BUNCH OF DIFFERENT OPTIONS
    if action == 'New Database':
        print('This database will be set as default upon creation')
        question = {
            'type':'input',
            'name':'db_name',
            'message':'Enter the database name (exclude the .db):',
            'default':'bulwark'
        }
        new_db = bulwark(prompt(question)['db_name'])
        new_db.db_init()
        default_db = new_db
    elif action == 'Parse Scan':
        name_loc = file_location('Enter the location of the scan (.xml)')
        print(scan.scan_file(name_loc))
    elif action == 'Insert Scan':
        name_loc = file_location('Enter the location of the scan (.xml)')
        default_db.insert(name_loc)
    elif action == "Clear Database":
        default_db.db_clear()
    elif action == "Exit Bulwark":
        print("\nGoodbye!\n\n")
        sys.exit()
    elif action == "Change Database":
        question = {
            'type':'input',
            'name':'change_db',
            'message':'Enter the database name (exclude the .db):',
            'default':'bulwark'
        }
        change_db = bulwark(prompt(question)['change_db'])
        default_db = change_db
    elif action == "Export Data":
        question = {
            'type':'checkbox',
            'name':'export_type',
            'message':'What format(s) would you like to export to?',
            'choices':[
                Separator('= CLI ='),
                {'name':'JSON (CLI)'},
                {'name':'JSON (FILE)'},
                Separator('= GUI = '),
                {'name':'EXCEL SPREADSHEET'}
            ]
        }
        default_db.export(prompt(question)['export_type'])

    interaction()

def file_location(langprompt): #sets up a system to easily do questions for file locations
    question = {
        'type':'input',
        'name':'file_loc',
        'message':langprompt,
        'default':'none'
    }
    answer = prompt(question)
    return answer['file_loc']

about() #this runs the whole thing
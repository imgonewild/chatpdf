import tkinter as tk #import model A as alias B
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from chatpdf_api import *
from dotenv import load_dotenv
#from model A import function/class/vairable

#root = Python GUI
root = tk.Tk()
root.title('Inteplast SDS Tool')
root.resizable(False, False)
root.geometry('600x350')

load_dotenv() #make you able to use os.getenv() and os.environ to load .env file
X_API_KEY = os.getenv('X_API_KEY')

def load_pdf():
    var_pdf_select.set('Select SDS') #set select option

    pdf_select['menu'].delete(0, 'end')

    readfile = open('.env', "r")
    for line in readfile:
        line = line.replace(' ','')
        split = line.split("=")
        key = split[0]
        if(key!='X_API_KEY' and key[0]!='#'):
            pdf_select['menu'].add_command(label=key, command=tk._setit(var_pdf_select, key))

def select_files(): #browse select file dialog
    filetypes = (        
        ('PDF files', '*.pdf'),
        ('All files', '*.*')
    )

    file = fd.askopenfilename(
        title='Open files',
        initialdir='/',
        filetypes=filetypes)
    
    call_api(file)
  
def call_api(method):
    pdf = var_pdf_select.get()        

    if method == "ask_question" and pdf == 'Select SDS':
        messagebox.showinfo("Alert", "Please select a SDS.")
        return
    
    elif method == "ask_question" and pdf != 'Select SDS':
        source_id = os.getenv(pdf)
        question = entry_value.get()
        ans = api_ask_question(source_id, question)
        messagebox.showinfo("Answer", ans)

    elif method != '':  #upload file
        messagebox.showinfo("Info", api_upload_file(method))  
        load_pdf()      

# Add an optional Label widget
Label(root, text= "Inteplast SDS system", font= ('Aerial 17 bold italic')).pack(pady= 30)

pdf_choices = ('1') #It should use at least one option or it'd show error
var_pdf_select = tk.StringVar(root)
pdf_select = tk.OptionMenu(root, var_pdf_select, pdf_choices)
pdf_select.pack()

load_pdf()

# Label Creation
lbl = tk.Label(root, text = f"Question:").pack()

entry_value = StringVar(root, value="What is the firs aid measures of eye contact?")
entry=Entry(root, textvariable=entry_value, width=50).pack(padx=10, pady=10)
  
printButton = ttk.Button(root,
                        text = "Ask", 
                        command = lambda: call_api('ask_question')                        
                        ).pack(pady= 10)

browser_pdf_btn = ttk.Button(
    root,
    text='Upload SDS PDF Files',
    command=select_files,
    width=30
).pack()

root.mainloop()
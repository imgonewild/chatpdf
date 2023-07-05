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

def load_pdf(): #load .env file then select option data
    var_sds_select.set('Select SDS')
    sds_option_menu['menu'].delete(0, 'end')
    readfile = open('.env', "r")

    for line in readfile:
        split = line.replace(' ','').split("=")
        key = split[0]
        if(key!='X_API_KEY' and key[0]!='#'):
            sds_option_menu['menu'].add_command(label=key, command=tk._setit(var_sds_select, key))

def select_files(): #browse select file dialog
    filetypes = (        
        ('pdf file', '*.pdf'),
        ('All file', '*.*')
    )

    file = fd.askopenfilename(
        title='Open file',
        initialdir='/',
        filetypes=filetypes)
    
    call_api('upload_file',file)
  
def call_api(method, content):
    selected_sds = var_sds_select.get()        

    if method == "ask_question" and selected_sds == 'Select SDS':
        messagebox.showinfo("Alert", "Please select a SDS.")
        return
    
    elif method == "ask_question" and selected_sds != 'Select SDS':
        source_id = os.getenv(selected_sds)
        ans = api_ask_question(source_id, content)
        messagebox.showinfo("Answer", ans)

    elif method == 'upload_file':  #upload file
        messagebox.showinfo("Info", api_upload_file(content))  
        load_pdf()      

# Add an optional Label widget
Label(root, text= "Inteplast SDS system", font= ('Aerial 17 bold italic')).pack(pady= 30)

# Add select option widget
sds_options = ('1') #It should use at least one option or it'd show error
var_sds_select = tk.StringVar(root)
sds_option_menu = tk.OptionMenu(root, var_sds_select, sds_options)
sds_option_menu.pack()

load_pdf()

# Add label 
tk.Label(root, text = f"Question:").pack()

# Add entry Creation aka input textarea
entry_value = StringVar(root, value="What is the firs aid measures of eye contact?")
entry = Entry(root, textvariable=entry_value, width=50).pack(padx=10, pady=10)
  
ttk.Button(
    root,
    text = "Ask", 
    command = lambda: call_api('ask_question', entry_value.get())                        
).pack(pady= 10)

ttk.Button(
    root,
    text='Upload SDS selected_sds Files',
    command=select_files,
    width=30
).pack()

root.mainloop()
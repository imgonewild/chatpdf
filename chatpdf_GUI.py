import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from chatpdf_api import *
from dotenv import load_dotenv

root = tk.Tk()
root.title('Inteplast SDS Tool')
root.resizable(False, False)
root.geometry('600x350')

load_dotenv()
X_API_KEY = os.getenv('X_API_KEY')

def load_pdf():
    var_pdf_select.set('Select SDS')

    pdf_select['menu'].delete(0, 'end')

    readfile = open('.env', "r")
    for line in readfile:
        line = line.replace(' ','')
        split = line.split("=")
        key = split[0]
        if(key!='X_API_KEY' and key[0]!='#'):
            pdf_select['menu'].add_command(label=key, command=tk._setit(var_pdf_select, key))

def select_files():
    filetypes = (        
        ('PDF files', '*.pdf'),
        ('All files', '*.*')
    )

    file = fd.askopenfilename(
        title='Open files',
        initialdir='/',
        filetypes=filetypes)

    # showinfo(
    #     title='Selected Files',
    #     message=file
    # )
    call_api(file)
  
def call_api(method):
    pdf = var_pdf_select.get()        

    if method == "ask_question" and pdf == 'Select SDS':
        messagebox.showinfo("Alert", "Please select a SDS.")
        return
    elif method == "ask_question" and pdf != 'Select SDS':
        print("var_pdf_select.get()", pdf)

        source_id = os.getenv(pdf)
        
        question = entry_value.get()
        ans = api_ask_question(source_id, question)
        print("source_id", source_id)

        messagebox.showinfo("Answer", ans)
    elif method != '':  #upload file
        messagebox.showinfo("Info", api_upload_file(method))  
        load_pdf()      

# def btn_question_click(event):
#     print("clicked!")
#     entry.delete(0,END)

def callback(*args):
    print(var_pdf_select.get())

# Add an optional Label widget
Label(root, text= "Inteplast SDS system", font= ('Aerial 17 bold italic')).pack(pady= 30)

pdf_choices = ('1')
var_pdf_select = tk.StringVar(root)
pdf_select = tk.OptionMenu(root, var_pdf_select, *pdf_choices)
var_pdf_select.trace("w", callback)
pdf_select.pack()

# tk.Button(root, text='Reload SDS', command=load_pdf).pack()
load_pdf()

# Label Creation
lbl = tk.Label(root, text = f"Question:")
lbl.pack()

entry_value = StringVar(root, value="What is the firs aid measures of eye contact?")

entry=Entry(root, textvariable=entry_value, width=50)
entry.pack(padx=10, pady=10)
# entry.bind("<1>", btn_question_click)
  
printButton = ttk.Button(root,
                        text = "Ask", 
                        command = lambda: call_api('ask_question')                        
                        ).pack(pady= 10)

# label_ans_var = StringVar(root, value="Answer: ")
# Label(root, textvariable = label_ans_var,  width=60).pack()

browser_pdf_btn = ttk.Button(
    root,
    text='Upload SDS PDF Files',
    command=select_files,
    width=30
).pack()

root.mainloop()
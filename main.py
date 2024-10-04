from customtkinter import set_appearance_mode, CTk, CTkButton, CTkTextbox, CTkImage, filedialog, CTkLabel
from PIL import ImageTk, Image
from tkinter import PhotoImage, Label
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import shutil
from init_database import init
from query import query_rag
import threading

#context = ""

prompt_template = """
Do the following instruction

Here is the conversation history as a reference: {context}

Question: {question}

Answer: 
"""


model = OllamaLLM(model='llama3')
prompt = ChatPromptTemplate.from_template(prompt_template)
chain = prompt | model



#App
root = CTk()

#Title
root.title("OLLAMA AI APP")

#Size
root.minsize(600,700)


root.iconbitmap('icon.ico')

#Appearance
set_appearance_mode("dark")

#Button Size
button_size = 15

#Icon
icon = Image.open('send.png')
icon = icon.resize((25,25))

attach_icon = Image.open('attach.png')
attach_icon = attach_icon.resize((25,25))

loading_icon = Image.open('square.png')
loading_icon = loading_icon.resize((25,25))


#Textbox Response
textbox_chat = CTkTextbox(root, width=500, height=400,
                          state = 'normal' , font=('Helvetica', 12), wrap='word')

textbox_chat.place(relx = 0.5, rely = 0.35, anchor='center')
textbox_chat.insert('end', "OLLAMA: Hello, I am OLLAMA, an AI chatbot. How can I help you today?\n")
textbox_chat.configure(state='disabled')


def send_prompt():
    def worker():
        user_prompt = textbox_entry.get(0.0, 'end')
        textbox_entry.delete(0.0, 'end')
        init()
        result,_ = query_rag(user_prompt)
        textbox_chat.configure(state='normal')
        textbox_chat.insert('end', "\nUser: " + user_prompt +'\n')
        textbox_chat.insert('end', "OLLAMA: " + result +'\n')
        textbox_chat.configure(state='disabled')
        loading_button.place_forget()
        
        
    loading_button.place(in_=textbox_entry, x=button_x,y=button_y,)
    loading_button.configure(state='disabled')
    threading.Thread(target=worker).start()

def attach_file():
    def worker():
        root.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("pdf files", "*.pdf"),))
        if root.filename == "":
            return root.filename
        shutil.copy(root.filename, 'data')
        init()
        result, _ = query_rag("Summarize the text")
        textbox_chat.configure(state='normal')
        textbox_chat.insert('end', "OLLAMA: " + result +'\n')
        textbox_chat.configure(state='disabled')
        loading_button.place_forget()
        
 
    loading_button.place(in_=textbox_entry, x=button_x,y=button_y - 40)
    loading_button.configure(state='disabled')
    threading.Thread(target=worker).start()

#Textbox Entry
textbox_entry = CTkTextbox(root, width=500, height=80, font=('Helvetica', 12),border_spacing=25, border_color='gray', wrap='word')
textbox_entry.place(relx = 0.5, rely = 0.75, anchor='center')


#Button Configuration
send_button = CTkButton(root, text="", corner_radius=button_size//2, height = button_size, width=2, 
                        image=CTkImage(dark_image=icon, light_image=icon), fg_color='light blue',command=send_prompt)

attach_button = CTkButton(root, text="", corner_radius=button_size//2, height = button_size, width=2, 
                        image=CTkImage(dark_image=attach_icon, light_image=attach_icon), fg_color='light blue',command=attach_file)

loading_button = CTkButton(root, text="", corner_radius=button_size//2, height = button_size, width=2, 
                        image=CTkImage(dark_image=loading_icon, light_image=loading_icon), fg_color='light blue')
#Button Size
button_x = textbox_entry.winfo_width() - button_size - 10 + 500
button_y = (textbox_entry.winfo_height() - button_size) //2 +50



#Place Button inside Textbox entry
send_button.place(in_=textbox_entry, x=button_x,y=button_y)

attach_button.place(in_=textbox_entry, x=button_x,y=button_y - 40)


root.mainloop()
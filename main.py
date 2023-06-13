from tkinter import *
from tkinter import filedialog as fd
from tkinter import Canvas
from pdfreader import Viewer
from audio_book import Speak
from pdf2docx import Converter
from tkinter import ttk
from tkinter.messagebox import showerror
from PyDictionary import PyDictionary

import os


class Reader:

    # Setting up the Reader
    def __init__(self, window):
        self.win = window
        self.win.title("Advance PDF Reader")
        self.win.geometry('700x700+400+0')
        self.win.state(newstate='zoomed')
        self.win.iconbitmap(self.win, 'icons/logo.png')

        # Setting Variables for to Read PDF
        # path for the pdf doc
        self.path = None
        # state of the pdf doc, open or closed
        self.isFileOpen = None
        # author of the pdf doc
        self.author = None
        # name for the pdf doc
        self.name = None
        # the current page for the pdf
        self.current_page = 0
        # total number of pages for the pdf doc
        self.numPages = None
        # Pages
        self.img = None
        # reader
        self.reader = None
        self.doc = []
        self.speaker = None

        # Creating Menu
        self.menu = Menu(self.win)
        self.win.config(menu=self.menu)

        # Adding File Menu
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu, underline=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Exit")

        # Adding Edit Menu
        self.edit_menu = Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu, underline=0)
        self.edit_menu.add_command(label="Copy")
        self.edit_menu.add_command(label="Cut")
        self.edit_menu.add_command(label="Paste")

        # Adding View Menu
        self.view_menu = Menu(self.menu)
        self.menu.add_cascade(label="View", menu=self.view_menu, underline=0)

        # Adding Help Menu
        self.help_menu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.help_menu, underline=0)

        # Creating Frames for Index, Content, tools
        self.top_frame = Frame(self.win)
        self.ind_frame = Frame(self.win, bg='white', height=650)
        self.cont_frame = Frame(self.win, bg='#ECE8F3', height=650)
        self.top_frame.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.05, height=50)
        self.ind_frame.place(relx=0.0, rely=0.05, relwidth=0.3)
        self.cont_frame.place(relx=0.3, rely=0.05, relwidth=0.7)

        # Setting Content In cont_frame
        self.content = Canvas(self.cont_frame, bg="#ECE8F3", highlightbackground="#ECE8F3", highlightthickness=1)
        self.ver_scroll = Scrollbar(self.cont_frame, orient='vertical')
        self.hor_scroll = Scrollbar(self.cont_frame, orient='horizontal')
        self.content.config(yscrollcommand=self.ver_scroll.set, xscrollcommand=self.hor_scroll.set)
        self.ver_scroll.configure(command=self.content.yview)
        self.hor_scroll.configure(command=self.content.xview)
        self.content.place(relx=0.0, rely=0.0, relwidth=0.97, relheight=0.97)
        self.ver_scroll.place(relx=0.97, rely=0.0, relheight=0.97, relwidth=0.03)
        self.hor_scroll.place(relx=0.0, rely=0.97, relwidth=1)
        self.content.update()
        print(self.content.winfo_width())

        # Adding Icons to Top Frame
        # Importing Logos
        self.home_logo = PhotoImage(file='icons/house-solid.png').subsample(30, 30)
        self.up_logo = PhotoImage(file='icons/caret-up-solid.png').subsample(30, 30)
        self.down_logo = PhotoImage(file='icons/caret-down-solid.png').subsample(30, 30)
        self.zoom_in_logo = PhotoImage(file='icons/plus-solid.png').subsample(30, 30)
        self.zoom_out_logo = PhotoImage(file='icons/minus-solid.png').subsample(30, 30)
        self.export_logo = PhotoImage(file='icons/file-export-solid.png').subsample(30, 30)
        self.print_logo = PhotoImage(file='icons/print-solid.png').subsample(30, 30)
        self.speaker_logo = PhotoImage(file='icons/volume-high-solid.png').subsample(30, 30)

        # Creating frames for icons
        self.icons_frame = Frame(self.top_frame)
        self.icons_frame.pack(anchor='center')

        # Read icons frame
        self.read_icon_frame = Frame(self.icons_frame)

        # Creating Buttons
        self.home_btn = Button(self.icons_frame, text='Home', command=self.go_to_home)
        self.zoom_in_btn = Button(self.icons_frame, text='Zoom In')
        self.zoom = Entry(self.icons_frame)
        self.zoom_out_btn = Button(self.icons_frame, text='Zoom Out')
        self.up_btn = Button(self.icons_frame, text='Up', command=self.previous_page)
        self.pageNo = Entry(self.icons_frame)
        self.total_pages = Label(self.icons_frame, text='/ Pages')
        self.down_btn = Button(self.icons_frame, text='Down', command=self.next_page)
        self.speak_btn = Button(self.read_icon_frame, text="Speak",command=self.read)
        self.pause_btn = Button(self.read_icon_frame, text='Pause', command=self.pause_or_resume)
        # self.resume_btn = Button(self.read_icon_frame, text='Resume', command=self.resum)
        self.stop_btn = Button(self.read_icon_frame, text='Stop', command=self.stop)

        self.export_btn = Button(self.icons_frame, text='Convert', command=self.convert_word)
        self.print_btn = Button(self.icons_frame, text='Print')

        self.home_btn.config(image=self.home_logo, height=30, width=40, bd=0)
        self.home_btn.grid(row=0, column=0, padx=10)

        self.zoom_out_btn.config(image=self.zoom_out_logo, height=30, width=40, bd=0)
        self.zoom_out_btn.grid(row=0, column=1, padx=10)

        self.zoom.configure(width=5, font=('Airal', 12), bd=0)
        self.zoom.grid(row=0, column=2, padx=10)

        self.zoom_in_btn.config(image=self.zoom_in_logo, height=30, width=40, bd=0)
        self.zoom_in_btn.grid(row=0, column=3, padx=10)

        self.up_btn.config(image=self.up_logo, height=30, width=40, bd=0)
        self.up_btn.grid(row=0, column=4, padx=10)

        self.pageNo.config(width=5, font=('Airal', 12), bd=0)
        self.total_pages.config(font=('Airal', 12), bd=0)
        self.pageNo.grid(row=0, column=5, padx=10)
        self.total_pages.grid(row=0, column=6, padx=10)

        self.down_btn.config(image=self.down_logo, height=30, width=40, bd=0)
        self.down_btn.grid(row=0, column=7, padx=10)

        self.speak_btn.config(image=self.speaker_logo, height=30, width=40, bd=0)
        self.stop_btn.config(bd=0)
        self.pause_btn.config(bd=0)

        self.read_icon_frame.grid(row=0, column=8, padx=10)
        self.speak_btn.grid(row=0, column=0, padx=10)
        self.pause_btn.grid(row=0, column=1, padx=10)
        self.stop_btn.grid(row=0, column=2, padx=10)

        self.export_btn.config(image=self.export_logo, height=30, width=40, bd=0)
        self.export_btn.grid(row=0, column=9, padx=10)

        self.print_btn.config(image=self.print_logo, height=30, width=40, bd=0)
        self.print_btn.grid(row=0, column=10, padx=10)
        # self.win.bind('<Button-1>', self.display_page_no)

        # Setting the dictionary Frame
        self.search_box = Frame(self.ind_frame, height=200, padx=2, pady=20)
        self.meaning_box = Frame(self.ind_frame, padx=5)
        self.search_box.place(relx=0, rely=0, relwidth=1, height=200, relheight=0.2)
        self.meaning_box.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

        # Setting Search Box
        self.word_entry = Entry(self.search_box, font='Doctun 20 italic')
        self.search_btn = Button(self.search_box, text='Search', command=self.search_word)
        self.word_entry.place(relx=0, rely=0.15, relwidth=0.7)
        self.search_btn.place(relx=0.7, rely=0.15, relwidth=0.3, height=35)

        # Setting Meaning Box
        self.dict_content = Canvas(self.meaning_box)
        self.word_lab = Label(self.dict_content, font='Airal 24 bold', justify='left')
        self.meaning_text = Text(self.dict_content)
        self.dict_content.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.word_lab.place(relx=0, rely=0, relwidth=0.9, relheight=0.2)
        self.meaning_text.place(rely=0.2, relx=0, relwidth=1, relheight=0.8)
        self.prononunce_btn = Button(self.dict_content, text='Pronounce', image=self.speaker_logo)

        self.dictionary = PyDictionary()

    def open_file(self):
        file = fd.askopenfilename(title="Select a File", initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if file:
            self.path = file
            filename = os.path.basename(self.path)
            self.reader = Viewer(self.path, self.content.winfo_width())
            data, total_pages = self.reader.get_metadata()
            self.current_page = 0
            if total_pages:
                self.name = data.get('title', filename[::-4])
                self.name = filename[:-4] if not self.name else self.name
                print(self.name)
                self.author = data.get('author')
                self.numPages = total_pages
                self.isFileOpen = True
                self.win.title(self.name)
                self.display_pdf()

    def display_pdf(self):
        self.total_pages.config(text=f'/ {self.numPages} Pages')
        # y = 0
        # for page_no in range(self.numPages):
        self.img, height = self.reader.get_page(self.current_page)
        # self.doc.append(self.img)
        self.content.create_image(0, 0, anchor='nw', image=self.img)
        # y += height+10
        region = self.content.bbox(ALL)
        self.content.configure(scrollregion=region)
        self.pageNo.delete(0, END)
        self.pageNo.insert(0, str(self.current_page+1))

    def next_page(self):
        if 0 <= self.current_page < self.numPages:
            self.current_page += 1
            self.display_pdf()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_pdf()

    def go_to_home(self):
        self.current_page = 0
        self.display_pdf()

    def go_to_end(self):
        self.current_page = self.numPages
        self.display_pdf()

    def read(self):
        text = self.reader.get_all_text(self.current_page)
        self.speaker = Speak(text)
        self.speaker.start()

    def stop(self):
        if self.speaker:
            self.speaker.stop()
            self.speaker = None

    def pause_or_resume(self):
        if self.speaker:
            if self.speaker.paused:
                self.speaker.resume()
            else:
                self.speaker.pause()

    def stop_read(self):
        self.speaker.engine.stop()

    def convert_word(self):
        save_path = fd.askdirectory()
        print(save_path)
        output_file = f'{save_path}/{self.name}.docx'
        Converter(self.path).convert(str(output_file), multi_processing=True)

    def search_word(self):
        word = self.word_entry.get()
        if word == '':
            showerror(title='Error', message='Please enter a word you wanna search for')
        else:
            try:
                meaning = self.dictionary.meaning(word)

                meanings = ''
                for i in meaning:
                    meanings += f'{i}: {meaning[i][0]} \n'
                self.meaning_text.delete(1.0, END)
                self.meaning_text.insert(INSERT, meanings)
                self.word_lab.config(text=word)
                self.prononunce_btn.place(relx=0.9, rely=0, height=35)

            except:
                showerror(title='Error', message='An error occurred while trying to search word meaning'\
                                                 '\nThe following could be ' \
                                                 'the cause:\n->No/Slow internet connection\n' \
                                                 '->Wrong word spelling\n' \
                                                 'Please make sure you have a stable internet connection&\n'
                                                 'the word spelling is correct')


if __name__ == '__main__':
    win = Tk()
    app = Reader(win)
    win.mainloop()

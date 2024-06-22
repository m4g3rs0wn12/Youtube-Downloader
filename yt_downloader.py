from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import threading
import os

# exception handling (push them to the text box inside root)
# download Queue for multiple downloads

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    root.title((str(int(percentage_of_completion))) + '%')

def get_path():
    path = filedialog.askdirectory()
    path_entry.delete(0, 'end')
    path_entry.insert(0,str(path))
    
def download_file(path, link):
    root.title('Downloading...')
    chunk_size = 1024
    yt = YouTube(link)
    video = yt.streams.get_highest_resolution()
    yt.register_on_progress_callback(on_progress)
    info_box.configure(state='normal')
    info_box.insert(1.0, f"Fetching \"{video.title}\".. \n")
    info_box.insert(2.0, f"Fetching successful\n")
    info_box.insert(3.0, f"Information: \n"
          f"File size: {round(video.filesize * 0.000001, 2)} MegaBytes\n"
          f"Highest Resolution: {video.resolution}\n"
          f"Author: {yt.author}\n")
    info_box.insert(4.0, "Views: {:,}\n".format(yt.views))
    info_box.configure(state='disabled')
    if state.get() == 1:
        video.download(path)  
        root.title("Done.")
    elif state.get() == 0:
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(path)
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        root.title("Done.")

def apply():
    pass

def more_options():
    more_options = Toplevel()
    more_options.title('...')
    numUrl = Label(more_options, text="numUrl: ", justify='center')
    numUrl.grid(row=0,column=0)
    count = Entry(more_options)
    count.grid(row=0,column=1)
    apply = Button(more_options, text="Apply") #command=apply)
    apply.grid(row=1, column=1,padx=(81,0), pady=(0,1), sticky='S')
        

root = Tk()
root.title('Youtube 720p Download')

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Advanced", command=more_options)
filemenu.add_separator()
filemenu.add_command(label="Quit", command=lambda:root.destroy())
menubar.add_cascade(label="Options", menu=filemenu)
root.config(menu=menubar)

path_entry = Entry(root, width=50)
path_entry.grid(row=0,column=0,columnspan=3)
path_entry.insert(0, 'C:/')

get_path_button = Button(root, text='Get Path', command=lambda:get_path())
get_path_button.grid(row=1, column=0, columnspan=3, ipadx=5)

url_entry = Entry(root, width=50)
url_entry.grid(row=2, column=0, columnspan=3)
url_entry.bind("<Button-1>", lambda e: url_entry.delete(0, 'end'))
url_entry.insert(0, "URL")

download_button = Button(root, text='Download', command=lambda:threading.Thread(
    target=download_file(path_entry.get(), url_entry.get())).start)
download_button.grid(row=3,column=2)

state = IntVar()
state.set(0)

sw1 = Radiobutton(root, text='MP3', variable=state, value=0)
sw1. grid(row=3, column=0)
sw2 = Radiobutton(root, text='MP4', variable=state, value=1)
sw2. grid(row=3, column=1)

info_box = Text(root, wrap='word', state='disabled', width=38, height=10)
info_box.grid(row=4, column=0, columnspan=3)

root.resizable(False, False)
root.mainloop()

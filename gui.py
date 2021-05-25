import multiprocessing
import os
import queue
import time
import tkinter  as tk
from io import BytesIO
from os import listdir
from tkinter import ttk
import pyperclip
import threading
from yt import *
import re
import eyed3
from PIL import Image,ImageTk
import pygame
from spotifyApi import *

MAX_FONT=("Verdana", 18)
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

PATH = 'C:/Users/roman/Music/YtMusics'

def list_files():
    return [f for f in listdir(PATH) if f[-4:]=='.mp3']

def resize_image(path, width, height):
    image = Image.open(path)
    image = image.resize((width, height), Image.ANTIALIAS)  ## The (40, 40) is (height, width)
    image = ImageTk.PhotoImage(image)
    return image

def navBar(frame):
    navFrame = tk.Frame(frame, bg='#66ff99', pady=1, padx=25)
    style = ttk.Style()
    style.configure('flat.TButton',
                    background='#66ff99',
                    borderwidth=0,
                    font=("Helvetica", 12, "bold"),
                    padx=7, cursor="hand1")
    style.map('flat.TButton',
              foreground=[('pressed', 'red'), ('active', 'blue')],
              background=[('pressed', '!disabled', '#66ff99'), ('active', '#66ff99')]
              )

    image = resize_image('headphone.png', 25, 25)
    song = ttk.Button(navFrame, text='MY MUSIC', image=image,
                      compound='left', style='flat.TButton',
                      cursor="hand2",
                      command=lambda:frame.controller.show_frame(StartPage))
    song.pack(side='left', )
    song.photo = image

    image = resize_image('discover.png', 25, 25)
    song = ttk.Button(navFrame, text='DISCOVER', style='flat.TButton',
                      image=image, compound='left', cursor="hand2",
                      command=lambda:frame.controller.show_frame(DiscoverPage))
    song.pack(side='left', padx=5)
    song.photo = image

    image = resize_image('downloading.png', 25, 25)
    song = ttk.Button(navFrame, text='DOWNLOADS', style='flat.TButton',
                      image=image, compound='left', cursor="hand2",
                      command=lambda:frame.controller.show_frame(DownloadPage))
    song.pack(side='left', padx=5)
    song.photo = image

    image = resize_image('search.png', 30, 30)
    search_icon = ttk.Button(navFrame, image=image,
                             style='flat.TButton', cursor="hand2")
    search_icon.pack(side='right')
    search_icon.photo = image

    style.configure('E.TEntry', height=10, )
    search = ttk.Entry(navFrame, style='E.TEntry', width=50, )
    search.pack(side='right', ipady=3)

    navFrame.pack(fill='x', side=tk.TOP)



class Window(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        pygame.mixer.init()
        tk.Tk.iconbitmap(self, default="download.ico")
        tk.Tk.wm_title(self, "Youtube Music Downloader")
        self.geometry("940x700")

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # menubar = tk.Menu(container)
        # filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        # filemenu.add_separator()
        # # filemenu.add_command(label="Exit", command=quit)
        # menubar.add_cascade(label="File", menu=filemenu)

        # tk.Tk.config(self, menu=menubar)

        self.frames = {}

        for F in (StartPage,DownloadPage,DiscoverPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(DownloadPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        try:
            frame.canvas.bind_all("<MouseWheel>",
                          lambda e: frame.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        except:
            pass
        frame.tkraise()


class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller=controller
        s=ttk.Style()
        s.configure('TFrame',background='#ccffdd',pady=10, padx=5)
        navBar(self)
        self.container = ttk.Frame(self, )
        self.container.pack(side='left', fill='both', expand=True, )
        self.canvasFrame()

    def resize_frame(self, e):
        self.canvas.itemconfig(self._frame_id, width=e.width)

    def canvasFrame(self):
        self.canvas = tk.Canvas(self.container, bg='blue')
        canvas = self.canvas
        vs = ttk.Scrollbar(self.container, orient='vertical', command=self.canvas.yview)
        frame = ttk.Frame(canvas)

        # self.canvas.bind_all("<MouseWheel>",self._on_mousewheel)
        frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=frame.bbox("all")
            )
        )
        self._frame_id = canvas.create_window(0, 0, anchor='nw', window=frame)
        self.canvas.update_idletasks()
        self.canvas.configure(yscrollcommand=vs.set,
                              scrollregion=self.canvas.bbox(tk.ALL))

        self.canvas.pack(side='left', expand=True, fill='both')
        vs.pack(side='right', fill='y')
        self.canvas.bind('<Configure>', self.resize_frame)
        
        for i in range(1,4):
            tk.Grid.columnconfigure(frame,i,weight=1)
        
        tk.Label(frame,  text="#" , font=MAX_FONT,bg='black',fg='white').grid(row=0,column=0,pady=3,padx=5,sticky='we')
        tk.Label(frame,text="SONG" , font=MAX_FONT,bg='black',fg='white').grid(row=0,column=1,pady=3,padx=5,sticky='we')
        tk.Label(frame, text="ARTIST" , font=MAX_FONT,bg='black',fg='white').grid(row=0,column=2,pady=3,padx=5,sticky='we')
        tk.Label(frame, text="ALBUM" , font=MAX_FONT,bg='black',fg='white').grid(row=0,column=3,pady=3,padx=5,sticky='we')

        ttk.Separator(frame, orient='horizontal').grid(row=1, column=0,columnspan=4, sticky='ew', )

        files_list = list_files()
        for index, file in enumerate(files_list):
            pos=index*2+2
            audioFile = eyed3.load(PATH + "/" + file)
            t = audioFile.tag

            fName=f'img-{t.artist}-{t.title}.jpeg'
            if '/' in fName:
                fName=fName.replace('/','-')
            if '\\' in fName:
                fName=fName.replace('\\','-')
            fPath = os.path.join(os.getcwd()+'\\images\\',fName)

            # if not os.path.exists('images/' + fName):
            #     if t.images:
            #         imgdata = t.images[0].image_data
            #         with open(fPath, 'wb') as f:
            #             f.write(imgdata)
            # try:
            #     image=resize_image(fPath,60,60)
            # except :
            #     image=resize_image('images/music_logo.png',60,60)

            def play(song):
                pygame.mixer.music.load(song)
                pygame.mixer.music.play(loops=0)
            style=ttk.Style()

            style.map("image.TButton",
                      foreground=[('!active', 'black'), ('pressed', 'red'), ('active', 'white')],
                      background=[('!active', 'grey75'), ('pressed', 'green'), ('active', 'black')]
                      )


            # imBtn=ttk.Button(frame,cursor='plus',style='image.TButton',command=lambda song=(PATH+'/'+file) : play(song))
            # imBtn.grid(row=pos, column=0, pady=3, padx=5,sticky='w')
            # imBtn.config(image=image)
            # imBtn.photo=image

            ttk.Label(frame, wraplength=300,background='#ccffdd', text=t.title, font=LARGE_FONT,).grid(row=pos, column=1, pady=3, padx=5,sticky='w')
            ttk.Label(frame, wraplength=300, text=t.artist, font=LARGE_FONT,background='#ccffdd').grid(row=pos, column=2, pady=3, padx=5,sticky='w')
            ttk.Label(frame, wraplength=300, text=t.album, font=LARGE_FONT,background='#ccffdd').grid(row=pos, column=3, pady=3, padx=5,sticky='w')

            ttk.Separator(frame, orient='horizontal').grid(row=pos+1, column=0, columnspan=4,sticky='ew', )





class DownloadPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)

        navBar(self)

        self.container=ttk.Frame(self)
        self.container.pack(side='left',fill='both',expand=True,padx=1,pady=2)

        self.controller=controller
        self.style = ttk.Style()
        self.style.configure('uF.TFrame',background='#80ff80')
        self.upperFrame=ttk.Frame(self.container,style='uF.TFrame')
        self.upperFrame.pack(side='top',fill='x',padx=2,ipady=10)


        pasteBtn = ttk.Button(self.upperFrame,text='Paste',
                              command=lambda:threading.Thread(target=self.parseUrl).start())
        pasteBtn.pack(side='left',padx=5,ipady=3)


    def parseUrl(self):

        url = pyperclip.paste().strip() #url <- pasted url

        if 'youtube.com' in url or 'youtu.be' in url: #checking if it is valid url

            #check if it is playlist then download all playlist videos
            if "playlist" in url:
                print("Downloading Playlist")
                urls=downloadAudioPlaylist(url)
                tl=[]
                for url in urls:
                    progressBar = ttk.Progressbar(self.container, orient='horizontal',
                                                  length=300, mode='indeterminate')
                    progressBar.pack(side='top', anchor='nw', pady=10, padx=5)
                    progressBar.start(10)
                    t=threading.Thread(target=lambda:self.download(url,progressBar))
                    t.start()
                    tl.append(t)
                for t in tl:
                    t.join()


            elif "list=" in url:
                try:
                    result = re.search(r"list=.*", url).group(0)
                    result=result[5:]
                except :
                    result = re.search(r"list=.*&", url).group(0)
                    result=result[5:-1]
                if len(result)<15:
                    self.download(url,progressBar)
                    return 0
                else:
                    self.popupdownloadOption(url,result)

            else:
                progressBar = ttk.Progressbar(self.container, orient='horizontal',
                                              length=300, mode='indeterminate')
                progressBar.pack(side='top', anchor='nw', pady=10, padx=5)
                progressBar.start(10)
                self.download(url,progressBar)
        else:
            self.invalidPopUp('Invalid url')



    def invalidPopUp(self,msg):
        popup = tk.Tk()
        popup.wm_title("!")
        label = tk.Label(popup, text=msg, font=LARGE_FONT,bg='red',pady=10,padx=10,fg='white')
        label.pack(side="top", fill="x", pady=30,padx=50)
        B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack(pady=10)
        popup.mainloop()

    def popupdownloadOption(self,url,result):
        popup = tk.Tk()
        popup.wm_title("???")
        label = ttk.Label(popup, text="What do you want to download?", font=LARGE_FONT)
        label.pack(side="top", fill="x", pady=10)

        B1 = ttk.Button(popup, text="Whole Playlist", command=lambda: self.dPorA(url, popup,result, 'p'))
        B2 = ttk.Button(popup, text="Only this song", command=lambda: self.dPorA(url, popup,result, 'a'))
        B1.pack(pady=5)
        B2.pack(pady=5)
        popup.mainloop()

    def dPorA(self,url, popup,result, opt):
        popup.destroy()
        if opt == 'p':
            url = 'youtube.com/playlist?list='+result
            print(url)
            urls = downloadAudioPlaylist(url)
            tl = []
            for url in urls:
                progressBar = ttk.Progressbar(self.container, orient='horizontal',
                                              length=300, mode='indeterminate')
                progressBar.pack(side='top', anchor='nw', pady=10, padx=5)
                progressBar.start(10)
                t = threading.Thread(target=lambda: self.download(url, progressBar))
                t.start()
                tl.append(t)
            for t in tl:
                t.join()
        else:
            progressBar = ttk.Progressbar(self.container, orient='horizontal',
                                          length=300, mode='indeterminate')
            progressBar.pack(side='top', anchor='nw', pady=10, padx=5)
            progressBar.start(10)
            self.download(url,progressBar)
            return

    def download(self,url,progressBar):
        try:
            for _ in range(3):
                yt = parseUrl(url)

                break
        except Exception as ec:
            # progressBar.stop()
            # progressBar.destroy()
            l=tk.Label(self.container,text=ec,bg='red',fg='white')
            l.pack(side='top',anchor='nw',pady=10,padx=5)
            return 0


        if fileExist(getPath(yt.title + '.mp3')):
            print("File Already Exist")
            progressBar.stop()
            progressBar.destroy()
            l=tk.Label(self.container,text='File Already Exist', bg='red',
                       fg='white',font=MAX_FONT)
            l.pack(side='top',anchor='nw',padx=5,ipadx=50,pady=5)
            l.after(3000,l.destroy)
            return 0
        progressBar.stop()
        progressBar.configure(mode='determinate')
        progressBar['value']=0

        print('*******Downloading Audio***********')

        defaultFileName = yt.streams.first().default_filename

        audioFileName = defaultFileName.replace(' ', '_')
        audioFilePath = getPath(audioFileName)

        # getting streams of only audio with highest res
        audio = yt.streams.filter(only_audio=True).first().download(dPath)
        progressBar['value'] += 15

        # Renaming and deleting if file with that name exist
        if fileExist(audioFilePath):
            os.remove(audioFilePath)
        os.rename(audio, audioFilePath)
        progressBar['value'] += 5
        # convert mp4 to mp3
        mp3File = getPath(yt.title + '.mp3')
        print('######Converting to mp3########')
        oldFile = audioFilePath
        newFile = mp3File
        toMp3(oldFile, newFile)
        print('######Converted########')

        progressBar['value'] += 25

        print('######Setting Metadata########')
        setMeta(newFile, yt.title)
        print('######Done Setting########')

        progressBar['value'] += 55

        # # increasing volume level
        # _fName=getPath(yt.title+".mp3").replace(' ','_')
        # subprocess.run(f'ffmpeg -i {mp3File} -filter:a "volume=2" {_fName}')
        # fName=yt.title+".mp3"
        # print(fName)
        # os.rename(_fName,fName)

class DiscoverPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self,parent)
        self.controller = controller

        navBar(self)

        self.container = ttk.Frame(self,)
        self.container.pack(side='left', fill='both', expand=True,)

        # self.canvasFrame()

    def resize_frame(self, e):
        self.canvas.itemconfig(self._frame_id,  width=e.width)

    def canvasFrame(self):
        self.canvas = tk.Canvas(self.container, bg='blue')
        self.canvas.pack(side='left', expand=True, fill='both')

        vs = ttk.Scrollbar(self.container, orient='vertical', command=self.canvas.yview)
        vs.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=vs.set,)
        self.canvas.bind('<Configure>',
                         lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        frame = ttk.Frame(self.canvas)
        frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=frame.bbox("all")
            )
        )
        self._frame_id = self.canvas.create_window(0, 0, anchor='nw', window=frame)

        self.canvas.bind('<Configure>', self.resize_frame)

        albums = newReleases()

        def getImage(url):
            image = requests.get(url)
            image_data = BytesIO(image.content)

            image=resize_image(image_data,30,30)
            return image

        for album in albums:
            s=time.perf_counter()
            image=getImage(album['image_url'])
            f=time.perf_counter()
            print(f-s)
            albumIm=tk.Label(frame,image=image)
            albumIm.photo=image
            albumIm.grid()

if __name__=='__main__':
    app=Window()
    app.mainloop()

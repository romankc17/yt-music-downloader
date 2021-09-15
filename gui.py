import time
import tkinter  as tk
from io import BytesIO
from os import listdir
from tkinter import ttk
from tkinter import font as tkFont

import PIL
import pyperclip
import threading

lock = threading.Lock()
from PIL import Image, ImageTk
import pygame

from yt import *
from spotifyApi import *
from spotifyApi import SpotifyApi
from youtubeApi import YoutubeApi

youtubeApi = YoutubeApi()
musicDownloader = MusicDownloader()

spotiApi = SpotifyApi()

MAX_FONT = ("Verdana", 18)
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

PATH = 'C:/Users/roman/Music/YtMusics'
import eyed3


def list_files():
    return [f for f in listdir(PATH) if f[-4:] == '.mp3']


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
                      command=lambda: frame.controller.show_frame(StartPage))
    song.pack(side='left', )
    song.photo = image

    image = resize_image('discover.png', 25, 25)
    song = ttk.Button(navFrame, text='DISCOVER', style='flat.TButton',
                      image=image, compound='left', cursor="hand2",
                      command=lambda: frame.controller.show_frame(DiscoverPage))
    song.pack(side='left', padx=5)
    song.photo = image

    image = resize_image('downloading.png', 25, 25)
    song = ttk.Button(navFrame, text='DOWNLOADS', style='flat.TButton',
                      image=image, compound='left', cursor="hand2",
                      command=lambda: frame.controller.show_frame(DownloadPage))
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
    def __init__(self, *args, **kwargs):
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

        for F in (StartPage, DownloadPage, DiscoverPage):
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
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        s1 = ttk.Style()
        s1.configure('F1.TFrame', background='#ccffdd', pady=10, padx=5)
        navBar(self)
        self.container = ttk.Frame(self, style='F1.TFrame')
        self.container.pack(side='left', fill='both', expand=True, )
        # self.canvasFrame()


class DownloadPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        navBar(self)

        self.container = ttk.Frame(self)
        self.container.pack(side='left', fill='both', expand=True, padx=1, pady=2)

        self.controller = controller
        style = ttk.Style()
        style.configure('uF.TFrame', background='green')
        self.upperFrame = ttk.Frame(self.container, style='uF.TFrame')
        self.upperFrame.pack(side='top', fill='x', padx=2, ipady=10)
        self.lowerFrame = tk.Frame(self.container)
        self.lowerFrame.pack(side='bottom', fill='both', expand=True, )
        self.createDownloadFrame()

        pasteBtn = ttk.Button(self.upperFrame, text='Paste',
                              command=lambda: threading.Thread(target=self.parseUrl).start())
        pasteBtn.pack(side='left', padx=5, ipady=3)

        self.i = 100
        # for _ in range(10):
        #     self.eachDownloadFrame()

    # # creating a scrollable frame to show dowloads
    def createDownloadFrame(self):
        canvas = tk.Canvas(self.lowerFrame, bg='#80ff80')
        canvas.pack(side='left', expand=True, fill='both')

        vs = tk.Scrollbar(self.lowerFrame, orient='vertical', command=canvas.yview)
        vs.pack(side='right', fill='y')

        downloadFrame = tk.Frame(canvas, )
        downloadFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=downloadFrame.bbox('all')
            )
        )
        _frame_id = canvas.create_window(0, 0, anchor='nw', window=downloadFrame)

        def resize(e):
            canvas.itemconfig(_frame_id, width=e.width)

        # canvas.update_idletasks()
        canvas.bind('<Configure>', resize)

        canvas.configure(yscrollcommand=vs.set)
        canvas.configure(scrollregion=canvas.bbox("all"))
        self.downloadFrame = downloadFrame

    def retrievingText(self, master):
        font = tkFont.Font(family='Arial', size=16, weight='bold')
        text = 'Retrieving Information.......'

        t = tk.Text(master, bg=self.download_background, fg='white')
        t.insert(tk.INSERT, text)
        t.configure(font=font)
        t.pack()

    def song_info_frame(self, master, yt_title, song_info):
        leftFrame = tk.Frame(master, width=64, height=64, bg=self.download_background)
        rightFrame = tk.Frame(master, height=64, bg=self.download_background)

        leftFrame.pack(side='left')
        rightFrame.pack(side='right', expand=True, fill='both', )

        # tk.Grid.columnconfigure(master,0,weight=1)
        # # tk.Grid.columnconfigure(master,0,weight=1)
        #
        thumbnail_url = song_info['images']['low']['url']
        image = requests.get(thumbnail_url)
        image_bits = BytesIO(image.content)
        im = PIL.Image.open(image_bits)
        image = ImageTk.PhotoImage(im)
        labelImage = tk.Label(leftFrame, image=image, bg=self.download_background)
        labelImage.photo = image
        labelImage.pack()
        labelImage.pack_propagate(0)
        #
        font = tkFont.Font(family='Arial', size=16, weight='bold')
        t = tk.Label(rightFrame, text=yt_title, bg=self.download_background, fg='white', font=font)
        t.grid(row=0, column=0, columnspan=3)

        titleLabel = tk.Label(rightFrame, text=f"Title: {song_info['name']}", bg="white")
        titleLabel.grid(row=1, column=0, padx=5)

        artistLabel = tk.Label(rightFrame, text=f"Artist: {';'.join(song_info['artists'])}", bg='white')
        artistLabel.grid(row=1, column=1, padx=5)

        albumLabel = tk.Label(rightFrame, text=f"Album: {song_info['album_name']}", bg='white')
        albumLabel.grid(row=1, column=2, padx=5)

        # progress bar
        bar = self.downloadBar(rightFrame, length=300)
        bar.grid(row=2, column=1, columnspan=3, sticky='ns')

        return bar

    def downloadBar(self, master, length=int):
        bar = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=length)
        return bar

    def eachDownloadFrame(self):
        self.download_background = 'blue'
        s = ttk.Style()
        s.configure('dFrame.TFrame', background=self.download_background)
        f = ttk.Frame(self.downloadFrame, style='dFrame.TFrame', height=64)
        tk.Grid.columnconfigure(self.downloadFrame, 0, weight=1)
        tk.Grid.columnconfigure(f, 0, weight=1)
        f.grid(row=self.i, column=0, pady=1, sticky='nsew')
        f.pack_propagate(0)

        self.retrievingText(f)
        # tk.Label(f,text='Retrieving Information',bg='blue').grid(row=0,column=0)
        lock.acquire()
        self.i -= 1
        lock.release()
        return f

    def downloadMusic(self, url, video_id):
        # Create download frame and label song info
        f = self.eachDownloadFrame()
        f.grid_propagate(0)

        # getting video info from youtube api
        video_info = youtubeApi.video_info(video_id)
        yt_title = video_info['title']

        # Extract the search keys from yt title
        keys = spotiApi.purify_ytTitle(yt_title)
        q = ' '.join(keys)

        # using search key to search song in spotify
        print("Searching q: " + q)
        song_info = spotiApi.get_first_search(q)

        # set the title as youtube video name if not found searching in spotify
        if song_info['name'].strip() == "":
            song_info['name'] = yt_title
            song_info['images'] = {
                "high": video_info['thumbnails']["standard"],
                "low": video_info['thumbnails']["default"]
            }

        for widget in f.winfo_children():
            widget.destroy()

        # make a frame with song info and return progress bar
        bar = self.song_info_frame(f, yt_title, song_info)

        filename = ' X '.join(song_info['artists']) + " - " + song_info['name']
        audio_file = musicDownloader.downlod(url, filename)
        bar['value'] += 50
        musicDownloader.set_metadata(audio_file, song_info)
        bar['value'] += 50

    def parseUrl(self):
        url = pyperclip.paste().strip()  # url <- pasted url

        # initialize Downlaod object with yt url
        link_type = musicDownloader.link_type(url)
        if not link_type['type']:  # return types of link 0 if is invalid url
            self.invalidPopUp("Invalid Url")
            return 0

        # if the url is for a music video only
        if link_type['type'] == 2:
            video_id = link_type['video_id']
            self.downloadMusic(url, video_id)
            return

        # if the url is for playlist only
        elif link_type['type'] == 3:
            print("Downloading Playlist")
            urls = musicDownloader.get_playlist_urls(url)
            tl = []
            for url in urls:
                video_id = musicDownloader.link_type(url)['video_id']
                t = threading.Thread(target=lambda: self.downloadMusic(url, video_id))
                t.start()
                tl.append(t)
            for t in tl:
                t.join()

        else:
            video_id = link_type['video_id']
            playlist_id = link_type['playlist_id']
            self.popupdownloadOption(video_id, playlist_id)

    def invalidPopUp(self, msg):
        popup = tk.Tk()
        popup.wm_title("!")
        label = tk.Label(popup, text=msg, font=LARGE_FONT, bg='red', pady=10, padx=10, fg='white')
        label.pack(side="top", fill="x", pady=30, padx=50)
        B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        B1.pack(pady=10)
        popup.mainloop()

    # Choose option if to download playlist or only a video
    def popupdownloadOption(self, video_id, playlist_id):
        popup = tk.Tk()
        popup.wm_title("???")
        label = ttk.Label(popup, text="What do you want to download?", font=LARGE_FONT)
        label.pack(side="top", fill="x", pady=10)

        B1 = ttk.Button(popup, text="Whole Playlist", command=lambda: self.dPorA(popup, 'p', video_id, playlist_id))
        B2 = ttk.Button(popup, text="Only this song", command=lambda: self.dPorA(popup, 'a', video_id, playlist_id))
        B1.pack(pady=5)
        B2.pack(pady=5)
        popup.mainloop()

    def dPorA(self, popup, opt, video_id, playlist_id):
        popup.destroy()
        if opt == 'p':
            url = 'youtube.com/playlist?list=' + playlist_id
            url = 'https://youtu.be/6tsu2oeZJgo?list=PLunpsO_IVuepyV8k1II8gUqRn8qv4fLJB'
            print(url)
            urls = musicDownloader.get_playlist_urls(url)
            tl = []
            print(urls)
            for url in urls:
                video_id = musicDownloader.link_type(url)['video_id']
                t = threading.Thread(target=lambda: self.downloadMusic(url, video_id))
                t.start()
                tl.append(t)
            for t in tl:
                t.join()
        else:
            url = 'youtube.com/' + video_id
            self.downloadMusic(url, video_id)
            return


class DiscoverPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        navBar(self)

        self.container = ttk.Frame(self, )
        self.container.pack(side='left', fill='both', expand=True, )


if __name__ == '__main__':
    app = Window()
    app.mainloop()

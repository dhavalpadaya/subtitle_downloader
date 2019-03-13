import os
import sys
import tkinter as tk
from tkinter import filedialog
#pip install guessit
from guessit import guessit
from utils import File
from utils import decompress
from xmlrpc.client import ServerProxy, Transport
import io
#pip install IMDbPY
import imdb
import ntpath
import configs as cfg

imdbObj = imdb.IMDb()

#Url of opensubtitles API
url = 'https://api.opensubtitles.org/xml-rpc'

transport = Transport()
transport.user_agent = 'OSTestUserAgent'

#Create a Tkinter window
window = tk.Tk()
window.title('Subtitle Downloader')
window.geometry("300x150") #You want the size of the app to be 500x500
window.resizable(0, 0)

server = ServerProxy(url,allow_none=True, transport=transport)
token = server.LogIn('', '', 'en', 'TemporaryUserAgent')['token']

videoFilesExtensionList = cfg.videoFilesExtensionList
subtitleLanguages = cfg.subtitleLanguages
maxSubtitles= cfg.maxSubtitles

#Generate a text file with information of given file from IMDB
def generateTextFile(root,filenameWithoutExtension,movieObj):
    fpath = os.path.join(root, filenameWithoutExtension+".info.txt")
    if not os.path.isfile(fpath):
        try:
            with io.open(fpath, "w", encoding="utf-8") as f: 
                if 'title' in movieObj:       
                    f.write("Title - "+movieObj["title"] + "\n")
                if 'kind' in movieObj:       
                    f.write("Type - "+movieObj["kind"] + "\n")
                if 'year' in movieObj:
                    f.write("Year - "+str(movieObj['year'])+ "\n")
                if 'number of seasons' in movieObj:
                    f.write("Number Of Seasons - "+str(movieObj['number of seasons'])+ "\n")
                if 'series years' in movieObj:
                    f.write("Series Years - "+str(movieObj['series years'])+ "\n")
                if 'rating' in movieObj:
                    f.write("Rating - "+str(movieObj['rating'])+ "\n")
                if 'votes' in movieObj:
                    f.write("Votes - "+str(movieObj['votes'])+ "\n")
                if 'genres' in movieObj:
                    f.write('Genres:'+ "\n")
                    for genre in movieObj['genres']:
                        f.write("\t"+genre+ "\n")
                if 'plot outline' in movieObj:
                    f.write("Plot Outline - "+movieObj['plot outline']+ "\n")
                if 'cast' in movieObj:
                    f.write('Cast:'+ "\n")
                    for cast in movieObj['cast']:
                        f.write("\t"+cast['name']+ "\n")
                if 'directors' in movieObj:
                    f.write('Directors:'+ "\n")
                    for director in movieObj['directors']:
                        f.write("\t"+director['name']+ "\n")
            print("IMDB text file generated for file "+filenameWithoutExtension)
        except IOError as e:
            print("There was an error generating text file for information of {}.".format(fpath),file=sys.stderr)
            print(e)
    else:
        print("IMDB text file already exists for file "+filenameWithoutExtension)

#IMDbPY is a Python package useful to retrieve and manage the data of the IMDb movie database about movies, people, characters and companies.
#pip install IMDbPY
#to get MOVIE or TV Episode details from IMDB based on filename
def getIMDBGetails(root,filename):
    try:
        #guessIt is a python library that extracts as much information as possible from a video filename. http://guessit.io
        #to get file details based on filename using python library
        #pip install guessit
        outputFromGuessIt = guessit(filename)
        filenameWithoutExtension = os.path.splitext(filename)[0]
        title = outputFromGuessIt["title"]
        result = imdbObj.search_movie(title)
        idOfMovie = result[0].movieID
        movieObj = imdbObj.get_movie(idOfMovie)
        # print(movieObj.infoset2keys)
        print("********************************Details From IMDB******************************************")
        if 'title' in movieObj:
            print("Title - "+movieObj['title'])
        if 'kind' in movieObj:
            print("Type - "+movieObj['kind'])
        if 'year' in movieObj:
            print("Year - "+str(movieObj['year']))
        if 'number of seasons' in movieObj:
            print("Number Of Seasons - "+str(movieObj['number of seasons']))
        if 'series years' in movieObj:
            print("Series Years - "+str(movieObj['series years']))
        if 'rating' in movieObj:
            print("Rating -"+str(movieObj['rating']))
        if 'votes' in movieObj:
            print("Votes - "+str(movieObj['votes']))
        if 'genres' in movieObj:
            print('Genres:')
            for genre in movieObj['genres']:
                print("\t"+genre+ "\n")
        if 'plot outline' in movieObj:
            print("Plot Outline - "+movieObj['plot outline'])
        print("********************************Details From IMDB******************************************")
        generateTextFile(root,filenameWithoutExtension,movieObj)
    except:
        print("There was an error getting IMDB details of {}.".format(filename),file=sys.stderr)

def searchAndDownloadSubtitleBasedOnFileName(root,filename,files=None):
    try:
        filenameWithoutExtension = os.path.splitext(filename)[0]
        #To get all files which contains same name as this file(extension won't be checked while comparing)
        allFilesWithThisVideoFileName = []
        if files is not None:
            allFilesWithThisVideoFileName = [s for s in files if filenameWithoutExtension in s]
        if any(".srt" in s for s in allFilesWithThisVideoFileName):
            print("Subtitle file for movie "+filenameWithoutExtension+" Already exists.")
        else:
            #guessIt is a python library that extracts as much information as possible from a video filename. http://guessit.io
            #to get file details based on filename using python library
            #pip install guessit
            outputFromGuessIt = guessit(filename)
            titleFromGuessIt = outputFromGuessIt["title"]
            season = outputFromGuessIt.get('season','')
            episode = outputFromGuessIt.get('episode','')
            videoFile = File(os.path.join(root, filename))
            videoFileHash = videoFile.get_hash()
            videoFileSize = videoFile.size
            print('Search Subtitle for movie - '+filename)
            searchResponse = server.SearchSubtitles(token, [{'sublanguageid': subtitleLanguages, 'moviehash': videoFileHash, 'moviebytesize': videoFileSize,'season':season,'episode':episode,'query':titleFromGuessIt}], {'limit':maxSubtitles})
            data = searchResponse.get('data')
            if len(data) > 0:
                for oneSub in data:
                    id_subtitle = oneSub.get('IDSubtitleFile')
                    id_subtitle_lang = oneSub.get('SubLanguageID')
                    resp = server.DownloadSubtitles(token, [id_subtitle])
                    if resp['status'] == '200 OK':
                        dataFromResponse = resp['data']
                        for eachResponse in dataFromResponse:
                            subtitleByteData = eachResponse['data']
                            decoded_data = (decompress(subtitleByteData, 'utf-8') or decompress(subtitleByteData, 'latin1'))
                            if not decoded_data:
                                print("An error occurred while decoding subtitle file ID {}.".format(id_subtitle), file=sys.stderr)
                            else:
                                fpath = os.path.join(root, filenameWithoutExtension+"."+id_subtitle+"."+id_subtitle_lang+".srt")
                                try:
                                    with io.open(fpath, "w", encoding="utf-8") as f:
                                        f.write(decoded_data)
                                    print("Subtitle file generated for file "+filenameWithoutExtension)
                                except IOError as e:
                                    print("There was an error writing file {}.".format(fpath),file=sys.stderr)
                                    print(e)
                    else:
                        print(resp)
            else:
                print("No Subtitle found for "+filename)
    except:
        print("There was an error downloading subtitle for file {}.".format(fpath),file=sys.stderr)

def processForAFolder():
    folder_path = filedialog.askdirectory()
    window.destroy()
    if folder_path is not None and folder_path != '':
        print('Selected Folder - '+folder_path)
    else:
        print('Folder is not selected.')
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if(filename.endswith(videoFilesExtensionList)):
                searchAndDownloadSubtitleBasedOnFileName(root,filename,files)
                getIMDBGetails(root,filename)

def processForAFile():
    file_path = filedialog.askopenfilename(filetypes=[(ext, "*"+ext) for ext in videoFilesExtensionList])
    window.destroy()
    if file_path is not None and file_path != '':
        print('Selected File - '+file_path)
        filename = ntpath.basename(file_path)
        root = ntpath.dirname(file_path)
        print('Directory - '+root)
        if(filename.endswith(videoFilesExtensionList)):
            searchAndDownloadSubtitleBasedOnFileName(root,filename)
            getIMDBGetails(root,filename)
    else:
        print('File is not selected.')

def showButtonWindow():
    tk.Button(window, text="Select A Single File", fg="red", command = lambda: processForAFile(),height = 2, width = 20).grid(row=0,column=0,padx=70,pady=10,sticky='e')
    tk.Button(window, text="Select A Folder", fg="red", command = lambda: processForAFolder(),height = 2, width = 20).grid(row=1,column=0,padx=70,pady=10,sticky='we')
    window.mainloop()

if len(sys.argv) > 1 and sys.argv[1] == 'lang_list':
    print(server.GetSubLanguages('en'))
    sys.exit()
elif len(sys.argv) > 1 and sys.argv[1] == 'file':
    processForAFile()
elif len(sys.argv) > 1 and sys.argv[1] == 'folder':
    processForAFolder()
else:
    showButtonWindow()
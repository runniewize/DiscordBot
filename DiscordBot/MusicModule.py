from youtube_dl import YoutubeDL

from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL


import os
import os.path
import json

SongsList = []

def SoundSearch(keywords, playlist_id="Playlist", duration=5):
    try:

        videosSearch = VideosSearch(keywords, limit = 5)


        search_result = videosSearch.result()['result']


        results_dur = []
        results_ids = []
        results_imgs = []

        x = 0
        while (x != len(search_result)):
            #print(search_result[x]['id'])
            #print(search_result[x]['duration'])
            results_dur.append(search_result[x]['duration'])
            results_ids.append(search_result[x]['id'])
            results_imgs.append(search_result[x]['thumbnails'][0]['url'])
            x = x + 1

        x = 0
        while (x != len(results_dur)):
            points_id = results_dur[x].find(":")
            cur_result_dur = ""
            y = 0
            while (y != points_id):

                cur_result_dur = str(cur_result_dur) + str(results_dur[x][y])
                #print(cur_result_dur)

                y = y + 1

            if (int(cur_result_dur) < int(duration)):
                #print(str(results_dur[x]) + "< then " + str(duration) + " FINE FINE FINE")

                result_id = results_ids[x]
                result_img = results_imgs[x]
                result_dur = results_dur[x]
                break
            else:
                #print(str(results_dur[x]) + "> then " + str(duration) + " ALARM ALARM ALARM")
                print("")
            x = x + 1

        if (result_id == None):
            result_id = results_ids[x]

        file_list = os.listdir("music")

        song_id = None

        x = 0

        for files in file_list:
            curFileCheck = "song" + str(x) + ".mp3"
            #print("x is " + str(x))
            if curFileCheck in file_list:
                #print("file already exist")
                x = x + 1
            else:
                #print("file not exist, need to create new")
                song_id = x



        ydl_opts = {'format': 'bestaudio', 'outtmpl': 'music/song' + str(song_id) + '.mp3',
        'noplaylist' : True,
        'keep' : False,
        'post-processing': [{'extract-audio' : True,}],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            
        }]}

        with YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            video = ydl.extract_info("https://www.youtube.com/watch?v=" + str(result_id), download=True) # СМЕНИТЬ НА TRUE !!!!!! TAG ТЭГ WARNING

            print("Media downloaded: " + str(video['title']))

        

        SongsListDef(str(video['title']), str('song' + str(song_id) + '.mp3'), result_img, "https://www.youtube.com/watch?v=" + str(result_id), playlist_id, result_dur)

        return("https://www.youtube.com/watch?v=" + str(result_id))

    except:
        print("[!!!] SoundSearch error [104]: relevant video could not be found.")
        return ("Не удалось найти медиа на YouTube. Перепроверь параметры запроса.")

def SongsListDef(media_title, file_name, avatar, YTLink, playlist_id, audio_duration):


    SongEntry = {'SongTitle' : media_title, 'FileName' : file_name, 'Avatar' : avatar, 'YouTube' : YTLink, 'Duration' : audio_duration}
    loaded_data = []

    if (ReadMusicData() == "Undefined"):
        #print("Music data undefined, making first data value.")
        loaded_data = [{'Playlist_Title' : playlist_id, 'Playlist_Info' : [SongEntry]}]
    else:
        loaded_data = ReadMusicData()
        #print(loaded_data)

        x = 0
        playlist_already_exist = False
        for cur_playlist in loaded_data:
            if (loaded_data[x]['Playlist_Title'] == playlist_id):
                loaded_data[x]['Playlist_Info'].append(SongEntry)
                playlist_already_exist = True
                break
            else:
                x = x + 1

        if (playlist_already_exist == False):
            loaded_data.append({'Playlist_Title' : playlist_id, 'Playlist_Info'  : [SongEntry]})

    with open('music\MusicData.json', 'w') as outfile:


        json.dump(loaded_data, outfile)

        outfile.close()

    print("\n----------------- Soundfind: COMPLETE ----------------------\n")
    return YTLink


def ReadMusicData():

    try:
        with open('music\MusicData.json', 'r') as outfile:
            all_music_data = json.load(outfile)

            #print(all_music_data)
        
            outfile.close()
            return all_music_data
    except:
        return "Undefined"

def ClearMusicData():
    try:
        file_list = os.listdir("music")
        for file in file_list:
            if (file[0] + file[1] + file[2] + file[3] == "song"):
                os.remove("music\\" + file)
        print("MusicData file removed.")
        os.remove("music\MusicData.json")
    except:
        print("MusicData file undefined.")

def RemoveMusicDataEntry(playlist_id=0, songID="all"):

    print("\n----------- RemoveMusicDataEntry() trying to start... -------------\n")

    loaded_data = ReadMusicData()

    if (playlist_id == "all"):
        try:
           ClearMusicData()
           return "Медиатека стёрта."
        except:
           return "Плейлистов не существует."

    try:
        playlist_id = TryConvertInt(playlist_id)
    except:
        print("CONVERTING TO INT PLAYLIST FAILED.")

    file_list = os.listdir("music")

    if "MusicData.json" in file_list:
        try:

            if (type(playlist_id) == str):
                x = 0
                FindExistingPlaylist = False
                for cur_playlist in loaded_data:
                    if (playlist_id == loaded_data[x]['Playlist_Title']):
                        FindExistingPlaylist = True
                        #print("find match name playlist")


                        if (songID == "all"):

                            file_list = os.listdir("music")

                            print("songID equals ALL - Remove whole playlist with following NAME: " + " " + loaded_data[x]['Playlist_Title'] + " - ID EQUALS TO: " + str(x))

                            for cur_file in file_list:
                                y = 0
                                #print("cur_file is " + str(cur_file))
                                for cur_song in loaded_data[x]['Playlist_Info']:
                                    #print("cur_song is " + str(cur_song['FileName']))
                                    #print(loaded_data[x]['Playlist_Info'][y]['FileName'])

                                    if (cur_file == loaded_data[x]['Playlist_Info'][y]['FileName']):
                                        #print("stage passed")
                                        #print("Current file match with: " + loaded_data[x]['Playlist_Info'][y]['FileName'] + " must be deleted i guess...")
                                        os.remove("music\\" + loaded_data[x]['Playlist_Info'][y]['FileName'])
                                        print("Removing .mp3: /music/" + loaded_data[x]['Playlist_Info'][y]['FileName'])
                                        y = y + 1
                                    else:
                                        print("Current file doesn't match with: " + loaded_data[x]['Playlist_Info'][y]['FileName'] + "with file to delete, skipping...")
                                        y = y + 1

                            print("Removing playlist: " + loaded_data[x]['Playlist_Title'])

                            deleted = [loaded_data[x]['Playlist_Title'], "Playlist"]
                            
                            loaded_data.pop(x)

                        else:
                            try:
                                songID = int(songID) - 1
                                if (songID < 0):
                                    #print("SongID below zero, making it equals: 0")
                                    songID = 0
                                elif (songID >= len(ReadMusicData()[x]['Playlist_Info'])):
                                    songID = len(ReadMusicData()[x]['Playlist_Info']) - 1
                                    #print("SongID above len of ReadMusicData(), making it equals: " + str(songID))
                                #print("STR to INT convertation, returned SongID:" + str(songID))
                            except:
                                print("SongID converting to INT failed, processing as string...")

                            if (type(songID) == int):

                                if (songID >= len(loaded_data[x]['Playlist_Info'])):
                                    songID = len(loaded_data[x]['Playlist_Info'])
                                elif (songID < 0):
                                    songID = 0

                                mp3file = loaded_data[x]['Playlist_Info'][songID]['FileName']

                                deleted = [loaded_data[x]['Playlist_Info'][songID]['SongTitle'], "Song"]

                                loaded_data[x]['Playlist_Info'].pop(songID)

                                

                                os.remove("music\\" + mp3file)

                                print("Removing track: " + mp3file + " - " + deleted[0])

                                if (len(loaded_data[x]['Playlist_Info']) == 0):
                                    loaded_data.pop(x)
                                    print("Removing playlist, because now it is empty.")
                            
                            else:
                                print("\n------ [!] ERROR: MusicData: songID is not INTEGER [!] ------\n")

                                return "Необходимо указать ID песни."

                    else:
                        x = x + 1
                
                if (FindExistingPlaylist == False):

                    print("\n------ [!] MusicData(): Playlist STR is not exist. [!] ------\n")
                    return "Указанный плейлист не существует."

            else:

                if (len(loaded_data) != 0):
                    if (songID == "all"):
                        file_list = os.listdir("music")

                        print("songID equals ALL - Remove whole playlist with following NAME: " + " " + loaded_data[playlist_id]['Playlist_Title'] + " - ID EQUALS TO:" + str(playlist_id) + " - type is " + str(type(playlist_id)))

                        for cur_file in file_list:
                            x = 0
                            print("cur_file is " + str(cur_file))
                            for cur_song in loaded_data[playlist_id]['Playlist_Info']:
                                #print("cur_song is " + str(cur_song))
                                if (cur_file == loaded_data[playlist_id]['Playlist_Info'][x]['FileName']):
                                    #print("Current file match with: " + loaded_data[playlist_id]['Playlist_Info'][x]['FileName'] + " must be deleted i guess...")
                                    os.remove("music\\" + loaded_data[playlist_id]['Playlist_Info'][x]['FileName'])
                                    print("Removing .mp3: /music/" + loaded_data[playlist_id]['Playlist_Info'][x]['FileName'])
                                    x = x + 1
                                else:
                                    #print("Current file doesn't match with: " + loaded_data[playlist_id]['Playlist_Info'][x]['FileName'] + "with file to delete, skipping...")
                                    x = x + 1

                        print("Removing playlist: " + loaded_data[playlist_id]['Playlist_Title'])

                        deleted = [loaded_data[playlist_id]['Playlist_Title'], "Playlist"]
                        
                        loaded_data.pop(playlist_id)

                    else:

                        try:
                            songID = int(songID) - 1
                            if (songID < 0):
                                #print("SongID below zero, making it equals: 0")
                                songID = 0
                            elif (songID >= len(ReadMusicData()[playlist_id]['Playlist_Info'])):
                                songID = len(ReadMusicData()[playlist_id]['Playlist_Info']) - 1
                                #print("SongID above len of ReadMusicData(), making it equals: " + str(songID))
                            #print("STR to INT convertation, returned SongID:" + str(songID))
                        except:
                            print("SongID converting to INT failed, processing as string...")

                        if (type(songID) == int):
                            if (songID >= len(loaded_data[playlist_id]['Playlist_Info'])):
                                songID = len(loaded_data[playlist_id]['Playlist_Info'])
                            elif (songID < 0):
                                songID = 0

                            mp3file = loaded_data[playlist_id]['Playlist_Info'][songID]['FileName']

                            deleted = [loaded_data[playlist_id]['Playlist_Info'][songID]['SongTitle'], "Song"]

                            loaded_data[playlist_id]['Playlist_Info'].pop(songID)

                            

                            os.remove("music\\" + mp3file)

                            print("Removing track: " + mp3file + " - " + deleted[0])

                            if (len(loaded_data[playlist_id]['Playlist_Info']) == 0):
                                loaded_data.pop(playlist_id)
                                print("Removing playlist, because now it is empty.")

                        else:

                            print("\n------ [!] ERROR: MusicData: songID is not INTEGER [!] ------\n")

                            return "Необходимо указать ID песни."
                else:
                    
                    print("Trying to remove playlist, but whole JSON file is empty : 293")
                    return "Указанный плейлист не существует."

            with open('music\MusicData.json', 'w') as outfile:

                json.dump(loaded_data, outfile)

                outfile.close()

            print("\n------ [X] Cleaned MusicData entry [X] ------\n")

            if (deleted[1] == "Playlist"):
                return "Плейлист удалён: " + deleted[0]
            elif (deleted[1] == "Song"):
                return "Трек удалён: " + deleted[0]
            else:
                return "Unexpected error in MusicModule: 3544"

        except Exception as error:
            print("RemoveMusicDataEntry ERROR: 368 ")
            print(error)
            return "Нельзя удалить трек, который сейчас играет." #Нельзя удалить трек, который сейчас играет.
    else:
        print(file_list)
        print("MusicData.JSON is not found.")
        return "Медиатека пуста."


def TryConvertInt(parameter):
        #print("STR to INT convertation, entered value:" + str(parameter))
        parameter = int(parameter) - 1
        if (parameter < 0):
            #print("Value below zero, making it equals: 0")
            parameter = 0
        elif (parameter >= len(ReadMusicData())):
            parameter = len(ReadMusicData()) - 1
            #print("Value above len of ReadMusicData(), making it equals: " + str(parameter))
        #print("STR to INT convertation, returned value:" + str(parameter))
        return parameter

def DrawPlaylist(playlist_id=0):

    if (ReadMusicData() == "Undefined"):
        print("Music play error: playlist is empty : 101")
        return 'Плейлистов не существует. Команда поиска и добавления треков описана в: "!music"', "UndefinedPlaylistID"
    
    else:
        try:
            playlist_id = TryConvertInt(playlist_id)
        except:
            print("Converted to int argument failed, continue processing as a string: music module 196")

        if (type(playlist_id) == int):

            playlist_id = playlist_id

            if (playlist_id < 0):
                playlist_id = 0
            elif (playlist_id >= len(ReadMusicData())):
                playlist_id = len(ReadMusicData()) - 1

            result_playlist_answer = "[" + str(playlist_id+1) + "]" + ReadMusicData()[playlist_id]['Playlist_Title'] + "\n\n"
            y = 0
            for cur_song in ReadMusicData()[playlist_id]['Playlist_Info']:
                result_playlist_answer = result_playlist_answer + "  " + str(y+1) + ". " + ReadMusicData()[playlist_id]['Playlist_Info'][y]['SongTitle'] + " | " + ReadMusicData()[playlist_id]['Playlist_Info'][y]['Duration'] + "\n"
                y = y + 1
            result_playlist_answer = result_playlist_answer + "\n"

            return result_playlist_answer, playlist_id

        elif(type(playlist_id) == str):
            x = 0
            FindExistingPlaylist = False
            for cur_playlist in ReadMusicData():
                if (ReadMusicData()[x]['Playlist_Title'] == playlist_id):

                    result_playlist_answer = "[" + str(x+1) + "]" + ReadMusicData()[x]['Playlist_Title'] + "\n\n"
                    y = 0
                    for cur_song in ReadMusicData()[x]['Playlist_Info']:
                        result_playlist_answer = result_playlist_answer + "  " + str(y+1) + ". " + ReadMusicData()[x]['Playlist_Info'][y]['SongTitle'] + " | " + ReadMusicData()[x]['Playlist_Info'][y]['Duration'] + "\n"
                        y = y + 1
                    result_playlist_answer = result_playlist_answer + "\n"
                    FindExistingPlaylist = True

                    return result_playlist_answer, x
                else:
                    x = x + 1

            if (FindExistingPlaylist == False):
                return "Указанный плейлист не найден.", "UndefinedPlaylistID"
        
        else:
            print("Arg type equals NoneType: music module 197")
            result_playlist_answer = ""
            x = 0
            for cur_playlist_info in ReadMusicData():
                result_playlist_answer = result_playlist_answer + "[" + str(x+1) + "]" + ReadMusicData()[x]['Playlist_Title'] + "\n\n"
                y = 0
                for cur_song in ReadMusicData()[x]['Playlist_Info']:
                    result_playlist_answer = result_playlist_answer + "  " + str(y+1) + ". " + ReadMusicData()[x]['Playlist_Info'][y]['SongTitle'] + " | " + ReadMusicData()[x]['Playlist_Info'][y]['Duration'] + "\n"
                    y = y + 1
                x = x + 1
                result_playlist_answer = result_playlist_answer + "\n"

            return 'Плейлистов:  ' + str(len(ReadMusicData())) + "\n\n" + result_playlist_answer, "UndefinedPlaylistID"
        


        #result_playlist_answer = "[" + str(playlist_id+1) + "]" + ReadMusicData()[playlist_id]['Playlist_Title'] + "\n\n"
        #y = 0
        #for cur_song in ReadMusicData()[playlist_id]['Playlist_Info']:
        #    result_playlist_answer = result_playlist_answer + "  " + str(y+1) + ". " + ReadMusicData()[playlist_id]['Playlist_Info'][y]['SongTitle'] + "\n"
        #    y = y + 1
        #result_playlist_answer = result_playlist_answer + "\n"
        #return result_playlist_answer


#SoundSearch("hotline miami 2 blizzard", duration=5)
#MusicQueue()
#ClearMusicData()
#print(ReadMusicData())
#print(len(ReadMusicData()))

#print(ReadMusicData()[0]['Playlist_Info'][2])

#print(ReadMusicData()[0]['Playlist_Info'][1]['FileName'][4])
#print(DrawPlaylist("4len")[1])
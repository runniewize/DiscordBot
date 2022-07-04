from discord.ext import commands
import discord
from CDN import *
# from SteamModule import first_sale, second_sale
import random
from TwitchModule import SetTwitchStreamer
import random

from MusicModule import SoundSearch, ReadMusicData, RemoveMusicDataEntry, DrawPlaylist


client = commands.Bot(command_prefix='!')
client.remove_command("help")

discord_token = "OTYxNDA2ODMyMDg4MzQyNTk4.Yk4h4g.4imI80kVZMCmjpdqGbq572ZZ3dY"

tryFind = False
userTryingFind = None

tryFindTwitch = False
userTryingFindTwitch = None

tryFindMusic = False
userTryingFindMusic = None
playlist_id = None
music_duration = None

voiceChannel = None

cur_music_queue = 0

@client.event
async def on_ready():
           print("Bot connected.")


@client.command()
async def soundfind(msg, params="Playlist", media_duration=5):
    #await msg.channel.send("total: " + params + " " + str(media_duration)) 
    global playlist_id
    playlist_id = params
    global tryFindMusic
    tryFindMusic = True
    global userTryingFindMusic
    userTryingFindMusic = msg.author
    global music_duration
    music_duration = media_duration

    print("playlist_params are " + str(params))
    print("media duration is " + str(media_duration))
    print("][][")

    await msg.channel.send('Waiting for input audio title.')

    #await msg.channel.send('Обрабатываю запрос, через пару секунд медиа появится в плейлисте.')
    #SoundSearch(params, media_duration)
    #await msg.channel.send(ReadMusicData()[len(ReadMusicData())-1]['YouTube'])

def PlayMusic(voice_channel, playlist=0, SongIDValue=None, PlayAllPlaylists=False):
    print("\n----------------- PlayMusic(): trying to start --------------------\n")

    global cur_music_queue
    if (str(SongIDValue) == "None"):
        print("Music ID is not set, playing playlist first song.")
        cur_music_queue = 0
    else:
        print("Music ID is set, playing playlist song with ID (+1): " + str(SongIDValue+1))
        cur_music_queue = SongIDValue

    if (cur_music_queue >= len(ReadMusicData()[playlist]['Playlist_Info'])):
        if (PlayAllPlaylists == False):
            print("Playlist is over, queue set to zero - repeating playlist.")
            cur_music_queue = 0
        else:
            playlist = playlist + 1
            if (playlist >= len(ReadMusicData())):
                playlist = 0
                cur_music_queue = 0
                print("All playlists are over, repeating all playlists again.")
            else:
                print("Playlist is over, queue set to zero - going to next playlist.")
                cur_music_queue = 0

    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(source="music\\song" + ReadMusicData()[playlist]['Playlist_Info'][cur_music_queue]['FileName'][4] + ".mp3"))

    try:  
        voice_channel.play(source=source, after= lambda e: PlayMusic(voice_channel, playlist, cur_music_queue, PlayAllPlaylists))
        print("MusicQueue is " + str(cur_music_queue) + ", current play: " + ReadMusicData()[playlist]['Playlist_Info'][cur_music_queue]['FileName'] + " - " + ReadMusicData()[playlist]['Playlist_Info'][cur_music_queue]['SongTitle'])
        cur_music_queue = cur_music_queue + 1

    except:
        print("Not in voice channel - loading on, must start soon | Another exception: 57")


    print("\n----------------- Current PlayMusic(): COMPLETE -------------------\n")
    

async def TryConnect(msg_parameter):
        channel = msg_parameter.author.voice.channel
        try:
            print("Trying to disconnect: 90")
            await msg_parameter.voice_client.disconnect()
        except:
            print("Disconnect failed.")

        try:
            print("Trying to connect: 92")
            await channel.connect()
            print("Connected to voice channel.")
        except:
            print("Connection failed: 96")

def ChooseEqualizerGif():
    equalizer_id = random.randrange(1, 7)
    print("Equalizer id is " + str(equalizer_id))
    equalizer = "equalizer_" + str(equalizer_id) + ".gif"
    return equalizer

@client.command()
async def playlist(msg, args=None, SongIDToPlay=0):   

    ReturnedPlaylistID = DrawPlaylist(args)

    await msg.channel.send(ReturnedPlaylistID[0], file=discord.File(ChooseEqualizerGif()))

    if (type(ReturnedPlaylistID[1]) == str):
        print("Playlist id is not set : 121")
    else:

        try:
            await TryConnect(msg)
        except:
            print("Unable to connect: TryConnect()")

        SongIDToPlay = SongIDToPlay - 1

        if (SongIDToPlay < 0):
            SongIDToPlay = 0
            print("Song ID value under zero, setting to zero.")

        elif (SongIDToPlay >= len(ReadMusicData()[ReturnedPlaylistID[1]]['Playlist_Info'])):
            SongIDToPlay = len(ReadMusicData()[ReturnedPlaylistID[1]]['Playlist_Info']) - 1
            print("Song ID value above len of ReadMusicData(), setting to max value: " + str(len(ReadMusicData()[ReturnedPlaylistID[1]]['Playlist_Info']) - 1))

        else:
            print("Song ID value in normal range and equals: " + str(SongIDToPlay))

        server = msg.message.guild
        voice_channel = server.voice_client

        PlayMusic(voice_channel, ReturnedPlaylistID[1], SongIDToPlay)


@client.command()
async def play(msg):   

    ReturnedPlaylistID = DrawPlaylist(None)
    await msg.channel.send(ReturnedPlaylistID[0], file=discord.File(ChooseEqualizerGif()))

    try:
        await TryConnect(msg)
    except:
        print("Unable to connect: TryConnect()")

    server = msg.message.guild
    voice_channel = server.voice_client

    PlayMusic(voice_channel, PlayAllPlaylists=True)


@client.command()
async def remove(msg, playlist=None, songID=None):
    if (playlist == None):   
        await msg.channel.send('You must choose playlist that you want to remove.')

    elif (playlist == "all"):
        try:
            print("Trying to disconnect: 90")
            await msg.voice_client.disconnect()
            await msg.channel.send("You must leave voice channel to clear media.")
        except:
            print("Disconnect failed.")
            await msg.channel.send(RemoveMusicDataEntry("all", None))

    else:
        if (songID == None):

            await msg.channel.send(RemoveMusicDataEntry(playlist, "all"))
        else:

            await msg.channel.send(RemoveMusicDataEntry(playlist, songID))

@client.command()
async def music(msg):    


    await msg.channel.send("Music:" + "\n"
    + "!music - commands" + "\n"+ "\n"
    + "!soundfind playlist duration - find track and add to playlist. Instead 'playlist' (optional) you need select playlist title: if it exists - new track will be added, if not exist, new playlist will be created. You can't use spaces in playlist title" + "\n" + "duration (optional) - sets maximum media duration, if you set it to 3, you will find track not longer then 3 minutes (5 minutes by default). Do not set higher then 10." + "\n\nExample:\n" + "!soundfind playlist 2" + "\n" + "Searching is going through YouTube." + "\n"
    + "\n" + "!playlist - check all playlists." + "\n"+ "\n"
    + "!play - play all playlists from first. You must be in voice channel." + "\n"+ "\n"
    + "!playlist 2 - play and repeat second playlist" + "\n"+ "\n"
    + "!playlist 2 3 - play third track of second playlist. When playlist is over, it will repeat." + "\n"+ "\n"
    + "!remove 2 - remove second playlist." + "\n"+ "\n"
    + "!remove 2 5 - remove fifth track from second playlist." + "\n"+ "\n"
    + "!remove all - remove all media." + "\n"+ "\n"

    + "!leave - leave voice channel and stop playing audio." + "\n"
    + "",
    file=discord.File('music_gif.gif')
    ) 

@client.command()   
async def leave(msg):
    try:
        await msg.voice_client.disconnect()
        await msg.channel.send("Отключение от каналa.")
    except:
        print("Can't leave channels: 118")










@client.command()   
async def help(msg):
    await msg.channel.send("Commands:" + "\n"
    + "!music - music" + "\n"  
    + "!watch - find movies and serials" + "\n" 
    + "!sales - Steam sales of the day" + "\n" 
    + "!twitch - find Twitch streamer" + "\n" 
    + "!clear - clear chat" + "\n" 


    + "!roll - roll random number (1-100)" + "\n", 
    
    file= discord.File("bot_logo.jpg"))

@client.command()   
async def roll(msg):
    rng = random.randint(1, 100)
    await msg.channel.send(str(msg.author) + " rolls: " + "\n" + "[- " + str(rng) + " -]")     

@client.command()   
async def twitch(msg):  
    await msg.channel.send("Who we are looking for?")  
    global tryFindTwitch
    tryFindTwitch = True
    global userTryingFindTwitch
    userTryingFindTwitch = msg.author

@client.command()   
async def sales(msg):  
    await msg.channel.send("Steam sales:")     
    await msg.channel.send("[ " + str(first_sale[0]) + " ]" + "\n" + str(first_sale[1]).replace("{","").replace("'",""))
    await msg.channel.send("[ " + str(second_sale[0]) + " ]" + "\n" + str(second_sale[1]).replace("{","").replace("'",""))
    await msg.channel.send("More: " + "\n" + "https://steamdb.info/sales/history/")        

           
@client.command()   
async def watch(msg):
    await msg.channel.send("Waiting for title input.")
    global tryFind
    tryFind = True
    global userTryingFind
    userTryingFind = msg.author

@client.command()   
async def clear(msg, args=None):
    print("Clear func starts...")

    try:
        args = int(args)
        print("Converted args to int.")
    except:
        print("Converting args to int failed, processing as a string.")

    if (type(args) == str and args == "all"):
        print("Purge all.")
        await msg.channel.purge(limit=100000)
        await msg.channel.send("Chat was cleaned.")
        print("Cleared func complete.")

    elif (type(args) == str):
        print("Purge 100.")
        await msg.channel.purge(limit=100)
        await msg.channel.send("Chat was cleaned.")
        print("Cleared func complete.")

    else:
        print("Purge args.")
        await msg.channel.purge(limit=args)
        await msg.channel.send("Chat was cleaned.")
        print("Cleared func complete.")


@client.event
async def on_message(msg):
    #print("New message income: " + "'" +  msg.content + "'" + " from " + msg.author.name)
    global tryFind
    global userTryingFind

    global tryFindTwitch
    global userTryingFindTwitch

    global tryFindMusic
    global userTryingFindTwitch
    global playlist_id
    global music_duration


    if (msg.author.name != "AcidHouse" and tryFind == True and userTryingFind == msg.author):

        #print("Trying to search a film " + msg.content +  " by" + msg.author.name)

        finded_results = GetFilm(msg.content)

        result_count = len(finded_results[0])
        
        cur_result_count = 0
        cur_result_titles = []

        await msg.channel.send("Seaching results:") 

        while (cur_result_count != result_count):
            cur_result_titles.append(str(finded_results[0][cur_result_count]).strip('[]') + "\n" + finded_results[2][cur_result_count] + "\n" + finded_results[1][cur_result_count] + "\n" + finded_results[3][cur_result_count])
            result_text = "\n" + str(cur_result_titles).strip('[]').replace('\\n', '\n').replace("'", "").replace(",", "")
            await msg.channel.send(result_text) 
            result_text = None
            cur_result_titles = []
            cur_result_count = cur_result_count + 1
        
        tryFind = False
        userTryingFind = None

    if (msg.author.name != "AcidHouse" and tryFindTwitch == True and userTryingFindTwitch == msg.author):

        twitchStreamer = msg.content
        await msg.channel.send(SetTwitchStreamer(twitchStreamer))

        tryFindTwitch = False
        userTryingFindTwitch = None

    if (msg.author.name != "AcidHouse" and tryFindMusic == True and userTryingFindMusic == msg.author):

        music_title = msg.content

        await msg.channel.send('Media will appear in playlists in a few seconds.')
        print("\n----------------- Soundfind: Trying to start -------------------\n")
        finded_yt_link = SoundSearch(music_title, playlist_id, music_duration)
        #print(finded_yt_link)
        await msg.channel.send(str(finded_yt_link))

        tryFindMusic = False
        userTryingFindTwitch = None
        playlist_id = "Playlist"
            
        

    await client.process_commands(msg)


client.run(discord_token)
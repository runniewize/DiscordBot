from ast import Index
import requests

cdn_token = "afA1zxbg7NyZTBFIpCGhIzUrAAtk8AvA"

def GetFilm(film_title):

    #reqs = requests.get("https://videocdn.tv/api/movies?api_token=" + cdn_token + "&title=" + film_title).json()
    reqs = requests.get("https://videocdn.tv/api/short?api_token=" + cdn_token + "&title=" + film_title).json()

    results_count = len(reqs["data"])
    titles = []
    pathes = []
    imdb = []
    title_type = []

    x = 0
    while x < results_count:

        replacing_done = False

        #film_prepath = reqs["data"][x]["media"][0]["path"]
        film_prepath = reqs["data"][x]["iframe_src"]

        #print("curfilm is " + reqs["data"][x]["ru_title"] + " [" + reqs["data"][x]["released"][0] + reqs["data"][x]["released"][1] + reqs["data"][x]["released"][2] + reqs["data"][x]["released"][3] + "] ")

        #y = 1

        #while (replacing_done != True):

        #    film_path = film_prepath[:-y]

            #print(film_path)

        #    if (film_path.find("?") == -1):

        #        replacing_done = True

        #    y = y + 1

        titles.append(reqs["data"][x]["title"] + " [" + reqs["data"][x]["year"][0] + reqs["data"][x]["year"][1] + reqs["data"][x]["year"][2] + reqs["data"][x]["year"][3] + "] ")
        #titles.append(reqs["data"][x]["ru_title"] + " [" + reqs["data"][x]["released"][0] + reqs["data"][x]["released"][1] + reqs["data"][x]["released"][2] + reqs["data"][x]["released"][3] + "] ")
        pathes.append("https:" + film_prepath)
        imdb.append("https://www.imdb.com/title/" + reqs["data"][x]["imdb_id"])
        title_type.append(reqs["data"][x]["type"])
        
        x = x + 1

    x = 0
    while (x != len(title_type)):
        if (title_type[x] == "movie"):
            title_type[x] = "Фильм"
        elif (title_type[x] == "serial"):
            title_type[x] = "Сериал"
        else:
            title_type[x] = "UNDEFINED" 
        x = x + 1
        

    #print(reqs)
    #print(title_type)
    #print(titles)
    #print(pathes)
    #print("done")

    
    

    return(WatchSortDate(titles, pathes, title_type, imdb))


def WatchSortDate(titles, pathes, title_type, imdb):
    x = 0
    dates = []
    titles_sorted = []
    titles_id = []
    pathes_sorted = []
    imdb_sorted = []
    title_type_sorted = []
    while (x != len(titles)):

        index = titles[x].find("[")
        dates.append(titles[x][index + 1] + titles[x][index + 2] + titles[x][index + 3] + titles[x][index + 4])

        x = x + 1

    dates = sorted(dates)

    x = 0
    while (x != len(titles)): #сработает 7 итераций
        #print(str(x+1) + " итерация цикла WHILE")
        id = 0
        for y in titles: #я начинаю перебирать все тайтлы (тоже 7 раз)
            #print("y is " + y + " and dates[x] is " + dates[x])

            if (str(dates[x]) in str(y) and y not in titles_sorted): #если в текущим тайтле (от 1 до 7) я смог найти совпадение даты,
                titles_sorted.append(y) #добавляю
                titles_id.append(id)
                pathes_sorted.append(pathes[id])
                imdb_sorted.append(imdb[id])
                title_type_sorted.append(title_type[id])
                #print("found match")
            #else:
                #print("not found match")
            id = id + 1    
        x = x + 1
    

    #print(str(len(titles)) +  " orig vs sorted " + str(len(titles_sorted)))
    #print("ids are " + str(titles_id))
    #print("dates are " + str(len(dates)) + " : " + str(dates))
    #print("\n\n" + str(titles))
    #print("imdbs origs are :" + str(imdb))
    #print("\n\n" + str(titles_sorted))
    #print("imdbs sorted :" + str(imdb_sorted))
    #print(title_type_sorted)
    return (titles_sorted, pathes_sorted, title_type_sorted, imdb_sorted)

#GetFilm("Наруто")
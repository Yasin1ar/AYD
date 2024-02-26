'''Alpha YouTube Downloader is a python script for downloading audios and and videos from YouTube,
You Provide The URL, and AYD serves you with the desired file :) .
pros:
    - You can download videos and musics for free, no charge, no ad, no disturbance
    - safe and trusted, you can observe and investigate the whole code, nothing is hidden from your eyes
    - acceptably fast, if your internet connection is not slow as ..., turtle! 
    
cons:
    - you can't chose the resolution :(, all the videos are available as 720p
    - not visually perfect, a nice GUI would be better I don't want to argue
    - probably not very user-friendly, especially for those who don't use CLI programs very often
    - you need python Installed, plus all of its dependencies, which I think is the biggest cons so far :(
        
    overall I think it is still useful, not for everyone, but for those like me that already has python installed, doesn't care about nice UI or using CLI programs,
    and doesn't want to pay, see ads, or risk for downloading a video.

    but that doesn't mean I don't have plans for making it better, but I could use some help :>>
    , would be very cool if you guys help me, I would really appreciate, thank for helping, or even using AYD :) '''

# --- Importing dependencies ---
from pytube import YouTube, exceptions, request
import os
# for error handling
from http.client import RemoteDisconnected, IncompleteRead 
from urllib.error import URLError

# If there's not a folder with desired name, create a new one
def file_path(name="AYD"):
    """creates a folder with provided parameter name if does not exist, then returns the name"""
    if not name in os.listdir(os.getcwd()):
        os.mkdir(name)
    return name

# specifies the chunk size
request.default_range_size = 1048576

def completed(artist, song_name):
    """gets called after the successful download"""
    print(f"\n  Downloaded successfully\n enjoy :)\n")


def progress_bar(self, chunk, bytes_remaining):
    """shows progress bar"""
    print(f"{round(bytes_remaining*0.000001)} MB remaining")

def check_name(file_name):
    """checks the name for possible characters in name that unsupported and raise error,
    if found, replaces with whitespace, then returns the corrected name"""
    for i in file_name:
        if i in [":", "|", "<", ">", "؟", "'", '"', "?", "/", "*"]:
            file_name = file_name.replace(i, " ")
    return file_name

def title(url):
    """returns the title in desired/ideal format"""
    title = f"{url.author} - {url.title}"
    return title

def file_name(url, audio=False):
    """returns the name of the file after passing the checking process, if the file is video it returns the default file name,
    if the file is audio, it appends the ".mp3" suffix to the desired file name"""
    if audio:
        file_name = title(url)
        file_name = check_name(file_name)
        return file_name + ".mp3"

    file_name = url.streams.first().default_filename
    file_name = check_name(file_name)

    return file_name

def yt_url():
    """get's the YouTube video url from the user and creates a YouTube object"""
    try:
        link = input("\nPlease enter the youtube link : ")
        print("please wait ...")
        url = YouTube(
            link, on_progress_callback=progress_bar, on_complete_callback=completed
        )
        return url
    except exceptions.RegexMatchError:
        print("Please Enter a Valid YouTube link")
        return yt_url()

def max_abr(url):
    """finds and returns the highest quality audio"""
    try:
        aud = url.streams.filter(only_audio=True)
        abrs = set([i.abr for i in aud])
        abrs.discard(None)
        max_abr = max([int(i.replace("kbps", "")) for i in abrs])
        max_abr = f"{max_abr}kbps"
        return max_abr
    except Exception as Error:
        print(
            "Something went wrong when trying to find the highest quality audio!, Please re-run the program. ERROR DETAILS : ",
            Error,
        )
        exit()

def download_video(url,custom_res:str):
    """Downloads the video"""
    print("Downloading ... ")
    url.streams.filter(res=custom_res).first().download(
        output_path=file_path(), filename=file_name(url)
    )

def download_audio(url):
    """Downloads the audio"""
    print("Downloading ... ")
    url.streams.filter(abr=max_abr(url)).first().download(
        output_path=file_path(), filename=file_name(url, audio=True)
    )


def download_type(fn):
    """a recursion function, provides the option for the user to chose between video or only audio, it calls itself until gets a valid input,
    then returns the chose"""
    print(f"\n'{fn}' found,")
    dl_type = input(
        "Do You Want the video or only the audio?\n 1 -> Video\n 2 -> Audio\n  $: "
    )
    if not dl_type.strip() in ["1", "2"]:
        return download_type(fn)
    return dl_type

# returns the selected res (140p, 360p, ...)
def select_resolution(url) -> str:
    print("Getting resolutions ... ")

    resolutions = []

    i = 0;
    for stream in url.streams.filter(mime_type="video/mp4"):
        if not stream.resolution in resolutions:
            print(f"{i}. {stream.resolution}")
            resolutions.append(stream.resolution)
            i+=1

    print("Chose resolution: ")
    custom_res = int(input(">> "))

    return resolutions[custom_res]


def download(dl_type:str, url):
    dl_type_name = "Video" if dl_type=="1" else "Audio"

    try:
        """calls the correct download function based on the user chose"""
        if dl_type == "1":
            download_video(url,select_resolution(url))
        else:
            download_audio(url)

    except exceptions.AgeRestrictedError:
        print(f"Age Restricted!, can not download, please try with another {dl_type_name} :(")
        exit()
    except Exception as Error:
        print(
            f"Something went wrong when trying to downloading the {dl_type_name}!, Please re-run the program. ERROR DETAILS : ",
            Error,
        )
        exit()

# - - - Main - - -
if __name__ == "__main__":
    """The Entry point of the program"""
    while True:
        try:
            url = yt_url()
            fn = title(url)
            dl_type = download_type(fn)
            download(dl_type, url)
            finish = input(
                f"'{fn}' Downloaded successfully!, press 'q' for exit or anything else to continue : "
            )
            if finish.strip().lower() == "q":
                print("Bye-Bye!")
                exit()
        except RemoteDisconnected:
            print("NetWork Error!, please check your network and try again")
            exit()
        except IncompleteRead:
            print("NetWork Error!, please check your network and try again")
            exit()
        except URLError:
            print("NetWork Error!, please check your network and try again")
            exit()
        except Exception as Error:
            print(
                """Something went wrong during the run!, please check your connection and retry, if it happened again
                Please open an issue in https://github.com/Yasin1ar/Alpha-Youtube-Downloader/issues,
                thanks for your contribute to improvement of this program! :)\nERROR DETAILS : """,
                Error,
            )
            exit()

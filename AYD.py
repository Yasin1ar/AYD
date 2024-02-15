from pytube import YouTube, exceptions, request
link = input("Please enter the youtube link : ")

request.default_range_size = 1048576
def completed(artist, song_name):
        print(f"\n  Downloaded successfully\n enjoy :)\n")

def progress_bar(self, chunk, bytes_remaining):
    print(f"{round(bytes_remaining*0.000001)} MB remaining")
# Making a YouTube Object to continue
url = YouTube(link,on_progress_callback=progress_bar,on_complete_callback=completed)

file = input(f'Found " {url.title} ", Do You Want the video or only the audio?\n 1 -> Video\n 2 -> Audio\n  $: ')

file = file.strip()

try:
    def get_video(url):
        
        url.streams.filter(progressive=True).get_highest_resolution().download()
    def get_audio(url):
        # a function to find the highest quality among all of them
        def get_max_abr():
            # making a streams object with youtube object, to use the filter method that returns a list of audios
            aud = url.streams.filter(only_audio=True)
            abrs = set([i.abr for i in aud])
            abrs.discard(None)
            max_abr = max([int(i.replace("kbps","")) for i in abrs]) 
            max_abr = f"{max_abr}kbps"
            return max_abr

        # an optional function to name the downloaded file + ".mp3" suffix that is more convenient than possible ".webm" suffix
        def file_name(link):
            title = url.title
            author = url.author
            return author + " - " + title + ".mp3"

        # finally, downloading the desired Music/Audio
        url.streams.filter(abr=get_max_abr()).first().download(filename=file_name(link))


except exceptions.AgeRestrictedError:
    print("Age Restricted!")


if file == "1":
    get_video(url)
elif file == "2":
    get_audio(url)
else:
    print("NOT correct!")
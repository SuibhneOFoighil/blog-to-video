import sys
from unstructured.partition.auto import partition
from generate import description, narrative, visuals
from video import Video

def main():
    
    # Parse the first command-line argument as the file name
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        print("File name:", file_name)
    else:
        print("No file name provided")
        return

    #load blog document into chunks
    path = f"blogs/{file_name}"
    with open(path, 'rb') as fl:
        chunks = partition(file=fl)

    chunks = chunks[:5]

    #generate visual description of each chunk
    # descriptions = description(chunks)

    # #generate audio narrative of each chunk
    # narrative(chunks)

    #generate video from audio and visual descriptions
    descriptions = []
    for i, chunk in enumerate(chunks):
        with open(f"descriptions/{i}.txt", "r") as fl:
            descriptions.append(fl.read())
    visuals(descriptions)

    # #make video
    # video = Video(visuals, audio)

    # #export video as mp4
    # video.export(f"videos/{file_name}.mp4")

if __name__ == "__main__":
    main()
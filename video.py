class Video:
    def __init__(self, visuals, audio):
        self.visuals = visuals
        self.audio = audio

    def export(self, file_name):
        print("Exporting video to", file_name)
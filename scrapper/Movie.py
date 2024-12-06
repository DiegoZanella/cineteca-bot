class Movie:
    def __init__(self, title, duration, director, description, times):
        self.title = title
        self.duration = duration
        self.director = director
        self.description = description
        self.times = times

    def get_title(self):
        return self.title

    def get_duration(self):
        return self.duration

    def get_director(self):
        return self.director

    def get_description(self):
        return self.description

    def get_times(self):
        return self.times

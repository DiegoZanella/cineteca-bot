class Movie:
    def __init__(self, film_id, title, duration, director, description, times, img_link):
        self.film_id = film_id
        self.title = title
        self.duration = duration
        self.director = director
        self.description = description
        self.times = times
        self.img_link = img_link

    def __str__(self):
        return f"Title: {self.title}\nDuration: {self.duration}\nDirector: {self.director}\nDescription: {self.description}\nTimes: {self.times}\nImg Link: {self.img_link}"

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

    def get_img_link(self):
        return self.img_link

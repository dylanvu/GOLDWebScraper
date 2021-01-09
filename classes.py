class Course:
    def __init__(self, name, department, weekday, hour, instructor, availability, max):
        self.name = name
        self.department = department
        self.weekday = weekday
        self.hour = hour
        self.instructor = instructor
        self.availability = availability
        self.max = max


class Department:
    def __init__(self, name, courses):
        self.name = name
        self.courses = courses

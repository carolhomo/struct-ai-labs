class Lesson:
    def __init__(self, subject, time, date, group, teacher, classroom):
        self.subject = subject
        self.time = time
        self.date = date
        self.group = group
        self.teacher = teacher
        self.classroom = classroom


class Group:
    def __init__(self, name):
        self.name = name
        self.schedule = []


class Teacher:
    def __init__(self, name):
        self.name = name
        self.schedule = []


class Classroom:
    def __init__(self, number):
        self.number = number
        self.schedule = []


class Schedule:
    def __init__(self):
        self.groups = {}
        self.teachers = {}
        self.classrooms = {}
        self.lessons = []

    def add_group(self, group_name):
        self.groups[group_name] = Group(group_name)

    def add_teacher(self, teacher_name):
        self.teachers[teacher_name] = Teacher(teacher_name)

    def add_classroom(self, classroom_number):
        self.classrooms[classroom_number] = Classroom(classroom_number)

    def add_lesson(self, subject, time, date, group_name, teacher_name, classroom_number):
        lesson = Lesson(subject, time, date, group_name, teacher_name, classroom_number)
        self.lessons.append(lesson)
        self.groups[group_name].schedule.append(lesson)
        self.teachers[teacher_name].schedule.append(lesson)
        self.classrooms[classroom_number].schedule.append(lesson)

    def remove_lesson(self, subject, time, date, group_name):
        for lesson in self.lessons:
            if (
                    lesson.subject == subject and lesson.time == time and lesson.date == date and lesson.group == group_name):
                self.lessons.remove(lesson)
                self.groups[group_name].schedule.remove(lesson)
                self.teachers[lesson.teacher].schedule.remove(lesson)
                self.classrooms[lesson.classroom].schedule.remove(lesson)
                break

    def find_lessons(self, **kwargs):
        found_lessons = []
        for lesson in self.lessons:
            match = True
            for key, value in kwargs.items():
                if getattr(lesson, key) != value:
                    match = False
                    break
            if match:
                found_lessons.append(lesson)
        return found_lessons

    def print_schedule(self, entity_type, name):
        schedule = []
        if entity_type == 'group':
            schedule = self.groups[name].schedule
        elif entity_type == 'teacher':
            schedule = self.teachers[name].schedule
        elif entity_type == 'classroom':
            schedule = self.classrooms[name].schedule

        for lesson in schedule:
            print(f"{lesson.subject} at {lesson.time} on {lesson.date} in {lesson.classroom}")

    def update_lesson(self, old_subject, old_time, old_date, group_name, new_subject=None, new_time=None, new_date=None,
                      new_classroom=None):
        lessons = self.find_lessons(subject=old_subject, time=old_time, date=old_date, group=group_name)
        if lessons:
            lesson = lessons[0]
            if new_subject:
                lesson.subject = new_subject
            if new_time:
                lesson.time = new_time
            if new_date:
                lesson.date = new_date
            if new_classroom:
                self.classrooms[lesson.classroom].schedule.remove(lesson)
                lesson.classroom = new_classroom
                self.classrooms[new_classroom].schedule.append(lesson)

    def analyze_data(self):
        group_load = {group: len(self.groups[group].schedule) for group in self.groups}
        teacher_load = {teacher: len(self.teachers[teacher].schedule) for teacher in self.teachers}
        classroom_load = {classroom: len(self.classrooms[classroom].schedule) for classroom in self.classrooms}

        free_classrooms = [classroom for classroom, load in classroom_load.items() if load == 0]

        return {
            "group_load": group_load,
            "teacher_load": teacher_load,
            "free_classrooms": free_classrooms
        }

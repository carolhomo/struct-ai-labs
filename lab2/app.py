from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from schedule import *

app = FastAPI()


class LessonBase(BaseModel):
    subject: str
    time: str
    date: str
    group: str
    teacher: str
    classroom: str


class LessonUpdate(BaseModel):
    old_subject: str
    old_time: str
    old_date: str
    group: str
    new_subject: Optional[str] = None
    new_time: Optional[str] = None
    new_date: Optional[str] = None
    new_classroom: Optional[str] = None


app = FastAPI()
schedule = Schedule()


@app.post("/groups/")
def add_group(name: str):
    schedule.add_group(name)
    return {"message": f"Group {name} added successfully"}


@app.post("/teachers/")
def add_teacher(name: str):
    schedule.add_teacher(name)
    return {"message": f"Teacher {name} added successfully"}


@app.post("/classrooms/")
def add_classroom(number: str):
    schedule.add_classroom(number)
    return {"message": f"Classroom {number} added successfully"}


@app.post("/lessons/")
def add_lesson(lesson: LessonBase):
    schedule.add_lesson(lesson.subject, lesson.time, lesson.date, lesson.group, lesson.teacher, lesson.classroom)
    return {"message": f"Lesson {lesson.subject} added successfully"}


@app.delete("/lessons/")
def remove_lesson(subject: str, time: str, date: str, group: str):
    schedule.remove_lesson(subject, time, date, group)
    return {"message": f"Lesson {subject} removed successfully"}


@app.get("/lessons/")
def find_lessons(subject: Optional[str] = None, time: Optional[str] = None, date: Optional[str] = None,
                 group: Optional[str] = None, teacher: Optional[str] = None, classroom: Optional[str] = None):
    lessons = schedule.find_lessons(subject=subject, time=time, date=date, group=group, teacher=teacher,
                                    classroom=classroom)
    return lessons


@app.get("/schedule/")
def get_schedule(entity_type: str, name: str):
    if entity_type not in ['group', 'teacher', 'classroom']:
        raise HTTPException(status_code=400, detail="Invalid entity type")
    schedule_data = []
    if entity_type == 'group':
        schedule_data = schedule.groups[name].schedule
    elif entity_type == 'teacher':
        schedule_data = schedule.teachers[name].schedule
    elif entity_type == 'classroom':
        schedule_data = schedule.classrooms[name].schedule
    return schedule_data


@app.put("/lessons/")
def update_lesson(lesson_update: LessonUpdate):
    schedule.update_lesson(
        lesson_update.old_subject, lesson_update.old_time, lesson_update.old_date, lesson_update.group,
        new_subject=lesson_update.new_subject, new_time=lesson_update.new_time, new_date=lesson_update.new_date,
        new_classroom=lesson_update.new_classroom
    )
    return {"message": "Lesson updated successfully"}


@app.get("/analysis/")
def analyze_data():
    analysis = schedule.analyze_data()
    return analysis


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

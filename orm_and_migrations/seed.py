from faker import Faker
from random import randint, choices, shuffle
from datetime import timedelta


from crud import create_record

fake = Faker()
grups = ["SP-3", "OT-2", "KM-5"]
subjects = ["Computer Science", "Mathematical Analysis", "Design and Technology", "Physics", "Machine Learning", "Data Management", "Philosofy"]

MAX_GRUPS = len(grups)
MAX_SUBJECTS = len(subjects)
MAX_STUDENTS = 40
MAX_TEACHERS = 4
MAX_MARKS = 20
MARK_VALUE = 100
DATE_DELTA = "-60d"


def get_groups():
    return [{"name": grup} for grup in grups]

def get_students():
    return [{"full_name": fake.name(), "group_id": randint(1,MAX_GRUPS)} 
            for _ in range(1, MAX_STUDENTS + 1)]

def get_teachers():
    return [{"full_name": fake.name()} for _ in range(1, MAX_TEACHERS + 1)]

def get_subjects():
    teachers_id = [id for id in range(1, MAX_TEACHERS + 1)]
    shuffle(teachers_id)
    if MAX_SUBJECTS > MAX_TEACHERS:
        teachers_id.extend(choices(teachers_id, k=MAX_SUBJECTS-MAX_TEACHERS))

    result = []
    for subject, teacher_id in zip(subjects, teachers_id):
        result.append({"name": subject, "teacher_id": teacher_id})
    return result

def get_marks():
    data = []
    for student_id in range(1, MAX_STUDENTS + 1):
        for _ in range(1, MAX_MARKS + 1):
            subject_id = randint(1, MAX_SUBJECTS)
            mark_date = fake.date_between(DATE_DELTA)
            if mark_date.weekday():
                mark_date = mark_date + timedelta(days=1)
            mark = randint(1, MARK_VALUE)
            data.append({"student_id": student_id, 
                         "mark": mark, 
                         "mark_date": mark_date, 
                         "subject_id": subject_id
                         })
    return data

def main():
    fake_grups = get_groups()
    for data in fake_grups:
        create_record("group", data)

    fake_students = get_students()
    for data in fake_students:
        create_record("student", data)

    fake_teachers = get_teachers()
    for data in fake_teachers:
        create_record("teacher", data)

    fake_subjects = get_subjects()
    for data in fake_subjects:
        create_record("subject", data)

    fake_marks = get_marks()
    for data in fake_marks:
        create_record("mark", data)


if __name__ == "__main__":
    main()

    


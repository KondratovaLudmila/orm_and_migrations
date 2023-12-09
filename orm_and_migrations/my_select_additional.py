from sqlalchemy import select, func, and_


from models import session, Student, Subject, Mark


def select_1(student_id: int, teacher_id: int):
    result = session\
        .query(func.round(func.avg(Mark.mark), 2).label("average_mark"))\
        .select_from(Mark)\
        .join(Subject)\
        .where(and_(Mark.student_id == student_id, 
                    Subject.teacher_id == teacher_id))\
        .all()
    
    return result


def select_2(group_id: int, subject_id: int):
    last_lesson = (select(func.max(Mark.mark_date).label("last_lesson"), 
                          Student.group_id, 
                          Mark.subject_id)\
                .select_from(Mark)\
                .join(Student)\
                .where(and_(Student.group_id == group_id, 
                            Mark.subject_id == subject_id))\
                .group_by(Student.group_id, 
                          Mark.subject_id)
                ).subquery()
    
    result = session\
        .query(Student.full_name.label("student"), Mark.mark, Mark.mark_date)\
        .select_from(Mark)\
        .join(Student)\
        .join(last_lesson, and_(Student.group_id == last_lesson.c.group_id, 
                                Mark.subject_id == last_lesson.c.subject_id,
                                Mark.mark_date == last_lesson.c.last_lesson))\
        .all()
    
    return result

if __name__ == "__main__":
    result = select_2(2, 5)
    print(result)
from sqlalchemy import select, func, desc, and_


from models import session, Group, Student, Teacher, Subject, Mark

def select_1():
    result = session.query(
                Student.id, 
                Student.full_name, 
                func.round(func.avg(Mark.mark), 2).label("average_mark"))\
            .select_from(Student)\
            .join(Mark)\
            .group_by(Student.id, Student.full_name)\
            .order_by(desc("average_mark"))\
            .limit(5)\
            .all()
    
    return result


def select_2(subject_id: int):
    result = session\
        .query(Student.id,
               Student.full_name,
               func.round(func.avg(Mark.mark), 2).label("average_mark"))\
        .select_from(Mark)\
        .join(Student)\
        .where(Mark.subject_id == subject_id)\
        .group_by(Student.id, Student.full_name)\
        .order_by(desc("average_mark"))\
        .limit(1)\
        .all()
    
    return result


def select_3(subject_id: int):
    result = session\
        .query(Group.name,
               func.round(func.avg(Mark.mark), 2).label("average_mark"))\
        .select_from(Mark)\
        .join(Student)\
        .join(Group)\
        .where(Mark.subject_id == subject_id)\
        .group_by(Group.name)\
        .all()
    
    return result


def select_4():
    result = session\
        .query(func.round(func.avg(Mark.mark), 2).label("average_mark"))\
        .select_from(Mark)\
        .all()
    
    return result


def select_5(teacher_id: int):
    result = session\
        .query(Subject.name)\
        .select_from(Subject)\
        .join(Teacher)\
        .where(Teacher.id == teacher_id)\
        .all()

    return result


def select_6(group_id: int):
    result = session\
        .query(Student.full_name)\
        .select_from(Student)\
        .where(Student.group_id == group_id)\
        .all()

    return result


def select_7(group_id: int, subject_id: int):
    result = session\
        .query(Student.full_name, Mark.mark, Mark.mark_date)\
        .select_from(Mark)\
        .join(Student)\
        .where(and_(Mark.subject_id == subject_id, 
                    Student.group_id == group_id))\
        .all()
    
    return result


def select_8(teacher_id: int):
    result = session\
        .query(func.round(func.avg(Mark.mark), 2).label("average_mark"))\
        .select_from(Mark)\
        .join(Subject)\
        .where(Subject.teacher_id == teacher_id)\
        .all()
    
    return result


def select_9(student_id: int):
    result = session\
        .query(Subject.name)\
        .select_from(Subject)\
        .join(Mark)\
        .where(Mark.student_id == student_id)\
        .group_by(Subject.name)\
        .all()
    
    return result


def select_10(student_id: int, teacher_id: int):
    result = session\
        .query(Subject.name)\
        .select_from(Subject)\
        .join(Mark)\
        .where(and_(Mark.student_id == student_id, Subject.teacher_id == teacher_id))\
        .group_by(Subject.name)\
        .all()
    
    return result

if __name__ == "__main__":
    result = select_2(3)
    print(result)

    
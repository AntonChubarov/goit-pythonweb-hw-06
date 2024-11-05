import datetime

from psycopg2._psycopg import Decimal
from sqlalchemy import func, desc, and_, or_
from sqlalchemy.orm import aliased
from models import Student, Group, Subject, Teacher, Grade
from session import session
from tabulate import tabulate

def select_1():
    """Find 5 students with the highest average grade across all subjects."""
    avg_grades = session.query(
        Grade.student_id,
        func.avg(Grade.grade).label('average_grade')
    ).group_by(Grade.student_id).subquery()

    top_students = session.query(
        Student.name,
        avg_grades.c.average_grade
    ).join(avg_grades, Student.id == avg_grades.c.student_id).order_by(
        desc(avg_grades.c.average_grade)
    ).limit(5).all()

    return top_students

def select_2(subject_id):
    """Find the student with the highest average grade in a specific subject."""
    top_student = session.query(
        Student.name,
        func.avg(Grade.grade).label('average_grade'),
        Subject.name.label('subject_name')
    ).join(Grade, Grade.student_id == Student.id)\
     .join(Subject, Subject.id == Grade.subject_id)\
     .filter(Grade.subject_id == subject_id)\
     .group_by(Student.id, Subject.name)\
     .order_by(desc(func.avg(Grade.grade)))\
     .first()

    if top_student:
        return [(top_student.name, float(top_student.average_grade), top_student.subject_name)]
    else:
        return []

def select_3(subject_id):
    """Find the average grade in groups for a specific subject."""
    group_averages = session.query(
        Group.name.label('group_name'),
        func.avg(Grade.grade).label('average_grade'),
        Subject.name.label('subject_name')
    ).join(Student, Student.group_id == Group.id)\
     .join(Grade, Grade.student_id == Student.id)\
     .join(Subject, Subject.id == Grade.subject_id)\
     .filter(Grade.subject_id == subject_id)\
     .group_by(Group.id, Subject.name)\
     .order_by(Group.name)\
     .all()

    results = [
        (group_name, float(average_grade), subject_name)
        for group_name, average_grade, subject_name in group_averages
    ]

    return results

def select_4():
    """Find the average grade in the intake (over the whole grades table)."""
    avg_grade = session.query(func.avg(Grade.grade)).scalar()
    return [float(avg_grade)]

def select_5(teacher_id):
    """Find which courses a specific teacher teaches."""
    courses = session.query(
        Teacher.name.label('teacher_name'),
        Subject.name.label('subject_name')
    ).join(Subject, Subject.teacher_id == Teacher.id)\
     .filter(Teacher.id == teacher_id)\
     .order_by(Subject.name)\
     .all()

    return courses

def select_6(group_id):
    """Find the list of students in a specific group."""
    students = session.query(
        Group.name.label('group_name'),
        Student.name.label('student_name')
    ).join(Student, Student.group_id == Group.id)\
     .filter(Group.id == group_id)\
     .order_by(Student.name)\
     .all()

    return students

def select_7(group_id, subject_id):
    """Find the grades of students in a specific group for a specific subject."""
    grades = session.query(
        Group.name.label('group_name'),
        Student.name.label('student_name'),
        Subject.name.label('subject_name'),
        Grade.grade,
        Grade.date_of.label('date')
    ).join(Student, Student.group_id == Group.id) \
        .join(Grade, Grade.student_id == Student.id) \
        .join(Subject, Subject.id == Grade.subject_id) \
        .filter(Group.id == group_id, Subject.id == subject_id) \
        .order_by(Student.name) \
        .all()

    return grades

def select_8(teacher_id):
    """Find the average grade that a specific teacher gives in their subjects."""
    avg_grades = session.query(
        Teacher.name.label('teacher_name'),
        Subject.name.label('subject_name'),
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject, Subject.teacher_id == Teacher.id) \
        .join(Grade, Grade.subject_id == Subject.id) \
        .filter(Teacher.id == teacher_id) \
        .group_by(Subject.id, Teacher.name) \
        .order_by(Subject.name) \
        .all()

    results = [
        (teacher_name, subject_name, float(average_grade))
        for teacher_name, subject_name, average_grade in avg_grades
    ]

    return results

def select_9(student_id):
    """Find the list of courses that a specific student attends."""
    courses = session.query(
        Student.name.label('student_name'),
        Subject.name.label('subject_name')
    ).join(Grade, Grade.student_id == Student.id) \
        .join(Subject, Subject.id == Grade.subject_id) \
        .filter(Student.id == student_id) \
        .distinct() \
        .order_by(Subject.name) \
        .all()

    return courses

def select_10(student_id, teacher_id):
    """List of courses that a specific teacher teaches to a specific student."""
    courses = session.query(
        Teacher.name.label('teacher_name'),
        Student.name.label('student_name'),
        Subject.name.label('subject_name')
    ).join(Subject, Subject.teacher_id == Teacher.id) \
        .join(Grade, Grade.subject_id == Subject.id) \
        .join(Student, Student.id == Grade.student_id) \
        .filter(Teacher.id == teacher_id, Student.id == student_id) \
        .distinct() \
        .order_by(Subject.name) \
        .all()

    return courses

def select_11(student_id, teacher_id):
    """Average grade that a specific teacher gives to a specific student."""
    avg_grade = session.query(
        Teacher.name.label('teacher_name'),
        Student.name.label('student_name'),
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject, Subject.teacher_id == Teacher.id) \
        .join(Grade, Grade.subject_id == Subject.id) \
        .join(Student, Student.id == Grade.student_id) \
        .filter(Teacher.id == teacher_id, Student.id == student_id) \
        .group_by(Teacher.name, Student.name) \
        .first()

    if avg_grade:
        return [(avg_grade.teacher_name, avg_grade.student_name, float(avg_grade.average_grade))]
    else:
        return []

def select_12(group_id, subject_id):
    """Grades of students in a specific group for a specific subject on the last lesson."""
    grade_alias = aliased(Grade)

    results = session.query(
        Group.name.label('group_name'),
        Student.name.label('student_name'),
        Subject.name.label('subject_name'),
        Grade.grade,
        Grade.date_of.label('lesson_date')
    ).join(Student, Student.group_id == Group.id) \
        .join(Grade, Grade.student_id == Student.id) \
        .join(Subject, Subject.id == Grade.subject_id) \
        .outerjoin(
        grade_alias,
        and_(
            grade_alias.student_id == Grade.student_id,
            grade_alias.subject_id == Grade.subject_id,
            grade_alias.date_of > Grade.date_of
        )
    ).filter(
        grade_alias.id == None,
        Group.id == group_id,
        Subject.id == subject_id
    ).order_by(Student.name) \
        .all()

    return results

def print_rows(rows, headers=None):
    if not rows:
        print("No data to display.")
        return

    if not headers:
        first_row = rows[0]
        if isinstance(first_row, dict):
            headers = first_row.keys()
            rows = [row.values() for row in rows]
        elif hasattr(first_row, '_fields'):
            headers = first_row._fields
        elif isinstance(first_row, tuple) or isinstance(first_row, list):
            headers = [f'Column {i+1}' for i in range(len(first_row))]
        else:
            headers = ['Value']
            rows = [[row] for row in rows]

    def process_value(value):
        if isinstance(value, Decimal):
            return float(value)
        elif isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return value

    processed_rows = [
        [process_value(item) for item in row] for row in rows
    ]

    print(tabulate(processed_rows, headers=headers, tablefmt="pretty"))


if __name__ == '__main__':
    print("Top 5 students with highest average grades")
    print_rows(select_1())

    print("\nStudent with the highest average grade in the subject with id 2")
    print_rows(select_2(2), headers=["name", "average_grade", "subject"])

    print("\nAverage grade in groups for the subject with id 1")
    print_rows(select_3(1), headers=["group", "average_grade", "subject"])

    print("\nAverage grade in the intake")
    print_rows(select_4())

    print("\nCourses of teacher with id 3")
    print_rows(select_5(3))

    print("\nList of students in the group with id 1")
    print_rows(select_6(1))

    print("\nGrades of students in the group with id 2 for the subject with id 3")
    print_rows(select_7(2, 3))

    print("\nAverage grade that teacher with id 2 gives in his/her subjects")
    print_rows(select_8(2), headers=["teacher", "subject", "average_grade"])

    print("\nList of courses that student with id 4 attends")
    print_rows(select_9(4))

    print("\nList of courses that teacher with id 3 teaches to student with id 5")
    print_rows(select_10(5, 3))

    print("\nAverage grade that teacher with id 3 gives to student with id 5")
    print_rows(select_11(5, 3), headers=["teacher", "student", "average_grade"])

    print("\nGrades of students in the group with id 2 for the subject with id 3 on the last lesson")
    print_rows(select_12(2, 3))

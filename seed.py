from models import Group, Student, Teacher, Subject, Grade
from faker import Faker
import random
from datetime import datetime, timedelta
from session import session

fake = Faker()

group_names = ['Group A', 'Group B', 'Group C']
groups = []
for name in group_names:
    group = Group(name=name)
    session.add(group)
    groups.append(group)
session.commit()

teachers = []
for _ in range(random.randint(3, 5)):
    teacher = Teacher(name=fake.name())
    session.add(teacher)
    teachers.append(teacher)
session.commit()

subject_names = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'Literature', 'Art']
subjects = []
for name in random.sample(subject_names, random.randint(5, 8)):
    subject = Subject(name=name, teacher=random.choice(teachers))
    session.add(subject)
    subjects.append(subject)
session.commit()

students = []
for _ in range(random.randint(30, 50)):
    student = Student(name=fake.name(), group=random.choice(groups))
    session.add(student)
    students.append(student)
session.commit()

for student in students:
    for _ in range(random.randint(1, 20)):
        grade = Grade(
            grade=random.randint(60, 100),
            date_of=datetime.now() - timedelta(days=random.randint(1, 365)),
            student=student,
            subject=random.choice(subjects)
        )
        session.add(grade)
session.commit()

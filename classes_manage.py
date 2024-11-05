import argparse
from models import Student, Group, Subject, Teacher, Grade
import sys
from tabulate import tabulate
from session import session

def create_record(model_name, **kwargs):
    model_class = get_model_class(model_name)
    if not model_class:
        print(f"Unknown model: {model_name}")
        return

    try:
        record = model_class(**kwargs)
        session.add(record)
        session.commit()
        print(f"Created {model_name} with ID: {record.id}")
    except Exception as e:
        session.rollback()
        print(f"Error creating {model_name}: {e}")

def list_records(model_name):
    model_class = get_model_class(model_name)
    if not model_class:
        print(f"Unknown model: {model_name}")
        return

    records = session.query(model_class).all()
    if records:
        headers = [column.name for column in model_class.__table__.columns]

        rows = [
            [getattr(record, column) for column in headers]
            for record in records
        ]

        print(tabulate(rows, headers=headers, tablefmt="pretty"))
    else:
        print(f"No records found for model {model_name}.")

def update_record(model_name, record_id, **kwargs):
    model_class = get_model_class(model_name)
    if not model_class:
        print(f"Unknown model: {model_name}")
        return

    record = session.query(model_class).get(record_id)
    if not record:
        print(f"{model_name} with ID {record_id} not found.")
        return

    try:
        for key, value in kwargs.items():
            setattr(record, key, value)
        session.commit()
        print(f"Updated {model_name} with ID: {record_id}")
    except Exception as e:
        session.rollback()
        print(f"Error updating {model_name}: {e}")

def remove_record(model_name, record_id):
    model_class = get_model_class(model_name)
    if not model_class:
        print(f"Unknown model: {model_name}")
        return

    record = session.query(model_class).get(record_id)
    if not record:
        print(f"{model_name} with ID {record_id} not found.")
        return

    try:
        session.delete(record)
        session.commit()
        print(f"Deleted {model_name} with ID: {record_id}")
    except Exception as e:
        session.rollback()
        print(f"Error deleting {model_name}: {e}")

def get_model_class(model_name):
    model_mapping = {
        'teacher': Teacher,
        'student': Student,
        'group': Group,
        'subject': Subject,
        'grade': Grade,
    }
    return model_mapping.get(model_name)

def main():
    parser = argparse.ArgumentParser(description='CLI for CRUD operations on the database.')
    parser.add_argument('-a', '--action', choices=['create', 'list', 'update', 'remove'], required=True, help='CRUD action to perform.')
    parser.add_argument('-m', '--model', choices=['teacher', 'student', 'group', 'subject', 'grade'], required=True, help='Model to perform action on.')

    parser.add_argument('--id', type=int, help='ID of the record (required for update and remove).')
    parser.add_argument('--name', type=str, help='Name field (for models that have a name).')

    parser.add_argument('--teacher_id', type=int, help='Teacher ID (for Subject model).')
    parser.add_argument('--group_id', type=int, help='Group ID (for Student model).')
    parser.add_argument('--subject_id', type=int, help='Subject ID (for Grade model).')
    parser.add_argument('--student_id', type=int, help='Student ID (for Grade model).')
    parser.add_argument('--grade', type=int, help='Grade value (for Grade model).')
    parser.add_argument('--date_of', type=str, help='Date of grade in YYYY-MM-DD format (for Grade model).')

    args = parser.parse_args()

    action = args.action
    model = args.model

    if action == 'create':
        kwargs = {}
        if model in ['teacher', 'student', 'group', 'subject']:
            if not args.name:
                print(f"--name is required to create a {model}.")
                sys.exit(1)
            kwargs['name'] = args.name

        if model == 'subject':
            if not args.teacher_id:
                print("--teacher_id is required to create a Subject.")
                sys.exit(1)
            kwargs['teacher_id'] = args.teacher_id

        if model == 'student':
            if not args.group_id:
                print("--group_id is required to create a Student.")
                sys.exit(1)
            kwargs['group_id'] = args.group_id

        if model == 'grade':
            required_args = ['student_id', 'subject_id', 'grade', 'date_of']
            for arg in required_args:
                if getattr(args, arg) is None:
                    print(f"--{arg} is required to create a Grade.")
                    sys.exit(1)
            kwargs['student_id'] = args.student_id
            kwargs['subject_id'] = args.subject_id
            kwargs['grade'] = args.grade
            kwargs['date_of'] = args.date_of

        create_record(model, **kwargs)

    elif action == 'list':
        list_records(model)

    elif action == 'update':
        if not args.id:
            print("--id is required to update a record.")
            sys.exit(1)
        kwargs = {}
        if args.name:
            kwargs['name'] = args.name
        if args.teacher_id:
            kwargs['teacher_id'] = args.teacher_id
        if args.group_id:
            kwargs['group_id'] = args.group_id
        if args.subject_id:
            kwargs['subject_id'] = args.subject_id
        if args.student_id:
            kwargs['student_id'] = args.student_id
        if args.grade is not None:
            kwargs['grade'] = args.grade
        if args.date_of:
            kwargs['date_of'] = args.date_of

        if not kwargs:
            print("At least one field to update must be provided.")
            sys.exit(1)

        update_record(model, args.id, **kwargs)

    elif action == 'remove':
        if not args.id:
            print("--id is required to remove a record.")
            sys.exit(1)
        remove_record(model, args.id)

    else:
        print(f"Unknown action: {action}")


if __name__ == '__main__':
    main()

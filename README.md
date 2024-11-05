# GOIT Python Web Homework 6 - Class Management System

A Python-based Class Management System utilizing SQLAlchemy ORM with a PostgreSQL database. This project provides scripts and a CLI application for performing CRUD operations on database models representing teachers, students, groups, subjects, and grades.

---

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
  - [Running Scripts](#running-scripts)
  - [Using the CLI Application](#using-the-cli-application)
- [Cleanup](#cleanup)

---

## Introduction

This project is designed to manage academic classes, allowing users to perform various operations such as creating, reading, updating, and deleting records related to teachers, students, groups, subjects, and grades. It leverages SQLAlchemy for ORM (Object-Relational Mapping) and uses PostgreSQL as the database backend.

---

## Requirements

Before you begin, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Python 3.10+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

---

## Installation

1. **Clone the Repository**

   ```shell
   git clone https://github.com/AntonChubarov/goit-pythonweb-hw-06.git
   cd goit-pythonweb-hw-06
   ```
   
2. **Install psycopg2-binary**

   ```shell
   pip install psycopg2-binary
   ```
   
3. **Install Project Dependencies**

   ```shell
   poetry install
   ```
   
## Setup

1. **Start the PostgreSQL Database**

   ```shell
   sh ./run_postgres.sh
   ```

2. **Apply Database Migrations**

   ```shell
   sh ./alembic_apply_migrations.sh
   ```

3. **Seed the Database with Fake Data**

   ```shell
   python3 seed.py
   ```
   
## Usage

### Running Scripts

You can run the `my_select.py` script to execute predefined queries and display results:
```shell
python3 my_select.py
```

### Using the CLI Application

The `classes_manage.py` script provides a command-line interface for CRUD operations on the database models.

#### View Help

```shell
python3 classes_manage.py --help
```

#### Examples

- **List All Subjects**
   
   ```shell
   python3 classes_manage.py -a list -m subject
   ```
  
- **Create a New Grade**
   
   ```shell
   python3 classes_manage.py -a create -m grade --subject_id 1 --student_id 4 --grade 95 --date_of 2024-11-04
   ```
  
- **Update a Teacher's Name**
   
   ```shell
   python3 classes_manage.py -a update -m teacher --id 3 --name "Emily Stone"
   ```
  
- **Remove a Student**
   
   ```shell
   python3 classes_manage.py -a remove -m student --id 5
   ```
  
## Cleanup

To stop and remove the PostgreSQL Docker container when you're done:

```shell
sh ./stop_postgres.sh
```
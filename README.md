# UCI Canvas LMS Assignment Fetcher

![Python](https://img.shields.io/badge/Python-3.13.7-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-lightgrey)

## About

A Python module and FastAPI server for retrieving upcoming assignments from the UCI Canvas LMS using the Canvas GraphQL API.

Includes instructions on how to host the FastAPI server locally.

Includes instructions for using the local server with the iOS Shortcuts app to import upcoming assignments into the iOS Reminders app.

---

## Features

- Fetch assignments with due dates for all Canvas courses.
- Store information about the assignments such as including course name, assignment name, and due date.
- Filter assignments due within a specified number of weeks.
- Easy to adapt for other universities by updating the base Canvas URL.
- Run a Python module that hosts a FastAPI server locally without using the command line.
- Display information about upcomming assignments on the local server.
- Access the local server across multiple devices on the same network using a simple url.

---

## iOS Shortcuts Integration

Following the guide to host a local server and use the iOS Shortcuts app, users can:

- Import upcoming assignments directly into the iOS Reminders app.
- Sync assignments on demand from your local FastAPI server.
- View assignment reminders on the iOS Calendar app.


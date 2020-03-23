# Playroom

A web application for managing a video game database. It uses Python with Flask, alongside MySQL.

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-yellow?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Made with Flask](https://img.shields.io/badge/Made%20with-Flask-green?style=for-the-badge&logo=flask)](https://palletsprojects.com/p/flask/)

## Functionalities

**User-related features**

- Login
- Logout

**Data-related features**

- List all video games
- Insert a video game
- Update a video game
- Delete a video game

**Validations**

In order for someone to insert, update or delete a video game from the database, the user must be logged in the application.
The listing (available at the index route) is displayed to everyone, logged in or not.

## Data storage

All structured data related to users and video games are stored in a relational database (MySQL), while the image files for the artwork of the video games are stored in the server (```/upload/``` directory).
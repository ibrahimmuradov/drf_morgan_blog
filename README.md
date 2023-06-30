# DRF Morgan Blog

Since I only do the backend part of the project with the API, you can complete the project with the front-end developer and use it.

## Description

I only did the backend part of the project. I've created APIs that the front-end developer can use. After installing the project, I added documentation that the front-end developer can access all APIs from the api/swagger/ page. In the project, users can register, login and edit their own information. As an admin, you can publish blogs from the admin panel and manage them as you wish. The blogs you share can be commented and shared. Users can contact you in the contact section.<br>
I made the backend with Django Rest Framework.

## Installation

```bash
git clone https://github.com/ibrahimmuradov/drf_morgan_blog.git .
pip install -r requirements.txt
django-admin startproject core . 
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

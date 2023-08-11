# Introduction

this is a code challenge django project.
this project is written in python and django 4.2.


### Main technologies

* Python 3.10

* Postgresql as database backend 

* Django 4.2

* Django Rest Framework

* celery



# Usage

To run project using :

```bash
docker-compose up -d
```

project will be accessible from **localhost:8080**

you can import sample data. in this case you can enter admin panel use admin/admin as username and password from **localhost:8080/admin**:

```bash
docker-compose exec license-server sh -c "python manage.py loaddata sample_data/sample_data_fixture"
```

or create a superuser and use admin panel:
```bash
docker-compose exec license-server sh -c "python manage.py createsuperuser"
```
you can run test using:
```bash
docker-compose exec license-server sh -c "python manage.py test"
```

also to send a license expiration notification process you can send post to **localhost:8080/notifications/license_expiration/** endpoint

you can use this command:
```bash
curl --location --request POST 'http://localhost:8080/notifications/license_expiration/'
```


# other features
in this project process of sending a notification(group of emails that matches a group of rules ) is taking place in celery task.
also beside web pages for notification history and items with their statuses related apis are provided that can be accessible from :

* localhost:8080/api/notifications/
* localhost:8080/api/notification_items/?notification_id=<notification_id>

# Django-blog
Take home assessment for First Principles Publishing

## Run instructions
This is a barebones application and is not FULLY optimized, but it does function and do everything the requirements asked

1. [Clone this repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
2. Add your own database password file `secrets/password.txt` and type in some password. The contents don't *actually* matter, the point is that the password is never part of the VCS
3. [Install docker and docker compose](https://www.docker.com/products/docker-desktop/?) if you haven't already
4. use docker compose to boot up the installation on your local machine
```shell
docker compose up 
```
5. access the site at https://localhost:8000/admin/
6. login to the admin site using the pre-built user `username=admin`, password is `superuser-password`


## Using the API
If using the API, you first need to get a refresh token, this app uses [django rest framework simple jwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html) 
1. First you need to POST username and password to the endpoint `api/token` and receive
```json
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```
2. Then use that token in the header of your request
```
curl \
  -H "Authorization: Bearer <your_access_token> \
  http://localhost:8000/blogposts/
```

Now you can CRUD new blogposts to the `blogposts/` and `blogposts/<pk>/` endpoints. If you get a 403, you need to use the `refresh` token to the `api/token/refresh/` endpoint to refresh the token. 


## Trade-offs and future features
First, I would have a more robust admin page for admins to do CRUD actions with a UI. 
Secondly, I would add additional configurations for terraform or other IAC in order to create the necessary cloud resources.
And finally, I would have an official CI/CD pipeline using circleCI or travisCI to test code on each push, and even automatically deploy changes to aforementioned cloud resources on certain actions, like merging into master

There's lots of little features I'd add, and moving around of code. But avoiding complication and redirection is more important than trying to predict the future. **Maintainable code is understandable code**



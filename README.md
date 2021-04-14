# Django Googel OAuth

This is an example app where you can sign up and sign in, and you can sign in with Google too.


## Getting Started
### Prerequisites
You need to have installed:

- [Python](https://www.python.org/downloads/)
- [VirtualEnv](https://virtualenv.pypa.io/en/latest/index.html)
  
You have to go to the [Google API Dashboard](https://console.cloud.google.com/apis/dashboard) and:
- Create a new project
- Fill in the oauth consent screen
- Create an Oauth ID client in the credentials section, where you'll register the origin of your app (http://127.0.0.1:8000) in the URI section and the URI http://127.0.0.1:8000/oauth/google/login/callback/ in the Redirect URI section.
- Finally you'll obtain a client Id and a secret key.


### Running the project
1. Clone the [project](https://github.com/Echeverrias/django-google-oauth.git) </b>
2. Open the terminal, go to the project root folder and install the virtual environment.<br>
3. Activate the virtual environment.<br>
4. Install all the requirements with <b>pip install -r requirements.txt</b><br>
5. Go to the 'src' folder<br>
6. Execute <b>python manage.py makemigrations</b> to create the migrations.<br>
7. Execute <b>python manage.py migrate</b> to create the tables in the database.<br>
8. Execute <b>python manage.py createsuperuser</b> to create a default user with administrator permission.<br>
9. Execute <b>python manage.py runserver</b> and the application will start in the url <a href="http://127.0.0.1:8000/">http://127.0.0.1:8000/</a><br>
10. Go to [administration panel](http://127.0.0.1:8000/admin)
11. Add a new site in Site model adding the origin of your app (http://127.0.0.1:8000) as the domain name.
12. Add a new social application in Social Applications model choosing Google ass provider, adding the client id and the secret key provided by Google and chosing your origin app as chosen sites.

## Development
The app is developed in [Python](https://www.python.org) and uses the framework [Django](https://www.djangoproject.com/) for build the web app.<br><br>

## Built with
* Python 3.9.2
* Django 3.2

# Author
* Juan Antonio Echeverrías Aranda
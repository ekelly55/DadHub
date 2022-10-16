# DadHub

## Concept 

### What is DadHub?
DadHub is your place for dads to connect! Everyone always says, "Making friends as an adult is hard," and "Making friends as a man is hard." When you become a dad, you suddenly have great common ground for making friends: fatherhood. But while fatherhood is a tremendous shared experience, sometimes you want to make dad-friends who share your interests and passions and want to share them with their own kids, too, whether those passions are sports-ball or...Norwegian black metal. You belong here.
DadHub: for the average dads, for the weird dads, and every dad in between.

### Who Can Join DadHub?
DadHub is for anyone who identifies as a dad or father-figure, regardless of age, race, religion, socioeconomic status, sexual orientation or gender assigned at birth. Bio-dads, adoptive-dads, step-dads, grand-dads, queer dads, foster dads, etc, are all welcome!

## Technology Stack

- Django 4.1.2 
- Python 3.1
- Bootstrap 5.1

## Installation Steps

After cloning this repo (these steps asssume postgresql previously installed):

1. Run pip3 install pipenv in your terminal.
2. Run pipenv shell to create and enter a new virtual environment shell. Be sure to run the following command within the pipenv shell. 
3. Run pipenv install django psycopg2-binary psycopg2
4. Run python3 manage.py runserver
5. You'll notice that the app is using a previously-created and populated SQL database. To create and use your own database, follow these steps:
    1. Run createdb <your-database-name>
    2 In settings.py, change DATABASES.default.NAME to your database name

## User Stories

Dads can go to DadHub and create an account or browse the blurb page first. To see more or interact, they will have to sign up. 
Upon signing up, the user is taken to a page to create a Bio. Once that is complete, they are directed to the blurbs page, where they can post their own Blurb and respond to other Blurbs. From here they are able to click on the usernames in posts to see other users' profiles. Users are able to edit and update their profile and delete their blurbs or responses. 

## Wireframes

Part of the story of DadHub is that I created it during a period in which both of my twin 3-year-old sons were sick, so it is fitting that the initial concept sketches were done roughly on a notepad with my son next to me doodling on his own notepad. 

### Blurbs Page

Initially the Home page, I changed the homepage to a landing page/about page. 

Blurbs: ![Blurbs](https://i.imgur.com/TU9z0q5.jpg "Blurbs")

Blurb Detail: ![Blurb Detail](https://i.imgur.com/ks8Saln.jpg "Blurb Detail")

Hub Detail (concept for group page): ![Hub Detail](https://i.imgur.com/80iTrIB.jpg "Hub Detail")

Bio: ![Bio](https://i.imgur.com/0FBoRWu.jpg "Bio")

Blurbs: ![Blurbs](/wp.png "Blurbs")
Blurbs: ![Blurbs](/wp.png "Blurbs")
Blurbs: ![Blurbs](/wp.png "Blurbs")
Blurbs: ![Blurbs](/wp.png "Blurbs")
Blurbs: ![Blurbs](/wp.png "Blurbs")


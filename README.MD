# Learner Management System (LMS)

This app allows teachers to keep track of their students and grades in each of their classes. It allows teachers to view, add , edit and delete both classes and students.  It also allows students to log in and view their classes, their grades and their average grade per subject. Each user can also edit their own public profile as well as view the profiles of other site users.

 
## UX

### User Stories 

** General User **
As a general site user I should be able to:
1. View the profile of other users.
2. Edit my profile.

** Teacher **
As a teacher I should be able to:
1. See all of the classes I teach.
2. Add and delete classes I teach. 
3. Edit the classes I teach by:
	* Seeing all of the students for each class and being able to add, edit and remove them for the class.
4. Add new students to the system.
5. See all the students on the system and be able to quickly view, edit or delete them.

** Student **
As a student I should be able to:
1. See all of the classes I study.
2. See my grade for each class and an average grade for each subject.

### Wireframes

[Click here to view Desktop wireframes](./wireframes/desktop/)
[Click here to view Tablet wireframes](./wireframes/tablet/)
[Click here to view Mobile wireframes](./wireframes/mobile/)

## Features

I have designed and split the site into three separate sections: Home, Student and Staff. This was achieved by implementing (or at least trying to) the Model View Controller pattern and using Flask blueprints. The hope was that this would "future proof" the project, in that if the student section needed to be change the changes could be made without worrying how it would affect the staff / home section.

The home section is responsible for handling user login, serving up user profiles and handling exceptions.

The staff section allows teachers to C.R.U.D their classes and students, and edit their profile.

The student section allows students to view their classes, grades and subject average grade as well as edit their profile.

### Existing Features
- The staff section allows teachers to easily Create, Retrieve, Update and Delete their classes. This is achieved by the user clicking the "Manage Classes" link. This takes the user to a page with a dynamically generated menu, broken into subjects. When the user clicks on a subject, each class they teach for that subjected is shown below. In addtion there is a button that allows the user to add a new class to this menu.

 When a teacher clicks the name of a course a dynamically generated table is displayed to them. This table allows them to Delete the entire class, as well as view all of the students studying the class. The teacher is able to view all the information for each student here as well as easily remove them from the class or edit their grade.

 - The staff section allows teachers to Create, Retrieve, Update and Delete students on the site. This is achieved by the user clicking hte "Manage students" link. Once clicked, the user is again presented with a dynmically generated table. Giving them an overview of all students (similar to the one view in manage classes).

 - The staff and the student section allow a student and teacher to view and edit their public profile. After logging in and being directed to the correct section of the site, they are immediately presented with their profile.

 - The student section allows students to view their classes. This is done by clicking the "My classes" link which will then show a dynamically generated menu, separated into subjects. When a student clicks a subject they are told the number of classes they are studying in, and the average grade for, the selected subject. They are also presented with a list of links to the courses of the selected subject. If clicked, this willl show the user their grade for the selected course.

### Features Left to Implement


- I would like to add an "Admin" section to the site that would allow admins to Create, Retrieve, Update and Delete courses, students and staff. 

- Improve the security of the site. 
	- At the moment the login system is a matter of simply storing and reading from a session variable, I would like to improve upon this and use a library to handle the login (for example Flask-Login).
	- A number of forms are use across the site and at the moment these are vulnerable to CSRF attacks. Ideally each form would have an attached CSRF token to prevent this.

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

* HTML 5 - Used to provide structure to each page of the site
* CSS  - Used to format the HTML of each page.
* Javascript - Used for AJAX and dynamically generating site content.
* [Python](https://www.python.org/) - Used for the backend of the site.
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Used for the web framework.
* [Mongodb](https://www.mongodb.com/) - Used as the database. Also used their cloud service to host the database for the deployed site.
* [MongoMock](https://github.com/mongomock/mongomock) - Used to mimick MongoDB in unittests.
* [PyMongo](https://pymongo.readthedocs.io/en/stable/) - Used to work with MongoDB in Python. 
* [Heroku](https://www.heroku.com/) - Used to host the deployed site.
* [Firefox Dev tools](https://developer.mozilla.org/en-US/docs/Tools) - Used during development to test the responsive design. 
* [Neovim](https://neovim.io/) - Code editor used to develop this project. A number of plugins were used with it and the config can be viewed [here](https://github.com/CDHayden/dotfiles/blob/master/init.vim)
* [Git] (https://git-scm.com/) - Local version control
* [Github](https://github.com/) - Used to host the online repository for this site.j
* [Bootstrap](https://getbootstrap.com/) - Used to builda responsive website.
* [color.review](https://color.review/) - To pick colour pallete and check the contrast is compliant with standards.
* [Fontawesome](https://fontawesome.com/) - Icons used on site.
* [Autoprefixer](https://autoprefixer.github.io/) - Used to get browser specific prefixs for my css.
* [Fontjoy](https://fontjoy.com/) - Used to find fonts that compliment one another.
* [Codepen - pen](https://codepen.io/martinwolf/pen/eNNdme/) - Used to tailor hover effect for links
* [ExploreFlask](http://exploreflask.com/) - I used this guide on how to structure my project initially, although changes were made
* [Design Tips](https://twitter.com/i/events/994601867987619840) - Design tips used when styling site.
* [Color Convertor](https://www.w3schools.com/colors/colors_converter.asp) - to change between hexcodes and hsl colour values.
* [Javascript base64 help](https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL) - How to preview file via Javascript and encode it as base64
* [Image Aspect Ratio Help](https://stackoverflow.com/questions/19414856/how-can-i-make-all-images-of-different-height-and-width-the-same-via-css) - How to display images the same height and width if they are different aspect ratios
* [Styling file input types](http://jsbin.com/fokexoc/2/edit?html,css,output) - How to style input type file and still make it accessible 
* [Help using a base64 string as a URI](https://stackoverflow.com/questions/6375942/)- Helped me to figure out how to serve the base64 uri directly as the image source and for it to work. 
* [Help using a base64 string as a URI](https://stackoverflow.com/a/49475135/12732623)- Helped me to figure out how to serve the base64 uri directly as the image source and for it to work. 
* [Help editing git hunks](https://git-scm.com/docs/git-add) - Helped with manually editing git hunks.
* [Help with blueprint endpoints and url_for](https://stackoverflow.com/questions/10542493/using-flask-blueprints-how-to-fix-url-for-from-breaking-if-a-subdomain-is-speci) - Helped with using the url_for function with blueprint endpoints
* I used the pymongo and mongodb docs a lot during this project, however I wanted  to specifically highlight the following:
	* [Array filters](https://docs.mongodb.com/manual/reference/operator/update/positional-filtered/)- Helped me to use postitional identifiers and array filters in my mongo queries
	* [Aggregation](https://pymongo.readthedocs.io/en/stable/examples/aggregation.html) - Helped with my aggregation queries

## Testing

As I wrote each unit of functionality I would manually test them with dummy data to make sure they worked as expected. However, this became quickly tedious and I started to write unittests. Unfortunately I ran out of time and have no chieved full-test coverage with them (I resorted to my old technique of manual testing with dummy data). You can view the tests in the test/ directory of the repository. To run them navigate to the root directory and run `python -m unittest discover -p "*_test.py"`

- Improve the dynamically generated menus for staff and students. In python, the order of keys in a dictionary is neither guaranteed nor maintained. This means that somtimes an item might be the first in a menu, whilst later on the same item might be last in the menu. This is very jarring to the user experience and halts the user building on learned experience. Having read around on this I believe the issue could be fixed by using bson.SON objects in my pymongo queries. Unfortunately I was unable to get this working presently.

## Deployment

This project was deployed to heroku via a simple Procfile. I also created the following config vars in the heroku app: 

You can view the deployed site here: [lms.herokuapp.com](http://lms5.herokuapp.com/)

```
ALLOWED_EXTENSIONS = {'jpg','jpeg','png','gif'}
HOST = 0.0.0.0
MONGO_URI = uri to mongo db
SECRET_KEY = secret key
```
To deploy locally please clone the repo into a location of your choice: 

` git clone https://github.com/CDHayden/LearnerManagementSystem.git`

In the root directory of your newly cloned repository there is a `.env` file with the following contents:

```
DEBUG=True
FLASK_APP=app.py
FLASK_ENV=development
ALLOWED_EXTENSIONS={'jpg','jpeg', 'png', 'gif'}

MONGO_URI=
SECRET_KEY=
```

You need to supply your own mongo_uri and secrey_key. You simply run the application by typing `flask run`

## Credits
My mentor Reuben Ferrante for his patience and time helping me with this project. I am very grateful to him.

## How to deploy locally
You will need environment variables (preferably via a .env file) for:

`MONGO_URI= dbURI
HOST= hostAddress
PORT= portnumber
SECRET_KEY= yoursecretkey
DEBUG= True
ALLOWED_EXTENSIONS = {'jpg','jpeg','png','gif'}`

## resources used
* http://exploreflask.com/ - I used this guide on how to structure my project initially, although changes were made

* https://flask.palletsprojects.com/en/1.1.x/patterns/jquery/ - Help with Ajax in flask 

* https://color.review/ - To pick colour pallete and check the contrast is compliant with standards.

* https://www.w3schools.com/colors/colors_converter.asp - to change between hexcodes and hsl colour values.

* https://twitter.com/i/events/994601867987619840 - Design tips used when styling site.

* https://fontawesome.com/ - Icons used on site.

* https://codepen.io/martinwolf/pen/eNNdme/ - Used to tailor hover effect for links

* https://fontjoy.com/ - Used to find fonts that compliment one another.

* http://jsbin.com/fokexoc/2/edit?html,css,output - How to style input type file and still make it accessible 

* https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL - How to preview file via Javascript and encode it as base64
*https://stackoverflow.com/questions/19414856/how-can-i-make-all-images-of-different-height-and-width-the-same-via-css - How to display images the same height and width if they are different aspect ratios

* https://stackoverflow.com/questions/6375942/https://stackoverflow.com/a/49475135/12732623- Helped me to figure out how to serve the base64 uri directly as the image source and for it to work. 

## Problems
Took a long time to get ajax to work. After googling the issue I came across an answer on stackoverflow that importing the slim version of jquery exlcudes the ajax capabilities. Importing the full version fixed this issue.However, this became redundant once I had upgraded to bootstrap 5 (which doesn't require Jquery). I simply rewrote the ajax functions in vanilla Javascript.

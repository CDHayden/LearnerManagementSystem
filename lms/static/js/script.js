/**
 * Called when a page has loaded and wants to apply the active class to the desired menu item.
 * Removes the active class from any other menu item.
 *
 * This function presumes that the list object (ol or ul) wrapping the menu items has an id of menuList
 *
 * As this function uses dom manipluation it is up to the user to check if the DOM content has loaded before using it.
 *
 * @param elementId - Id of the menu item to apply active to
 */
function selectActiveMenuItem(elementId, className) {
  let list = document.querySelectorAll('#menuList > li');

  list.forEach(function (currentLink) {
    if (currentLink.id == elementId) {
      currentLink.classList.add(className);
    } else {
      currentLink.classList.remove(className);
    }
  });
}

/**
 * Called when a link with the "course-content-link" class is clicked.
 * Requests and loads information about the course via AJAX
 *
 * @param e - Event object passed in on click
 * @param display - Element to display JSON data in
 */
const loadCourseContent = (e, displayID) => {
  const course = e.srcElement.innerText;
  const subject =
    e.srcElement.parentElement.parentElement.parentElement.parentElement
      .previousElementSibling.innerText;

  const display = document.getElementById(displayID);

  fetch('/student/_load_course_content', {
    headers: { 'content-type': 'application/json; charset=utf-8' },
    method: 'post',
    body: JSON.stringify({
      subject: subject,
      course: course,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      display.innerText = '';
      display.innerText = JSON.stringify(data);
    });
  e.preventDefault();
};

/**
 * Called when a link with the "subject-content-link" class is clicked.
 * Requests and loads information about the course via AJAX
 *
 * @param e - Event object passed in on click
 * @param display - Element to display JSON data in
 */
const loadSubjectContent = (e, displayID) => {
  const subject = e.srcElement.innerText;
  const display = document.getElementById(displayID);

  if (e.srcElement.attributes['aria-expanded'].nodeValue == 'true') {
    fetch('/student/_load_subject_content', {
      headers: { 'Content-Type': 'application/json; charset=utf-8' },
      method: 'POST',
      body: JSON.stringify({
        subject: subject,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        display.innerText = '';
        display.innerText = JSON.stringify(data);
      });
  }
  e.preventDefault();
};

/**
 * This file contains all the functionality to dynamically create the
 * table viewed when you select a class on /staff/my_classes
 */

/**
	Because generating a table requires a lot of rows, create a 
	separate function to handle the creation of it 
*/

const table_row = () => {
  row = document.createElement('tr');
  return row;
};

/**
	Generate the header row for the table, this would need 
	updating if the data passed in changed
*/
const generateTableHeader = () => {
  row = table_row();

  //username
  const un = document.createElement('th');
  un.setAttribute('scope', 'col');
  un.innerText = 'Username';

  //forename
  const fn = document.createElement('th');
  fn.setAttribute('scope', 'col');
  fn.innerText = 'Forename';

  //surname
  const sn = document.createElement('th');
  sn.setAttribute('scope', 'col');
  sn.innerText = 'Surname';

  //profile link
  const pf = document.createElement('th');
  pf.setAttribute('scope', 'col');
  pf.innerText = 'Profile';

  //grade
  const gd = document.createElement('th');
  gd.setAttribute('scope', 'col');
  gd.innerText = 'Grade';

  //actions
  const ac = document.createElement('th');
  ac.setAttribute('scope', 'col');
  ac.setAttribute('colspan', 2);
  ac.innerText = 'Actions';

  row.appendChild(un);
  row.appendChild(fn);
  row.appendChild(sn);
  row.appendChild(pf);
  row.appendChild(gd);
  row.append(ac);

  return row;
};

/* 
	Generates the body of the table and populates it with the data 
	received from the server */
const generateBodyRow = (subject, course, data) => {
  row = table_row();

  //username
  const un = document.createElement('th');
  un.setAttribute('scope', 'row');
  un.innerText = data.username;

  //forename
  const fn = document.createElement('td');
  fn.innerText = data.forename;

  //surname
  const sn = document.createElement('td');
  sn.innerText = data.surname;

  //profile
  const pf = document.createElement('td');
  const pfl = document.createElement('a');
  const pfl_text = document.createTextNode('Profile link');
  pfl.appendChild(pfl_text);
  pfl.setAttribute('title', 'Profile link for' + data.username);
  pfl.setAttribute('href', '/profile/' + data.username);
  pf.appendChild(pfl);

  //grade
  const gd = document.createElement('td');

  const grade = data.subjects.find(
    (element) => element['subject'] === subject && element['course'] == course
  )['grade'];

  gd.innerText = grade;

  //edit
  const ed = document.createElement('td');
  ed.addEventListener(
    'click',
    () => editStudent(data.username, grade, subject, course),
    false
  );
  const ed_icon = document.createElement('i');
  ed_icon.classList.add('fas');
  ed_icon.classList.add('fa-user-edit');
  ed.appendChild(ed_icon);

  //Delete
  const dl = document.createElement('td');
  dl.addEventListener(
    'click',
    () => removeFromClass(data.username, subject, course),
    false
  );
  const dl_icon = document.createElement('i');
  dl_icon.classList.add('fas');
  dl_icon.classList.add('fa-user-minus');
  dl.appendChild(dl_icon);

  row.appendChild(un);
  row.appendChild(fn);
  row.appendChild(sn);
  row.appendChild(pf);
  row.appendChild(gd);
  row.appendChild(ed);
  row.appendChild(dl);
  return row;
};

/**
Taken from:
https://www.javascripttutorial.net/dom/manipulating/remove-all-child-nodes/

Used in deleting the table
*/
const removeAllChildNodes = (node) => {
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }
};

/**
	Generates a table to hold JSON data from server
*/
const generateTable = (subject, course, data) => {
  const tableHead = document.getElementById('table-head');
  const tableBody = document.getElementById('table-body');

  header_row = generateTableHeader();
  tableHead.appendChild(header_row);

  data.forEach((student) => {
    tableBody.appendChild(generateBodyRow(subject, course, student));
  });

  add_new_student = table_row();
  const ans = document.createElement('td');
  ans.setAttribute('colspan', 7);
  ans.classList.add('text-center');
  ans.addEventListener('click', () => {
    addStudent(subject, course);
  });
  const ans_icon = document.createElement('i');
  ans_icon.classList.add('fas');
  ans_icon.classList.add('fa-user-plus');
  ans.appendChild(ans_icon);
  add_new_student.appendChild(ans);
  tableBody.appendChild(add_new_student);
};

/**
	Removes any dynamically generated table content
*/
const destroyTable = () => {
  const tableHead = document.getElementById('table-head');
  const tableBody = document.getElementById('table-body');

  removeAllChildNodes(tableHead);
  removeAllChildNodes(tableBody);
};

/**
 * 		EVENT LISTENERS
 */

const editModal = new bootstrap.Modal(document.getElementById('editModal'));
const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
const addModal = new bootstrap.Modal(document.getElementById('addModal'));
const addClassModal = new bootstrap.Modal(
  document.getElementById('addClassModal')
);
const deleteClassModal = new bootstrap.Modal(
  document.getElementById('deleteClassModal')
);

const addClass = (e) => {
  addClassModal.toggle();
  e.preventDefault();
};

const deleteClass = (e, subject, course) => {
  document.getElementById('deleteClassModalTitle').innerText =
    'Delete ' + subject + ' - ' + course;
  document.getElementById('deleteClassSubject').value = subject;
  document.getElementById('deleteClassCourse').value = course;
  document.getElementById('deleteClassConfirm').innerText =
    ' Are you sure you want to delete ' + subject + ' - ' + course + ' ? ';
  deleteClassModal.toggle();
  e.preventDefault();
};
/**
 * Handles the user clicking the remove user icon
 */
const removeFromClass = (username, subject, course) => {
  document.getElementById('deleteModalTitle').innerText = 'Remove ' + username;
  document.getElementById('deleteConfirm').innerText =
    'Do you really wish to remove ' +
    username +
    ' from ' +
    subject +
    ' - ' +
    course +
    '?';
  document.getElementById('deleteUsername').value = username;
  document.getElementById('deleteSubject').value = subject;
  document.getElementById('deleteCourse').value = course;
  deleteModal.toggle();
};

/**
 * Handles the user clicking the edit user icon
 */
const editStudent = (username, grade, subject, course) => {
  document.getElementById('editModalTitle').innerText = 'Edit ' + username;
  document.getElementById('editGrade').setAttribute('placeholder', grade);
  document.getElementById('editUsername').value = username;
  document.getElementById('editSubject').value = subject;
  document.getElementById('editCourse').value = course;
  editModal.toggle();
};

/**
 * Deletes all options in the select in the addStudent Modal
 */
const clear_options = () => {
  const options = document.querySelectorAll('#addStudents option');
  options.forEach((option) => {
    option.remove();
  });
};

/**
 * Generates a drop down list of usernames for students who can be
 * selected and added to the class.
 */
const generate_dropdown_options = (subject, course) => {
  const select = document.getElementById('addStudents');
  fetch('/staff/_get_students_not_in_course', {
    headers: { 'content-type': 'application/json; charset=utf-8' },
    method: 'post',
    body: JSON.stringify({
      subject: subject,
      course: course,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      clear_options();
      data.forEach((student) => {
        let option = document.createElement('option');
        option.text = student['username'];
        select.add(option);
      });
    });
};

/**
 * Handles the user clicking the add user icon
 */
const addStudent = (subject, course) => {
  document.getElementById('addModalTitle').innerText =
    'Add students to ' + subject + ' ' + course;
  generate_dropdown_options(subject, course);
  document.getElementById('addSubject').value = subject;
  document.getElementById('addCourse').value = course;
  addModal.toggle();
};

document.addEventListener('DOMContentLoaded', (event) => {
  document.getElementById('addClassLink').addEventListener('click', addClass);
});

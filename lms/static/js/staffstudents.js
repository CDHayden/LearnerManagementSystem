/**
 * this file contains all the functionality to dynamically create the
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

  //subjects
  const sbjs = document.createElement('th');
  sbjs.setAttribute('scope', 'col');
  sbjs.innerText = 'Subjects';

  //profile link
  const pf = document.createElement('th');
  pf.setAttribute('scope', 'col');
  pf.innerText = 'Profile';

  //actions
  const ac = document.createElement('th');
  ac.setAttribute('scope', 'col');
  ac.setAttribute('colspan', 2);
  ac.innerText = 'Actions';

  row.appendChild(un);
  row.appendChild(fn);
  row.appendChild(sn);
  row.appendChild(sbjs);
  row.appendChild(pf);
  row.append(ac);

  return row;
};

/* 
	Generates the body of the table and populates it with the data 
	received from the server */
const generateBodyRow = (data) => {
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

  //subjects
  const sbs = document.createElement('td');
  const subject_list = document.createElement('ul');

  data.subjects.forEach((subject) => {
    let new_item = document.createElement('li');
    new_item.innerText = subject['subject'] + ' ' + subject['course'];
    subject_list.appendChild(new_item);
  });

  sbs.appendChild(subject_list);

  //profile
  const pf = document.createElement('td');
  const pfl = document.createElement('a');
  const pfl_text = document.createTextNode('Profile link');
  pfl.appendChild(pfl_text);
  pfl.setAttribute('title', 'Profile link for' + data.username);
  pfl.setAttribute('href', '/profile/' + data.username);
  pf.appendChild(pfl);

  //edit
  const ed = document.createElement('td');
  ed.addEventListener(
    'click',
    () => {
      editStudent(data.username, data.forename, data.surname);
    },
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
    () => {
      deleteStudent(data.username);
    },
    false
  );
  const dl_icon = document.createElement('i');
  dl_icon.classList.add('fas');
  dl_icon.classList.add('fa-user-minus');
  dl.appendChild(dl_icon);

  row.appendChild(un);
  row.appendChild(fn);
  row.appendChild(sn);
  row.appendChild(sbs);
  row.appendChild(pf);
  row.appendChild(ed);
  row.appendChild(dl);
  return row;
};

/**
	Generates a table to hold JSON data from server
*/
const generateTable = (data) => {
  const tableHead = document.getElementById('table-head');
  const tableBody = document.getElementById('table-body');

  header_row = generateTableHeader();
  tableHead.appendChild(header_row);

  data.forEach((student) => {
    tableBody.appendChild(generateBodyRow(student));
  });

  add_new_student = table_row();
  const ans = document.createElement('td');
  ans.setAttribute('colspan', 7);
  ans.classList.add('text-center');
  ans.addEventListener('click', () => {
    addStudent();
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
 * 		EVENT LISTENERS
 */
const editModal = new bootstrap.Modal(document.getElementById('editModal'));
const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
const addModal = new bootstrap.Modal(document.getElementById('addModal'));

/**
 * Handles the user clicking the add user icon
 */
const addStudent = () => {
  document.getElementById('addModalTitle').innerText = 'Add a new student';
  addModal.toggle();
};

/**
 * Handles the user clicking the remove user icon
 */
const deleteStudent = (username) => {
  document.getElementById('deleteModalTitle').innerText = 'Delete ' + username;
  document.getElementById('deleteConfirm').innerText =
    'Are you sure you want to delete ' + username + ' ?';
  document.getElementById('deleteUsername').value = username;
  deleteModal.toggle();
};

/**
 * Handles the user clicking the remove user icon
 */
const editStudent = (username, forename, surname) => {
  document.getElementById('editModalTitle').innerText = 'Edit ' + username;

  document.getElementById('oldUsername').value = username;

  document.getElementById('editUsername').setAttribute('placeholder', username);
  document.getElementById('lblUsername').innerText = username;

  document.getElementById('editForename').setAttribute('placeholder', forename);
  document.getElementById('lblForename').innerText = forename;

  document.getElementById('editSurname').setAttribute('placeholder', surname);
  document.getElementById('lblSurname').innerText = surname;
  document
    .getElementById('editPassword')
    .setAttribute('placeholder', 'password');
  document
    .getElementById('editPasswordConfirm')
    .setAttribute('placeholder', 'confirm password');
  editModal.toggle();
};

from lms.controllers.student_controller import get_student_by_name



test = get_student_by_name("Chris Hayden")
print(test[0].courses['Phrasal Verbs and Idioms']['grade'])

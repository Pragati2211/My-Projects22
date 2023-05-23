# Name: Pragati Patidar             Student_id : s3858702
# Highest level i have attempted 100% till DI level and tried upto HD level.
# i tried my level best, some condition might not work in Hd level.
# i considered one space in all txt files between cells and 1 new line in rows(if txt files have more space in cell values, it will affect
# printing tabular data)

#imported important libraries
import os
import sys
import datetime
#2D array for students' marks
students_marks = [[99,75,85,62], [-1,92,67,52]]

# defining main class school
class School:
    """
    School class contains all the information about students and the available course
    """
    # defiing Constructor
    def __init__(self, courses_list, students_list, marks_list):
        """
        school class constructor method
        """
        # array for storing students information and course information
        self.courses_list = []
        self.students_list = []
        self.marks_list = []
        self.course_marks = {}
        self.students_report = {}
    # defining method for checking whether .txt file is available or not.
    def check_file_exists(self, file_name):
        """
        check file exists or not
        """
        is_file_available = os.path.exists(file_name)
        return is_file_available

    # defining method for reading scores.txt file
    def read_scores(self, file_name):
        """
        read students score
        """
        # reading file line by line
        read_file= open(file_name)
        line_from_file= read_file.readline()
        # data will append in array using append function
        all_rows = []
        while(line_from_file):
            all_rows.append(line_from_file)
            score_row = line_from_file.replace("\r\n","").strip().split(" ")
            # condition for course and student id
            if not self.courses_list:
                self.courses_list.extend(score_row[1:])
            if score_row[0].startswith("S"):
                self.students_list.extend(score_row[:1])
                self.marks_list.append(score_row)

            line_from_file= read_file.readline()
        #storing data in variable, iterating all rows
        courses_wise_marks = list(zip(*[row.replace("\r\n","").strip().split(" ") for row in all_rows]))[::-1]
        # iterating course details
        for course_mark in courses_wise_marks:
            if course_mark[0] not in self.course_marks and course_mark[0].startswith("C"):
                self.course_marks[course_mark[0]] = course_mark[1:]
        #  variable for excluding -1 and --(888) from marks
        excluded_subjects_list = ["-1", "--"]
        # iterating marks for mark list
        for student_marks in self.marks_list:
            # condition for checking marks
            if student_marks[0] not in self.students_report:
                enrolled_subjects = [i for i in student_marks if not i in excluded_subjects_list and not i.startswith("S")]
                self.students_report[student_marks[0]] = enrolled_subjects
        # file closed
        read_file.close()
        print("\n")
    # method for displaying scores of student in tabular form
    def display_tabular_data(self, file_name):
        """
        display data in tabular format
        """
        # inserting by index
        self.courses_list.insert(0, "")
        comined_list = [self.courses_list]
        # adding marks course wise
        final_list = comined_list + self.marks_list
        # iterating items
        length_list = [len(element) for row in final_list for element in row]
        column_width = max(length_list)
        # adding cells
        count = 0
 # condition for marks, if 888 means result is pending and -1 means student has not enrolled
        for row in final_list:
            new_items = ["--" if x == "888" else " " if x == "-1" else x for x in row]
            row = "".join(element.ljust(column_width + 2) for element in new_items)
            count = count + 1
            print(row)
            if count == 1 or count == (len(final_list) + 1):
                print('-' * 45)
        print('-' * 45)

# class student will inherit the properties of class school
class Students(School):
    """
    student class contains information about school
    """
    def __init__(self, students):
        """
        student class constructor
        """
        self.students = students


    def read_students(self, file_name):
        """
        students information
        """
        # reding file line by line and appending the data in array
        read_file = open(file_name)
        line_from_file = read_file.readline()
        while(line_from_file):
            student_row = line_from_file.replace("\r\n","").strip().split(" ")
            self.students.append(student_row)
            line_from_file= read_file.readline()
        # file closing
        read_file.close()
        print("\n")
        return self.students
    # method for sum of students
    def get_total_studets(self, students_list):
        """
        """
        return len(students_list)
    # method for finding top student based on scores
    def get_top_student(self, marks_list):
        """
        Top scores of a student excluding -1 and 888
        """
        student_marks_dict = {}
        for student_marks in marks_list:
            student_marks_dict[student_marks[0]] = sum([int(i) for i in student_marks[1:]  if i != "888" and i != "-1" and i != "--"])

        return student_marks_dict


    def get_student_cgpa(self, student_marks_list):
        """
        get student cgpa
        """
        # cgpa_dict = {}
       # initializing value in variable
        cgpa = 0
        # condition for  cgpa
        for sub_marks in student_marks_list:
            # condition for
            # condition  for calculating cgpa if marks are greater than 80, got HD and adding 4 in cgpa
            # applied for every given condition
            if int(sub_marks) > 80:
                cgpa = cgpa + 4
            if int(sub_marks) >= 70 and int(sub_marks) < 80:
                cgpa = cgpa + 3
            if int(sub_marks) >= 60 and int(sub_marks) < 70:
                cgpa = cgpa + 2
            if int(sub_marks) >= 50 and int(sub_marks) < 60:
                cgpa = cgpa + 1
        # calculating overall cgpa
        student_cgpa = round(cgpa / len(student_marks_list), 2)
        return student_cgpa
    # method for minimum subject requirement criteria
    def get_student_minimum_sub_requirement(self, student_type, total_enrolled_sub):
        """
        get the student_minimum_sub_requirement
        """
        #condition for full time and part time student, atleast 3 subject are compulsory for full time student
        # for part time atleast 2 subject
        if student_type == "FT":
            return total_enrolled_sub >= 3
        else:
            return total_enrolled_sub >= 2


    # generating student's report
    def generate_student_report(self, all_students, student_report):
        """
        generate students report
        """
        # itirating students details
        for student in all_students:
            # adding marks in report
            student_marks_list = student_report[student[0]]
            # adding subject details
            enrolled_sub = len(student_marks_list)
            # adding cgpa
            student_cgpa = self.get_student_cgpa(student_marks_list)
            # condition for miimum requirement
            is_minimum_requirement = self.get_student_minimum_sub_requirement(student[2], len(student_marks_list))
            if not is_minimum_requirement:
                enrolled_sub = str(enrolled_sub) + '   !'

            student.extend((str(enrolled_sub), str(student_cgpa)))
        # headers for report
        final_list = [["SID", "Name", "Mode",  "Enl.", "GPA"]] + all_students
        length_list = [len(element) for row in final_list for element in row]
        column_width = max(length_list)
        count = 0
        # generating report.txt file writing and appending
        students_file = open("students_report.txt", "a")
        # Adding data and time
        today = datetime.datetime.now()
        students_file.write("{:%d/%m/%Y %H:%M}".format(today))
        students_file.write("\n")
        # condition for not enrolled and result pending
        for row in final_list:
            new_items = ["--" if x == "888" else " " if x == "-1" else x for x in row]
            row = "".join(element.ljust(column_width + 2) for element in new_items)
            # for printing in format
            count = count + 1
            print(row)
            if count == 1 or count == (len(final_list) + 1):
                print('-' * 75)

            if count != 1:
                students_file.write("\n")
                students_file.write("".join(row))
        students_file.write("\n")
        print('-' * 75)
        print("students_report.txt generated!")
        students_file.write("\n")



# defining class course which inherit all the properties of class school
class Courses(School):
    """
    get courses details
    course c1 - cumpulsory, elective

    """
    # definig constructor
    def __init__(self, courses):
        """
        course class constructor
        """
        self.courses = []
        # self.course_marks = {}
    # method for  reading course.txt line by line
    def read_course(self, file_name):
        """
        """
        # open file and read line by line
        read_file= open(file_name)
        line_from_file= read_file.readline()
        while(line_from_file):
            course_row = line_from_file.replace("\r\n","").strip().split(" ")
            self.courses.append(course_row)
            line_from_file= read_file.readline()
         # closing of file
        read_file.close()
        print("\n")

     # method for calculating total course
    def get_total_course(self, courses_list):
        """
        get the total course count
        """
        available_course = [item for item in courses_list if item]
        return len(available_course)

    # method for calculating average course marks
    def get_courses_avg_marks(self, courses_marks):
        """
        get the avg marks of all the courses
        """
        # initializing dictionary
        course_dict = {}
        # itirating items
        for key, value in courses_marks.items():
            if key not in course_dict:
                count = 0
                total_marks = 0
                # condition for marks, excluding -1 and -- from average
                for val in value:
                    if val != "-1" and val != "888" and val != "--":
                        count = count + 1
                        total_marks = total_marks + float(val)
                # updating in dictionary
                if count > 0:
                    course_dict[key] = (count, round((total_marks/count),2))
                else:
                    course_dict[key] = (0, '--')

        return course_dict
    #  method for generating course report
    def generate_course_report(self, all_courses, courses_avg_marks):
        """
        """
        # itirating items of courses and condtion for elective and compusory
        for course in all_courses:
            if course[2].startswith("E"):
                course.insert(1, '-')
            else:
                course.insert(1, '*')
            course.remove(course[3])
            enrolled_students_count, course_avg = courses_avg_marks[course[0]]
            course.extend((str(enrolled_students_count), str(course_avg)))

        # adding headers in the report
        final_list = [["CID", " ", "Name", "Pt.",  "Enl.", "Avg."]] + all_courses
        length_list = [len(element) for row in final_list for element in row]
        column_width = max(length_list)
        count = 0
        file1 = open("course_report.txt", "a")
        # Adding data and time
        today = datetime.datetime.now()
        file1.write("{:%d/%m/%Y %H:%M}".format(today))

        file1.write("\n")
        # itirating all items and appling condition for -1 and 888
        for row in final_list:
            new_items = ["--" if x == "888" else "" if x == "-1" else x for x in row]
            row = "".join(element.ljust(column_width + 2) for element in new_items)
            count = count + 1
            print(row)
            if count == 1 or count == (len(all_courses) + 1):
                print('-'*75)
            if count != 1:
                file1.write("\n")
                file1.write("".join(row))
        file1.write("\n")
        print("course_report.txt generated!")
        file1.write("\n")


    # method for worst performing course
    def get_worst_performing_course(self, all_courses):
        """
        get the worst performing course
        """
        # calculating minimum marks
        min_marks = all_courses[0][-1]
        min_marks_sub = all_courses[0][0]
        for course in all_courses:
            if course[-1] == '--':
                continue
            #condition for marks
            if min_marks > course[-1]:
                min_marks = course[-1]
                min_marks_sub = course[0]

        return min_marks_sub, min_marks

# creating object for class school
school_obj = School("", "","")
# command line arguments
cmd_args = sys.argv

# if argument is greater than one then print scores.txt
if len(cmd_args) > 1:
    score_file = cmd_args[1]
    is_file_available = school_obj.check_file_exists(score_file)
    # if file is not available print message
    if not is_file_available:
        print("[Usage:] Python my_school.py <scores file>")
        exit()
    # calling all methods by class object
    school_obj.read_scores(score_file)
    school_obj.display_tabular_data(score_file)
    student_obj = Students([])
    courses_obj = Courses("")
    total_courses = courses_obj.get_total_course(school_obj.courses_list)
    total_students = student_obj.get_total_studets(school_obj.students_list)
    top_student_marks = student_obj.get_top_student(school_obj.marks_list)
    student_name, student_total_marks = max(top_student_marks.items(), key = lambda k : k[1])
    top_student_avg_marks = student_total_marks/total_courses
    print("{} students, {} courses, the top student is {}, average {}".format(total_students,total_courses,student_name, top_student_avg_marks))
else:
    school_obj.check_file_exists("")
    print("[Usage:] Python my_school.py <scores file>")
    exit()
# if argument is greater then 2 then print course file and generate report
if len(cmd_args) > 2:
    course_file = cmd_args[2]
    is_file_available = school_obj.check_file_exists(course_file)
    if not is_file_available:
        print("\n")
        print("[Usage:] Python my_school.py <courses file>")
        exit()
    # calling all methods of class via object
    courses_obj.read_course(course_file)
    all_courses = courses_obj.courses
    courses_avg_marks = courses_obj.get_courses_avg_marks(school_obj.course_marks)
    courses_obj.generate_course_report(all_courses, courses_avg_marks)
    min_marks_course, min_marks = courses_obj.get_worst_performing_course(all_courses)
    print("The worse performing course is {} with an average {}".format(min_marks_course, min_marks))
    
# if argument is greater then 2 then print course file and generate report
if len(cmd_args) > 3:
    students_file = cmd_args[3]
    is_file_available = school_obj.check_file_exists(students_file)
    if not is_file_available:
        print("\n")
        print("[Usage:] Python my_school.py <students file>")
        exit()
        #calling all methods by class objects
    all_students = student_obj.read_students(students_file)
    student_obj.generate_student_report(all_students, school_obj.students_report)




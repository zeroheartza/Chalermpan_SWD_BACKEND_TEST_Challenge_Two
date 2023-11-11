
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.models import SchoolStructure, Schools, Classes, Personnel, Subjects, StudentSubjectsScore
from ..serializers import CreateStudentSubjectsScoreSerializer,CategoryTreeSerializer
from django.db.models import Q 
import operator 

class StudentSubjectsScoreAPIView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        """
        [Backend API and Data Validations Skill Test]

        description: create API Endpoint for insert score data of each student by following rules.

        rules:      - Score must be number, equal or greater than 0 and equal or less than 100.
                    - Credit must be integer, greater than 0 and equal or less than 3.
                    - Payload data must be contained `first_name`, `last_name`, `subject_title` and `score`.
                        - `first_name` in payload must be string (if not return bad request status).
                        - `last_name` in payload must be string (if not return bad request status).
                        - `subject_title` in payload must be string (if not return bad request status).
                        - `score` in payload must be number (if not return bad request status).

                    - Student's score of each subject must be unique (it's mean 1 student only have 1 row of score
                            of each subject).
                    - If student's score of each subject already existed, It will update new score
                            (Don't created it).
                    - If Update, Credit must not be changed.
                    - If Data Payload not complete return clearly message with bad request status.
                    - If Subject's Name or Student's Name not found in Database return clearly message with bad request status.
                    - If Success return student's details, subject's title, credit and score context with created status.

        remark:     - `score` is subject's score of each student.
                    - `credit` is subject's credit.
                    - student's first name, lastname and subject's title can find in DATABASE (you can create more
                            for test add new score).

        """

        subjects_context = [{"id": 1, "title": "Math"}, {"id": 2, "title": "Physics"}, {"id": 3, "title": "Chemistry"},
                            {"id": 4, "title": "Algorithm"}, {"id": 5, "title": "Coding"}]

        credits_context = [{"id": 6, "credit": 1, "subject_id_list_that_using_this_credit": [3]},
                           {"id": 7, "credit": 2, "subject_id_list_that_using_this_credit": [2, 4]},
                           {"id": 9, "credit": 3, "subject_id_list_that_using_this_credit": [1, 5]}]

        credits_mapping = [{"subject_id": 1, "credit_id": 9}, {"subject_id": 2, "credit_id": 7},
                           {"subject_id": 3, "credit_id": 6}, {"subject_id": 4, "credit_id": 7},
                           {"subject_id": 5, "credit_id": 9}]

        # student_first_name = request.data.get("first_name", None)
        # student_last_name = request.data.get("last_name", None)
        # subject_title = request.data.get("subject_title", None)
        # score = request.data.get("score", None)

        createStudentSubjectsScoreSerializer = CreateStudentSubjectsScoreSerializer(request.data)

        try:   
            personnel = Personnel.objects.get(first_name=createStudentSubjectsScoreSerializer.data['first_name'], last_name=createStudentSubjectsScoreSerializer.data['last_name'])

        except Personnel.DoesNotExist:  
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

        try:   
            subjects = Subjects.objects.get(title=createStudentSubjectsScoreSerializer.data['subject_title'])

        except Subjects.DoesNotExist:  
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:   
            studentSubjectsScore = StudentSubjectsScore.objects.get(student=personnel,subjects=subjects)
            studentSubjectsScore.score = createStudentSubjectsScoreSerializer.data['score']
            studentSubjectsScore.save()
        except StudentSubjectsScore.DoesNotExist:  
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

        return Response({"student_id":personnel.id}, status=status.HTTP_201_CREATED)



class StudentSubjectsScoreDetailsAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Backend API and Data Calculation Skill Test]

        description: get student details, subject's details, subject's credit, their score of each subject,
                    their grade of each subject and their grade point average by student's ID.

        pattern:     Data pattern in 'context_data' variable below.

        remark:     - `grade` will be A  if 80 <= score <= 100
                                      B+ if 75 <= score < 80
                                      B  if 70 <= score < 75
                                      C+ if 65 <= score < 70
                                      C  if 60 <= score < 65
                                      D+ if 55 <= score < 60
                                      D  if 50 <= score < 55
                                      F  if score < 50

        """

        student_id = kwargs.get("id", None)
        print(student_id)
        try:   
            personnel = Personnel.objects.get(id=student_id)
            full_name = personnel.first_name + " " + personnel.last_name
            student_id = personnel.id
            school_name = personnel.school_class.school.title
            
        except Personnel.DoesNotExist:  
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
       
        studentSubjectsScore = StudentSubjectsScore.objects.filter(student=personnel)
        subject_detail = []
        
        total_score =  0
        for stds in studentSubjectsScore:
            subject = stds.subjects.title
            score = stds.score
            credit = stds.credit
            print(score)
            total_score+=score

            if score >= 80:
                grade =('Grade A')
            elif score >= 75:
                grade =('Grade B+')
            elif score >= 70:
                grade =('Grade B')
            elif score >= 65:
                grade =('Grade C+')
            elif score >= 60:
                grade =('Grade C')
            elif score >= 55:
                grade =('Grade D+')
            elif score >= 50:
                grade =('Grade D')
            else:
                grade =('Grade F')
            print(grade)
            data = {
                    "subject": subject,
                    "credit": credit,
                    "score": score,
                    "grade": grade,
                }
            subject_detail.append(data)

        avg_score = total_score/len(studentSubjectsScore)
        if avg_score >= 80:
            avg_grade =('Grade A')
        elif avg_score >= 75:
            avg_grade =('Grade B+')
        elif avg_score >= 70:
            avg_grade =('Grade B')
        elif avg_score >= 65:
            avg_grade =('Grade C+')
        elif avg_score >= 60:
            avg_grade =('Grade C')
        elif avg_score >= 55:
            avg_grade =('Grade D+')
        elif avg_score >= 50:
            avg_grade =('Grade D')
        else:
            avg_grade =('Grade F')

        example_context_data = {
            "student":
                {
                    "id": student_id,
                    "full_name": full_name,
                    "school": school_name
                },

            "subject_detail": subject_detail,

            "grade_point_average": avg_grade,
        }

        # example_context_data = {
        #     "student":
        #         {
        #             "id": "primary key of student in database",
        #             "full_name": "student's full name",
        #             "school": "student's school name"
        #         },

        #     "subject_detail": [
        #         {
        #             "subject": "subject's title 1",
        #             "credit": "subject's credit 1",
        #             "score": "subject's score 1",
        #             "grade": "subject's grade 1",
        #         },
        #         {
        #             "subject": "subject's title 2",
        #             "credit": "subject's credit 2",
        #             "score": "subject's score 2",
        #             "grade": "subject's grade 2",
        #         },
        #     ],

        #     "grade_point_average": "grade point average",
        # }

        return Response(example_context_data, status=status.HTTP_200_OK)


class PersonnelDetailsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        [Basic Skill and Observational Skill Test]

        description: get personnel details by school's name.

        data pattern:  {order}. school: {school's title}, role: {personnel type in string}, class: {class's order}, name: {first name} {last name}.

        result pattern : in `data_pattern` variable below.

        example:    1. school: Rose Garden School, role: Head of the room, class: 1, name: Reed Richards.
                    2. school: Rose Garden School, role: Student, class: 1, name: Blackagar Boltagon.

        rules:      - Personnel's name and School's title must be capitalize.
                    - Personnel's details order must be ordered by their role, their class order and their name.

        """
        school_title = kwargs.get("school_title", None)

        your_result = []

        
        personnel = Personnel.objects.filter().order_by('personnel_type')  
        personnel_in_school_title = [x for x in personnel if x.school_class.school.title==school_title]
       

        for i,pers in enumerate(personnel_in_school_title):
            data_pattern = "{order}. school: {school_title}, role: {personnel_type}, class: {class_order}, name: {first_name} {last_name}.".format(
                order=(i+1),school_title=school_title,personnel_type=pers.get_personnel_type_display(),class_order=pers.school_class.class_order,first_name=pers.first_name,last_name=pers.last_name)
            your_result.append(data_pattern)

      
        # data_pattern = [
        #     "1. school: Dorm Palace School, role: Teacher, class: 1,name: Mark Harmon",
        #     "2. school: Dorm Palace School, role: Teacher, class: 2,name: Jared Sanchez",
        #     "3. school: Dorm Palace School, role: Teacher, class: 3,name: Cheyenne Woodard",
        #     "4. school: Dorm Palace School, role: Teacher, class: 4,name: Roger Carter",
        #     "5. school: Dorm Palace School, role: Teacher, class: 5,name: Cynthia Mclaughlin",
        #     "6. school: Dorm Palace School, role: Head of the room, class: 1,name: Margaret Graves",
        #     "7. school: Dorm Palace School, role: Head of the room, class: 2,name: Darren Wyatt",
        #     "8. school: Dorm Palace School, role: Head of the room, class: 3,name: Carla Elliott",
        #     "9. school: Dorm Palace School, role: Head of the room, class: 4,name: Brittany Mullins",
        #     "10. school: Dorm Palace School, role: Head of the room, class: 5,name: Nathan Solis",
        #     "11. school: Dorm Palace School, role: Student, class: 1,name: Aaron Marquez",
        #     "12. school: Dorm Palace School, role: Student, class: 1,name: Benjamin Collins",
        #     "13. school: Dorm Palace School, role: Student, class: 1,name: Carolyn Reynolds",
        #     "14. school: Dorm Palace School, role: Student, class: 1,name: Christopher Austin",
        #     "15. school: Dorm Palace School, role: Student, class: 1,name: Deborah Mcdonald",
        #     "16. school: Dorm Palace School, role: Student, class: 1,name: Jessica Burgess",
        #     "17. school: Dorm Palace School, role: Student, class: 1,name: Jonathan Oneill",
        #     "18. school: Dorm Palace School, role: Student, class: 1,name: Katrina Davis",
        #     "19. school: Dorm Palace School, role: Student, class: 1,name: Kristen Robinson",
        #     "20. school: Dorm Palace School, role: Student, class: 1,name: Lindsay Haas",
        #     "21. school: Dorm Palace School, role: Student, class: 2,name: Abigail Beck",
        #     "22. school: Dorm Palace School, role: Student, class: 2,name: Andrew Williams",
        #     "23. school: Dorm Palace School, role: Student, class: 2,name: Ashley Berg",
        #     "24. school: Dorm Palace School, role: Student, class: 2,name: Elizabeth Anderson",
        #     "25. school: Dorm Palace School, role: Student, class: 2,name: Frank Mccormick",
        #     "26. school: Dorm Palace School, role: Student, class: 2,name: Jason Leon",
        #     "27. school: Dorm Palace School, role: Student, class: 2,name: Jessica Fowler",
        #     "28. school: Dorm Palace School, role: Student, class: 2,name: John Smith",
        #     "29. school: Dorm Palace School, role: Student, class: 2,name: Nicholas Smith",
        #     "30. school: Dorm Palace School, role: Student, class: 2,name: Scott Mckee",
        #     "31. school: Dorm Palace School, role: Student, class: 3,name: Abigail Smith",
        #     "32. school: Dorm Palace School, role: Student, class: 3,name: Cassandra Martinez",
        #     "33. school: Dorm Palace School, role: Student, class: 3,name: Elizabeth Anderson",
        #     "34. school: Dorm Palace School, role: Student, class: 3,name: John Scott",
        #     "35. school: Dorm Palace School, role: Student, class: 3,name: Kathryn Williams",
        #     "36. school: Dorm Palace School, role: Student, class: 3,name: Mary Miller",
        #     "37. school: Dorm Palace School, role: Student, class: 3,name: Ronald Mccullough",
        #     "38. school: Dorm Palace School, role: Student, class: 3,name: Sandra Davidson",
        #     "39. school: Dorm Palace School, role: Student, class: 3,name: Scott Martin",
        #     "40. school: Dorm Palace School, role: Student, class: 3,name: Victoria Jacobs",
        #     "41. school: Dorm Palace School, role: Student, class: 4,name: Carol Williams",
        #     "42. school: Dorm Palace School, role: Student, class: 4,name: Cassandra Huff",
        #     "43. school: Dorm Palace School, role: Student, class: 4,name: Deborah Harrison",
        #     "44. school: Dorm Palace School, role: Student, class: 4,name: Denise Young",
        #     "45. school: Dorm Palace School, role: Student, class: 4,name: Jennifer Pace",
        #     "46. school: Dorm Palace School, role: Student, class: 4,name: Joe Andrews",
        #     "47. school: Dorm Palace School, role: Student, class: 4,name: Michael Kelly",
        #     "48. school: Dorm Palace School, role: Student, class: 4,name: Monica Padilla",
        #     "49. school: Dorm Palace School, role: Student, class: 4,name: Tiffany Roman",
        #     "50. school: Dorm Palace School, role: Student, class: 4,name: Wendy Maxwell",
        #     "51. school: Dorm Palace School, role: Student, class: 5,name: Adam Smith",
        #     "52. school: Dorm Palace School, role: Student, class: 5,name: Angela Christian",
        #     "53. school: Dorm Palace School, role: Student, class: 5,name: Cody Edwards",
        #     "54. school: Dorm Palace School, role: Student, class: 5,name: Jacob Palmer",
        #     "55. school: Dorm Palace School, role: Student, class: 5,name: James Gonzalez",
        #     "56. school: Dorm Palace School, role: Student, class: 5,name: Justin Kaufman",
        #     "57. school: Dorm Palace School, role: Student, class: 5,name: Katrina Reid",
        #     "58. school: Dorm Palace School, role: Student, class: 5,name: Melissa Butler",
        #     "59. school: Dorm Palace School, role: Student, class: 5,name: Pamela Sutton",
        #     "60. school: Dorm Palace School, role: Student, class: 5,name: Sarah Murphy"
        # ]

        return Response(your_result, status=status.HTTP_400_BAD_REQUEST)


class SchoolHierarchyAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get personnel list in hierarchy order by school's title, class and personnel's name.

        pattern: in `data_pattern` variable below.

        """
        
        schools = Schools.objects.filter().order_by('title')  
        personnel_tec = Personnel.objects.filter(personnel_type=0)
        personnel_htr = Personnel.objects.filter(personnel_type=1)
        personnel_std = Personnel.objects.filter(personnel_type=2)
        your_result = []
        for sch in schools:
           
            personnel_tec_school_title = [x for x in personnel_tec if x.school_class.school.title== sch.title]
            personnel_tec_school_title = sorted(personnel_tec_school_title, key=lambda k: k.school_class.class_order, reverse=False)
            for ptst in personnel_tec_school_title:
                teacher_full_name = ptst.first_name + " " + ptst.last_name
      
                personnel_htr_school_title = [x for x in personnel_htr if x.school_class.school.title== sch.title and x.school_class.class_order==ptst.school_class.class_order]
                personnel_htr_school_title = sorted(personnel_htr_school_title, key=lambda k: k.first_name + " " + k.last_name, reverse=False)
                personnel_std_school_title = [x for x in personnel_std if x.school_class.school.title== sch.title and x.school_class.class_order==ptst.school_class.class_order ]
                personnel_std_school_title = sorted(personnel_std_school_title, key=lambda k: k.first_name + " " + k.last_name, reverse=False)
                std_arr = []
                for std in personnel_htr_school_title:
                    data = {}
                    data[str(std.get_personnel_type_display())] = std.first_name + " " + std.last_name
                    std_arr.append(data)
                for std in personnel_std_school_title:
                    data = {}
                    data[str(std.get_personnel_type_display())] = std.first_name + " " + std.last_name
                    std_arr.append(data)
             
                data_pattern = {
                    "school":sch.title
                }
                data_pattern[str("class {}".format(str(ptst.school_class.class_order)))]={}
                data_pattern[str("class {}".format(str(ptst.school_class.class_order)))][str("Teacher: {}".format(teacher_full_name))]= std_arr
                your_result.append(data_pattern)

        # data_pattern = [
        #     {
        #         "school": "Dorm Palace School",
        #         "class 1": {
        #             "Teacher: Mark Harmon": [
        #                 {
        #                     "Head of the room": "Margaret Graves"
        #                 },
        #                 {
        #                     "Student": "Aaron Marquez"
        #                 },
        #                 {
        #                     "Student": "Benjamin Collins"
        #                 },
        #                 {
        #                     "Student": "Carolyn Reynolds"
        #                 },
        #                 {
        #                     "Student": "Christopher Austin"
        #                 },
        #                 {
        #                     "Student": "Deborah Mcdonald"
        #                 },
        #                 {
        #                     "Student": "Jessica Burgess"
        #                 },
        #                 {
        #                     "Student": "Jonathan Oneill"
        #                 },
        #                 {
        #                     "Student": "Katrina Davis"
        #                 },
        #                 {
        #                     "Student": "Kristen Robinson"
        #                 },
        #                 {
        #                     "Student": "Lindsay Haas"
        #                 }
        #             ]
        #         },
        #         "class 2": {
        #             "Teacher: Jared Sanchez": [
        #                 {
        #                     "Head of the room": "Darren Wyatt"
        #                 },
        #                 {
        #                     "Student": "Abigail Beck"
        #                 },
        #                 {
        #                     "Student": "Andrew Williams"
        #                 },
        #                 {
        #                     "Student": "Ashley Berg"
        #                 },
        #                 {
        #                     "Student": "Elizabeth Anderson"
        #                 },
        #                 {
        #                     "Student": "Frank Mccormick"
        #                 },
        #                 {
        #                     "Student": "Jason Leon"
        #                 },
        #                 {
        #                     "Student": "Jessica Fowler"
        #                 },
        #                 {
        #                     "Student": "John Smith"
        #                 },
        #                 {
        #                     "Student": "Nicholas Smith"
        #                 },
        #                 {
        #                     "Student": "Scott Mckee"
        #                 }
        #             ]
        #         },
        #         "class 3": {
        #             "Teacher: Cheyenne Woodard": [
        #                 {
        #                     "Head of the room": "Carla Elliott"
        #                 },
        #                 {
        #                     "Student": "Abigail Smith"
        #                 },
        #                 {
        #                     "Student": "Cassandra Martinez"
        #                 },
        #                 {
        #                     "Student": "Elizabeth Anderson"
        #                 },
        #                 {
        #                     "Student": "John Scott"
        #                 },
        #                 {
        #                     "Student": "Kathryn Williams"
        #                 },
        #                 {
        #                     "Student": "Mary Miller"
        #                 },
        #                 {
        #                     "Student": "Ronald Mccullough"
        #                 },
        #                 {
        #                     "Student": "Sandra Davidson"
        #                 },
        #                 {
        #                     "Student": "Scott Martin"
        #                 },
        #                 {
        #                     "Student": "Victoria Jacobs"
        #                 }
        #             ]
        #         },
        #         "class 4": {
        #             "Teacher: Roger Carter": [
        #                 {
        #                     "Head of the room": "Brittany Mullins"
        #                 },
        #                 {
        #                     "Student": "Carol Williams"
        #                 },
        #                 {
        #                     "Student": "Cassandra Huff"
        #                 },
        #                 {
        #                     "Student": "Deborah Harrison"
        #                 },
        #                 {
        #                     "Student": "Denise Young"
        #                 },
        #                 {
        #                     "Student": "Jennifer Pace"
        #                 },
        #                 {
        #                     "Student": "Joe Andrews"
        #                 },
        #                 {
        #                     "Student": "Michael Kelly"
        #                 },
        #                 {
        #                     "Student": "Monica Padilla"
        #                 },
        #                 {
        #                     "Student": "Tiffany Roman"
        #                 },
        #                 {
        #                     "Student": "Wendy Maxwell"
        #                 }
        #             ]
        #         },
        #         "class 5": {
        #             "Teacher: Cynthia Mclaughlin": [
        #                 {
        #                     "Head of the room": "Nathan Solis"
        #                 },
        #                 {
        #                     "Student": "Adam Smith"
        #                 },
        #                 {
        #                     "Student": "Angela Christian"
        #                 },
        #                 {
        #                     "Student": "Cody Edwards"
        #                 },
        #                 {
        #                     "Student": "Jacob Palmer"
        #                 },
        #                 {
        #                     "Student": "James Gonzalez"
        #                 },
        #                 {
        #                     "Student": "Justin Kaufman"
        #                 },
        #                 {
        #                     "Student": "Katrina Reid"
        #                 },
        #                 {
        #                     "Student": "Melissa Butler"
        #                 },
        #                 {
        #                     "Student": "Pamela Sutton"
        #                 },
        #                 {
        #                     "Student": "Sarah Murphy"
        #                 }
        #             ]
        #         }
        #     },
        #     {
        #         "school": "Prepare Udom School",
        #         "class 1": {
        #             "Teacher: Joshua Frazier": [
        #                 {
        #                     "Head of the room": "Tina Phillips"
        #                 },
        #                 {
        #                     "Student": "Amanda Howell"
        #                 },
        #                 {
        #                     "Student": "Colin George"
        #                 },
        #                 {
        #                     "Student": "Donald Stephens"
        #                 },
        #                 {
        #                     "Student": "Jennifer Lewis"
        #                 },
        #                 {
        #                     "Student": "Jorge Bowman"
        #                 },
        #                 {
        #                     "Student": "Kevin Hooper"
        #                 },
        #                 {
        #                     "Student": "Kimberly Lewis"
        #                 },
        #                 {
        #                     "Student": "Mary Sims"
        #                 },
        #                 {
        #                     "Student": "Ronald Tucker"
        #                 },
        #                 {
        #                     "Student": "Victoria Velez"
        #                 }
        #             ]
        #         },
        #         "class 2": {
        #             "Teacher: Zachary Anderson": [
        #                 {
        #                     "Head of the room": "Joseph Zimmerman"
        #                 },
        #                 {
        #                     "Student": "Alicia Serrano"
        #                 },
        #                 {
        #                     "Student": "Andrew West"
        #                 },
        #                 {
        #                     "Student": "Anthony Hartman"
        #                 },
        #                 {
        #                     "Student": "Dominic Frey"
        #                 },
        #                 {
        #                     "Student": "Gina Fernandez"
        #                 },
        #                 {
        #                     "Student": "Jennifer Riley"
        #                 },
        #                 {
        #                     "Student": "John Joseph"
        #                 },
        #                 {
        #                     "Student": "Katherine Cantu"
        #                 },
        #                 {
        #                     "Student": "Keith Watts"
        #                 },
        #                 {
        #                     "Student": "Phillip Skinner"
        #                 }
        #             ]
        #         },
        #         "class 3": {
        #             "Teacher: Steven Hunt": [
        #                 {
        #                     "Head of the room": "Antonio Hodges"
        #                 },
        #                 {
        #                     "Student": "Brian Lewis"
        #                 },
        #                 {
        #                     "Student": "Christina Wiggins"
        #                 },
        #                 {
        #                     "Student": "Christine Parker"
        #                 },
        #                 {
        #                     "Student": "Hannah Wilson"
        #                 },
        #                 {
        #                     "Student": "Jasmin Odom"
        #                 },
        #                 {
        #                     "Student": "Jeffery Graves"
        #                 },
        #                 {
        #                     "Student": "Mark Roberts"
        #                 },
        #                 {
        #                     "Student": "Paige Pearson"
        #                 },
        #                 {
        #                     "Student": "Philip Fowler"
        #                 },
        #                 {
        #                     "Student": "Steven Riggs"
        #                 }
        #             ]
        #         },
        #         "class 4": {
        #             "Teacher: Rachael Davenport": [
        #                 {
        #                     "Head of the room": "John Cunningham"
        #                 },
        #                 {
        #                     "Student": "Aaron Olson"
        #                 },
        #                 {
        #                     "Student": "Amanda Cuevas"
        #                 },
        #                 {
        #                     "Student": "Gary Smith"
        #                 },
        #                 {
        #                     "Student": "James Blair"
        #                 },
        #                 {
        #                     "Student": "Juan Boone"
        #                 },
        #                 {
        #                     "Student": "Julie Bowman"
        #                 },
        #                 {
        #                     "Student": "Melissa Williams"
        #                 },
        #                 {
        #                     "Student": "Phillip Bright"
        #                 },
        #                 {
        #                     "Student": "Sonia Gregory"
        #                 },
        #                 {
        #                     "Student": "William Martin"
        #                 }
        #             ]
        #         },
        #         "class 5": {
        #             "Teacher: Amber Clark": [
        #                 {
        #                     "Head of the room": "Mary Mason"
        #                 },
        #                 {
        #                     "Student": "Allen Norton"
        #                 },
        #                 {
        #                     "Student": "Eric English"
        #                 },
        #                 {
        #                     "Student": "Jesse Johnson"
        #                 },
        #                 {
        #                     "Student": "Kevin Martinez"
        #                 },
        #                 {
        #                     "Student": "Mark Hughes"
        #                 },
        #                 {
        #                     "Student": "Robert Sutton"
        #                 },
        #                 {
        #                     "Student": "Sherri Patrick"
        #                 },
        #                 {
        #                     "Student": "Steven Brown"
        #                 },
        #                 {
        #                     "Student": "Valerie Mcdaniel"
        #                 },
        #                 {
        #                     "Student": "William Roman"
        #                 }
        #             ]
        #         }
        #     },
        #     {
        #         "school": "Rose Garden School",
        #         "class 1": {
        #             "Teacher: Danny Clements": [
        #                 {
        #                     "Head of the room": "Troy Rodriguez"
        #                 },
        #                 {
        #                     "Student": "Annette Ware"
        #                 },
        #                 {
        #                     "Student": "Daniel Collins"
        #                 },
        #                 {
        #                     "Student": "Jacqueline Russell"
        #                 },
        #                 {
        #                     "Student": "Justin Kennedy"
        #                 },
        #                 {
        #                     "Student": "Lance Martinez"
        #                 },
        #                 {
        #                     "Student": "Maria Bennett"
        #                 },
        #                 {
        #                     "Student": "Mary Crawford"
        #                 },
        #                 {
        #                     "Student": "Rodney White"
        #                 },
        #                 {
        #                     "Student": "Timothy Kline"
        #                 },
        #                 {
        #                     "Student": "Tracey Nichols"
        #                 }
        #             ]
        #         },
        #         "class 2": {
        #             "Teacher: Ray Khan": [
        #                 {
        #                     "Head of the room": "Stephen Johnson"
        #                 },
        #                 {
        #                     "Student": "Ashley Jones"
        #                 },
        #                 {
        #                     "Student": "Breanna Baker"
        #                 },
        #                 {
        #                     "Student": "Brian Gardner"
        #                 },
        #                 {
        #                     "Student": "Elizabeth Shaw"
        #                 },
        #                 {
        #                     "Student": "Jason Walker"
        #                 },
        #                 {
        #                     "Student": "Katherine Campbell"
        #                 },
        #                 {
        #                     "Student": "Larry Tate"
        #                 },
        #                 {
        #                     "Student": "Lawrence Marshall"
        #                 },
        #                 {
        #                     "Student": "Malik Dean"
        #                 },
        #                 {
        #                     "Student": "Taylor Mckee"
        #                 }
        #             ]
        #         },
        #         "class 3": {
        #             "Teacher: Jennifer Diaz": [
        #                 {
        #                     "Head of the room": "Vicki Wallace"
        #                 },
        #                 {
        #                     "Student": "Brenda Montgomery"
        #                 },
        #                 {
        #                     "Student": "Daniel Wilson"
        #                 },
        #                 {
        #                     "Student": "David Dixon"
        #                 },
        #                 {
        #                     "Student": "John Robinson"
        #                 },
        #                 {
        #                     "Student": "Kimberly Smith"
        #                 },
        #                 {
        #                     "Student": "Michael Miller"
        #                 },
        #                 {
        #                     "Student": "Miranda Trujillo"
        #                 },
        #                 {
        #                     "Student": "Sara Bruce"
        #                 },
        #                 {
        #                     "Student": "Scott Williams"
        #                 },
        #                 {
        #                     "Student": "Taylor Levy"
        #                 }
        #             ]
        #         },
        #         "class 4": {
        #             "Teacher: Kendra Pierce": [
        #                 {
        #                     "Head of the room": "Christopher Stone"
        #                 },
        #                 {
        #                     "Student": "Brenda Tanner"
        #                 },
        #                 {
        #                     "Student": "Christopher Garcia"
        #                 },
        #                 {
        #                     "Student": "Curtis Flynn"
        #                 },
        #                 {
        #                     "Student": "Jason Horton"
        #                 },
        #                 {
        #                     "Student": "Julie Mullins"
        #                 },
        #                 {
        #                     "Student": "Kathleen Mckenzie"
        #                 },
        #                 {
        #                     "Student": "Larry Briggs"
        #                 },
        #                 {
        #                     "Student": "Michael Moyer"
        #                 },
        #                 {
        #                     "Student": "Tammy Smith"
        #                 },
        #                 {
        #                     "Student": "Thomas Martinez"
        #                 }
        #             ]
        #         },
        #         "class 5": {
        #             "Teacher: Elizabeth Hebert": [
        #                 {
        #                     "Head of the room": "Caitlin Lee"
        #                 },
        #                 {
        #                     "Student": "Alexander James"
        #                 },
        #                 {
        #                     "Student": "Amanda Weber"
        #                 },
        #                 {
        #                     "Student": "Christopher Clark"
        #                 },
        #                 {
        #                     "Student": "Devin Morgan"
        #                 },
        #                 {
        #                     "Student": "Gary Clark"
        #                 },
        #                 {
        #                     "Student": "Jenna Sanchez"
        #                 },
        #                 {
        #                     "Student": "Jeremy Meyers"
        #                 },
        #                 {
        #                     "Student": "John Dunn"
        #                 },
        #                 {
        #                     "Student": "Loretta Thomas"
        #                 },
        #                 {
        #                     "Student": "Matthew Vaughan"
        #                 }
        #             ]
        #         }
        #     }
        # ]


        return Response(your_result, status=status.HTTP_200_OK)


class SchoolStructureAPIView(APIView):
     
    
    
    @staticmethod
    def get(request, *args, **kwargs):
    
        queryset = SchoolStructure.objects.all()
        
        serializer = CategoryTreeSerializer(queryset, many=True)
        your_result = []
        sub_arr= []
        sub_arr2= []
        start = 0
        now_title = ""
        now_title2 = ""
        structure_data=serializer.data
        old_parent = 0
        for i in range(len(structure_data)):
            if(structure_data[i]['parent'] is None):
                now_title = structure_data[i]['title']
                data = {
                    "title":structure_data[i]['title'],
                    "sub":[]
                }
                your_result.append(data)
                old_parent = 0
            if(i>0):
                if(structure_data[i-1]['parent'] is None):
                    for x in your_result:
                        if(x["title"]==str(now_title)):
                            now_title2 = structure_data[i]['title']
                            data_a = {
                            "title":structure_data[i]['title'],
                            "sub":[]
                            }
                            x["sub"].append(data_a)
                    old_parent = structure_data[i]['parent']  if structure_data[i]['parent'] is not None else 0
                else:
                
                    if((structure_data[i]['parent'] if structure_data[i]['parent'] is not None else 0)<old_parent):
                        for x in your_result:
                            if(x["title"]==str(now_title)):
                                now_title2 = structure_data[i]['title']
                                data_a = {
                                "title":structure_data[i]['title'],
                                "sub":[]
                                }
                                x["sub"].append(data_a)
                    
                        old_parent = structure_data[i]['parent'] if structure_data[i]['parent'] is not None else 0
                    else:
                        for x in your_result:
                            if(x["title"]==str(now_title)):
                                for y in x["sub"]:
                                    if(y["title"]==str(now_title2)):
                                        data_b = {
                                        "title":structure_data[i]['title'],
                                        
                                        }
                                        y["sub"].append(data_b)
                    
                        old_parent = structure_data[i]['parent'] if structure_data[i]['parent'] is not None else 0


        """
        [Logical Test]

        description: get School's structure list in hierarchy.

        pattern: in `data_pattern` variable below.

        """
      
          

        

            
        # data_pattern = [
        #     {
        #         "title": "มัธยมต้น",
        #         "sub": [
        #             {
        #                 "title": "ม.1",
        #                 "sub": [
        #                     {
        #                         "title": "ห้อง 1/1"
        #                     },
        #                     {
        #                         "title": "ห้อง 1/2"
        #                     },
        #                     {
        #                         "title": "ห้อง 1/3"
        #                     },
        #                     {
        #                         "title": "ห้อง 1/4"
        #                     },
        #                     {
        #                         "title": "ห้อง 1/5"
        #                     },
        #                     {
        #                         "title": "ห้อง 1/6"
        #                     },
        #                     {
        #                         "title": "ห้อง 1/7"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "title": "ม.2",
        #                 "sub": [
        #                     {
        #                         "title": "ห้อง 2/1"
        #                     },
        #                     {
        #                         "title": "ห้อง 2/2"
        #                     },
        #                     {
        #                         "title": "ห้อง 2/3"
        #                     },
        #                     {
        #                         "title": "ห้อง 2/4"
        #                     },
        #                     {
        #                         "title": "ห้อง 2/5"
        #                     },
        #                     {
        #                         "title": "ห้อง 2/6"
        #                     },
        #                     {
        #                         "title": "ห้อง 2/7"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "title": "ม.3",
        #                 "sub": [
        #                     {
        #                         "title": "ห้อง 3/1"
        #                     },
        #                     {
        #                         "title": "ห้อง 3/2"
        #                     },
        #                     {
        #                         "title": "ห้อง 3/3"
        #                     },
        #                     {
        #                         "title": "ห้อง 3/4"
        #                     },
        #                     {
        #                         "title": "ห้อง 3/5"
        #                     },
        #                     {
        #                         "title": "ห้อง 3/6"
        #                     },
        #                     {
        #                         "title": "ห้อง 3/7"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     {
        #         "title": "มัธยมปลาย",
        #         "sub": [
        #             {
        #                 "title": "ม.4",
        #                 "sub": [
        #                     {
        #                         "title": "ห้อง 4/1"
        #                     },
        #                     {
        #                         "title": "ห้อง 4/2"
        #                     },
        #                     {
        #                         "title": "ห้อง 4/3"
        #                     },
        #                     {
        #                         "title": "ห้อง 4/4"
        #                     },
        #                     {
        #                         "title": "ห้อง 4/5"
        #                     },
        #                     {
        #                         "title": "ห้อง 4/6"
        #                     },
        #                     {
        #                         "title": "ห้อง 4/7"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "title": "ม.5",
        #                 "sub": [
        #                     {
        #                         "title": "ห้อง 5/1"
        #                     },
        #                     {
        #                         "title": "ห้อง 5/2"
        #                     },
        #                     {
        #                         "title": "ห้อง 5/3"
        #                     },
        #                     {
        #                         "title": "ห้อง 5/4"
        #                     },
        #                     {
        #                         "title": "ห้อง 5/5"
        #                     },
        #                     {
        #                         "title": "ห้อง 5/6"
        #                     },
        #                     {
        #                         "title": "ห้อง 5/7"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "title": "ม.6",
        #                 "sub": [
        #                     {
        #                         "title": "ห้อง 6/1"
        #                     },
        #                     {
        #                         "title": "ห้อง 6/2"
        #                     },
        #                     {
        #                         "title": "ห้อง 6/3"
        #                     },
        #                     {
        #                         "title": "ห้อง 6/4"
        #                     },
        #                     {
        #                         "title": "ห้อง 6/5"
        #                     },
        #                     {
        #                         "title": "ห้อง 6/6"
        #                     },
        #                     {
        #                         "title": "ห้อง 6/7"
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # ]

        

        return Response(your_result, status=status.HTTP_200_OK)

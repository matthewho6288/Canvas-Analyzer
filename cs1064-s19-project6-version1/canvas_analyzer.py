"""
Project 6
Canvas Analyzer
CS 1064 Introduction to Programming in Python
Spring 2018

Access the Canvas Learning Management System and process learning analytics.

Edit this file to implement the project.
To test your current solution, run the `test_my_solution.py` file.
Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: Matthew Ho
"""
__version__ = 7

# 2) print_user_info
"""The print_user_info function consumes a user dictionary and returns nothing.
The user dictionary is obtained from a file with the get_user function from the
canvas_requests.py file. This function utilizes dictionary key mapping to find
information about a student and uses the built in print function to display the
information."""
def print_user_info (user_dictionary):
    print ("Name: " + user_dictionary["name"])
    print ("Title: " + user_dictionary["title"])
    print ("Primary email: " + user_dictionary["primary_email"])
    print ("Bio: " + user_dictionary["bio"])
# 3) filter_available_courses
"""The filter_available_courses function consumes a list of course dictionaries
which is obtained using the get_courses function from the canvas_requests.py file.
The get_course function consumes a user id in the form of a string and then returns
a list of course dictionaries. The filter_availble_courses function creates an empty
list and uses a for loop to append courses that are availble into the list. The courses
are found by a conditional statement where the course 'workflow_state' must be
'available'. Lastly, returns the new list of dictionaries for available courses."""
def filter_available_courses (courses):
    course_list = []
    for course in courses:
        if course["workflow_state"] == "available":
            course_list.append(course)
    return course_list
# 4) print_courses
"""The print_courses function consumes the list of dictionaries created by the previous
function above and returns nothing. It obtains the id and name of the course by using dictionary
key mapping. It also uses a for loop to print the name and id of each course in the list.
This function consumes nothing."""
def print_courses(course_list):
    for course in course_list:
        print (str(course["id"]) + ": " + course["name"])
# 5) get_course_ids
"""The get_course_ids function consumes the same list as the function print_courses
(the list of dictionaries for available courses). It creates an empty list which will
be used to store the ids of each course in the consumed list by using dictionary key
mapping. By using a for loop, the function is able to obtain every id in the course
dictionary list and then it returns the list of ids."""
def get_course_ids(course_list):
    id_list = []
    for course in course_list:
        id_list.append(course["id"])
    return id_list
# 6) choose_course
"""The choose_course function consumes the id_list created from the previous function.
It uses the input function to prompt the user to pick a course id from the list. This
function uses a while loop where the user must input an id until the id that is inputed
is found in the list. The users input is then returned as course_id."""
def choose_course(id_list):
    #Because the input function returns a string, we must use the built in integer funtion.
    course_id = int(input("choose a course: "))
    while course_id not in id_list:
        course_id = int(input("choose a valid course: "))
    return course_id
# 7) summarize_points
"""The summarize_points function contains a list of dictionaries for submissions which are
obtained by using the get_submissions function from the canvas_requests.py file. The function
the amount of possible points, the points earned by the student, and calculates their grade.
The function returns nothing but prints all of the described data."""
def summarize_points(submission_list):
    # This list is created for containing all the weighted points points.
    total_sum = []
    # This list is created for containing all the weighted points earned by the student.
    obtained_sum = []
    """For this for loop, a for each submission dictionary in a the list of dictionaries,
    the points possible and the group weight are found using key mapping and used to calculate
    a grade which is rounded."""
    for submission in submission_list:
        if (submission["score"]) is not None:
            point_possible = (submission["assignment"]["points_possible"])
            weight = (submission["assignment"]["group"]["group_weight"])
            weighted_points = point_possible * weight
            total_sum.append(weighted_points)  
            score = submission["score"]
            weighted_score = score * weight
            obtained_sum.append(weighted_score)
    grade = sum(obtained_sum) / sum(total_sum)
    current_grade = round(grade *100)
    print ("Points possible so far: " + str(sum(total_sum)))
    print ("Points obtained: " + str(sum(obtained_sum)))
    print ("Current grade: " + str(current_grade))
# 8) summarize_groups
"""For the summarize_groups function, the same list of dictionaries from above is consumed.
This function is purposed for printing each 'group' or grading section and it is meant to find
and calculate the grade for each of those sections. This function returns nothing but uses the
built in print function display the grading group with its grade."""
def summarize_groups(submission_list):
    group_names = []
    """This for loop appends an empty list with a group name by only appending the group_names
    list if the name of the group is not already in the list."""
    for submission in submission_list:
        if submission["score"] is not None and submission["assignment"]["group"]["name"] not in group_names:
            group_names.append(submission["assignment"]["group"]["name"])
            group_names.sort()
    # This for loop find and calculates each grade for each group name from the list above.
    for name in group_names:
        #The empty lists are appended and eventually summed using the built in sum function.
        total_score = []
        points_possible = []
        # For each submission with a certain group name, rounded grade is calculated and printed.
        for submission in submission_list:
             """The score cannot be None and to second part of the if statement makes sure scores
             and points are for the same group."""
             if submission["score"] is not None and submission["assignment"]["group"]["name"] == name:
                     total_score.append(submission["score"])
                     points_possible.append(submission["assignment"]["points_possible"])
        sum_score = sum(total_score)
        sum_points = sum(points_possible)
        grade = round(sum_score / sum_points * 100)      
        print("* " + name + ": " + str(grade))    
# 9) plot_scores
"""The plot_scores functions consumes the list of dictionaries for submissions and imports the matplot
library. The function creates a list for grades which are calculated using a for loop. Once the grades
are found, the list is then used to plot histogram showing the distribution of grades. This funciton
returns nothing."""
def plot_scores(submission_list):
    import matplotlib.pyplot as plt
    grades = []
    # This for loop divides the score by the total points possible for each submission and appends the list.
    for submission in submission_list:
        # Scores that are None should be ignored
        if (submission["score"]) is not None:
            score = submission["score"]
            #submissions where there are zero points possible should be ignored.
            if submission["assignment"]["points_possible"] > 0:
                calculated_grade = score * 100 / (submission["assignment"]["points_possible"])
                grades.append(calculated_grade)
    plt.hist(grades)
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.title("Distribution of Grades")
    plt.show()
# 10) plot_grade_trends
"""The plot_grade_trends consumes the list of dictionaries for submissions and imports the matplot
library and the datetime library. This function shows three progressions of grades overtime. The high
line shows the highest grade the student can progress to taking into account their current grade. The low
line shows the lowest grade the student can get given what their current grades are. The maximum line
shows what the grade progression would look like if all points were earned over time."""
def plot_grade_trends(submission_list):
    import matplotlib.pyplot as plt 
    import datetime
    high = []
    low = []
    maximum = []
    due_dates = []
    for submission in submission_list:
        a_string_date = submission["assignment"]["due_at"]
        due_at = datetime.datetime.strptime(a_string_date, "%Y-%m-%dT%H:%M:%SZ")
        due_dates.append(due_at)
        # This if statement means the current scores are combined with perfect scores for ungraded assignments.
        if submission["workflow_state"] != "graded":
            points_possible = submission["assignment"]["points_possible"]
            high_point = (100 * points_possible * (submission["assignment"]["group"]["group_weight"]))
        else:
            score = submission["score"]
            high_point = (100 * score * (submission["assignment"]["group"]["group_weight"]))
        high.append(high_point)
        # This if statement meants that the current scores are combined with zeros for ungraded assignments.
        if submission["workflow_state"] != "graded":
            score = 0
            low_point = (100 * score * (submission["assignment"]["group"]["group_weight"]))  
        else:
            score = submission["score"] 
            low_point = (100 * score * (submission["assignment"]["group"]["group_weight"]))   
        low.append(low_point)
        # This would be as if the student earn a 100% on all their assignments.
        max_points = 100 * (submission["assignment"]["points_possible"]) * (submission["assignment"]["group"]["group_weight"])
        maximum.append(max_points)
    total_max = sum(maximum) / 100
    high_sum = 0
    high_sums = []
    # This for loop creates a running sum of the highest possible grade percentages.
    for high_points in high:
        high_sum = (high_sum + high_points)
        high_sums.append(round(high_sum / total_max, 2))
    low_sum = 0
    low_sums = []
    # This for loop creates running sum of the lowest possible grade percentages.
    for low_points in low:
        low_sum = (low_sum + low_points)
        low_sums.append(round(low_sum/total_max, 2))

    max_sum = 0
    max_sums = []
    # This for loop creats running sum for maximum grade percentages.
    for max_points in maximum:
        max_sum = (max_sum + max_points)
        max_sums.append(round(max_sum / total_max, 2))
    plt.plot(due_dates, high_sums, label = "Highest")
    plt.plot(due_dates, low_sums, label = "Lowest")
    plt.plot(due_dates, max_sums, label = "Maximum")
    plt.legend()
    plt.xticks(rotation=45)
    plt.title("Grade Trend")
    plt.ylabel("Grade")
    plt.show()
# 1) main
"""The main function calls every single function defined before it. It also imports canvas_requests.py
and calls functions from that file."""
def main(user_id):
    import canvas_requests
    user_dictionary = canvas_requests.get_user(user_id)
    print_user_info(user_dictionary)
    courses = canvas_requests.get_courses(user_id)
    course_list = filter_available_courses(courses)
    print_courses(course_list)
    id_list = get_course_ids(course_list)
    course_id = choose_course(id_list)
    submission_list = canvas_requests.get_submissions(user_id, course_id)
    summarize_points(submission_list)
    summarize_groups(submission_list)
    plot_grade_trends(submission_list)
    plot_scores(submission_list)   
if __name__ == "__main__":
    main('hermione')
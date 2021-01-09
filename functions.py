import unicodedata
from classes import *
from bs4 import BeautifulSoup


def scrape_all_courses(page_source, department):
    # This function takes in an HTML input and outputs a list of objects representing all the lecture blocks in the department

    soup = BeautifulSoup(page_source, 'html.parser')

    # Thin out the soup a bit to only get the course information
    soup = soup.find("div", class_="datatableNew")

    # Find all lecturer/lecture blocks offered
    soup = soup.find_all("div", class_="col-lg-9 col-md-9 col-sm-9 col-xs-12")

    course_objects_list = []

    # Cycle through all of the lecturers
    for lecturer in soup:
        # Find the course name
        course_name_html = lecturer.find_parent("div", class_="courseSearchItem")
        course_name_html = course_name_html.find_previous_sibling("div", class_="courseSearchHeader")
        course_name = unicodedata.normalize("NFKD", course_name_html.find("span", class_="courseTitle").get_text())

        # Find the weekday the course is offered
        weekday = lecturer.find("div", class_="col-lg-search-days col-sm-push-1 col-md-days col-sm-days col-xs-2").get_text(strip=True)     # Setting strip to True removes the newline in the string
        weekday = weekday.replace("Days", "")

        # Find the hour the course is offered
        hour = lecturer.find("div", class_="col-lg-search-time col-sm-push-1 col-md-time col-sm-time col-xs-5").get_text(strip=True)
        hour = hour.replace("Time", "")

        # Find the instructor of the course
        instructor = unicodedata.normalize("NFKD", lecturer.find("div", class_="col-lg-search-instructor col-md-search-instructor col-sm-push-1 col-sm-search-instructor col-xs-3").get_text())
        instructor = instructor.replace("\n", "").replace("Instructor", "")

        # Find the spaces left in the course
        availability = lecturer.find("div", class_="col-lg-search-space col-md-space col-sm-push-1 col-sm-space col-xs-2").get_text(strip=True)
        availability = availability.replace("Space", "")

        # Convert the availability (and maximum later) to an integer, if possible.
        if availability.isdigit():
            availability = int(availability)

        # Find the maximum spaces of the course
        maximum = lecturer.find("div", class_="col-lg-days col-md-space col-sm-push-1 col-sm-space col-xs-2").get_text(strip=True)
        maximum = maximum.replace("Max", "")

        if maximum.isdigit():
            maximum = int(maximum)

        # Create an object representing this lecture block and add it to the list
        new_course = Course(course_name, department, weekday, hour, instructor, availability, maximum)

        # For now, due to differences on how I initially wrote the code, we have to append the object in its own list.
        course_objects_list.append([new_course])
        # TODO: Make the course_objects_list a better format for the single_course_scrape? Or modify the scrape_single_course to be in a better format?

    return course_objects_list


def scrape_single_course(course_titles, all_course_spans, course_number, department):
    # This function takes in inputs of the html, a specific course name, and the department, and outputs an object
    # representing that course

    target_span = "span"  # Placeholder for variable
    course_tuple = zip(course_titles, all_course_spans)
    # Cycle through every course title, associating course name with the soup (zip function)
    for title, span in course_tuple:
        if course_number in title:  # if the the desired course number is in the title, find the specific element
            target_span = span
            break

    if target_span == "span":  # Check to see if the course was found. If not, return nothing
        return

    course_number = department + course_number
    course_info = target_span.find_parent("div", class_="courseSearchHeader")
    course_info = course_info.find_next_sibling()  # Get to the course info we want to scrape

    specific_course_attribute = course_info.get_attribute_list("class")  # obtain the current attribute

    course_objects_list = []

    # This while loop is to scrape every single instructor of a specific course
    while specific_course_attribute[0] == "courseSearchItem":
        course_instructor = unicodedata.normalize("NFKD", course_info.find("span", attrs={"style": "word-wrap: break-word"}).get_text()).replace("\n", "")

        course_space = course_info.find("div", class_="col-lg-search-space col-md-space col-sm-push-1 col-sm-space col-xs-2").get_text(strip=True).replace("Space", "")
        if course_space.isdigit():
            course_space = int(course_space)

        course_maximum = course_info.find("div", class_="col-lg-days col-md-space col-sm-push-1 col-sm-space col-xs-2").get_text(strip=True).replace("Max", "")
        if course_maximum.isdigit():
            course_maximum = int(course_maximum)

        course_weekday = course_info.find("div", class_="col-lg-search-days col-sm-push-1 col-md-days col-sm-days col-xs-2").get_text(strip=True).replace("Days", "")

        course_time = course_info.find("div", class_="col-lg-search-time col-sm-push-1 col-md-time col-sm-time col-xs-5").get_text(strip=True).replace("Time", "")

        course_objects_list.append(
            Course(course_number, department, course_weekday, course_time, course_instructor, course_space,
                   course_maximum))

        course_info = course_info.find_next_sibling()
        specific_course_attribute = course_info.get_attribute_list("class")

    return course_objects_list


def concat_dept(course):
    # This function takes in a Course object and outputs a concatenated string in the form:
    # Course.name + Course.instructor + Course.weekday + Course.hour
    concat_string = course.name + " " + course.instructor + " " + course.weekday + " " + course.hour
    return concat_string

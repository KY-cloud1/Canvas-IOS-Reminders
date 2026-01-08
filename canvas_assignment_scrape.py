# Canvas Assignments Scraper

'''
This module contains a class that scrapes assignments from Canvas 
using the Canvas GraphQL API.
'''


import datetime
import json
import urllib.request

TOKEN = ""


class CanvasApiAssignments:
    '''
    Contains methods that fetches and manages assignments from the
    Canvas GraphQL API.
    '''

    def __init__(self, token: str) -> None:
        '''
        Initializes a CanvasApiAssignments object by setting the
        user's personal Canvas token.
        
        token represents the given Canvas access token.
        '''

        self._token = TOKEN  # CURRENTLY HARDCODED


    def get_all_assignments(self) -> dict | None:
        '''
        Fetches all assignments in the current Canvas courses.
        
        Returns a dictionary containing all of the assignments with
        names, ids, and due dates.

        Returns None if the Canvas API call failed or call result
        is invalid.
        '''

        BASE_URL = "https://canvas.eee.uci.edu/api/graphql"

        query = '''
        query AllUpcomingAssignments {
            allCourses {
                name
                assignmentsConnection(first: 100) {
                    nodes {
                        name
                        dueAt
                    }
                }
            }
        }
        
        '''

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json"
            }

        data = json.dumps({"query": query}).encode("utf-8")

        try:
            request = urllib.request.Request(BASE_URL, 
                                             data = data, 
                                             headers = headers, 
                                             method = "POST")

            with urllib.request.urlopen(request) as response:
                status = response.getcode()

                if status != 200:
                    print("FAILED.")
                    print('NOT 200')
                    return None
                
                try:
                    assignment_data = json.loads(response.read().decode("utf-8"))

                except json.JSONDecodeError:
                    print("FAILED.")
                    print('INVALID FORMAT RECEIVED')
                    return None
                
                if not assignment_data:
                    print("FAILED.")
                    print('ASSIGNMENT DATA DOES NOT EXIST.')
                    return None
                
                return assignment_data
            
        except Exception as e:
            print("FAILED")
            print(f"UNABLE TO CONNECT TO URL: {e}")
            return None
        

    def parse_assignments_due(self, assignments: dict) -> str:
        '''
        Parses given assignments by only selecting the ones that have
        a due date on or after the current day and no later than the
        delta weeks from the current date.
        
        assignments represents the data received from the Canvas API.

        Returns a JSON string containing only assignments that have
        due dates on or after the current day.
        '''

        # Represents the number of weeks in the future to consider
        # for assignments with due dates.
        WEEKS_DELTA = 2

        due_assignments = []

        curr_date = datetime.datetime.now(datetime.timezone.utc)

        weeks_future = curr_date + datetime.timedelta(weeks= WEEKS_DELTA)

        for course in assignments['data']['allCourses']:
            for assignment in course['assignmentsConnection']['nodes']:
                assignment_due_date = assignment.get("dueAt")

                if not assignment_due_date:
                    continue

                # Convert assignment due date from ISO 8601 string into
                # datetime.datetime object in UTC for comparison.
                due_date_dt = datetime.datetime.fromisoformat(
                    assignment_due_date.replace("Z", "+00:00"))

                if due_date_dt >= curr_date and due_date_dt <= weeks_future:
                    due_assignments.append({
                        "course": course['name'],
                        "assignment": assignment['name'],
                        "dueAt": assignment_due_date
                        })

        assignments_json_str = json.dumps(due_assignments, indent= 2)

        return assignments_json_str


def run():
    '''
    Docstring for main
    '''

    canvas_scraper = CanvasApiAssignments("jkl;")

    assignments = canvas_scraper.get_all_assignments()

    if not assignments:
        return

    sorted_assignments = canvas_scraper.parse_assignments_due(assignments)

    print(sorted_assignments)


if __name__ == '__main__':
    run()


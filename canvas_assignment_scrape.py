# Canvas Assignments Scraper

'''
This module contains a class that scrapes assignments from Canvas 
using the Canvas GraphQL API.
'''


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


    def get_assignments(self) -> dict | None:
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
                        _id
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
        

    def parse_assignments(self, assignments: dict) -> dict:
        '''
        Parses given assignments by 
        
        
        '''



def run():
    '''
    Docstring for main
    '''

    canvas_scraper = CanvasApiAssignments("jkl;")

    assignments = canvas_scraper.get_assignments()

    print(assignments)


if __name__ == '__main__':
    run()


# server.py

'''
This module contains a FastAPI application that uses Uvicorn (ASGI)
to send JSON data.
'''


import canvas_assignment_api
import fastapi
import uvicorn


# This constant represents the port that the local server will run on.
PORT = 8080


# This constant represents the number of weeks in the future to 
# consider for assignments with due dates.
WEEKS_DELTA = 2


app = fastapi.FastAPI()


@app.get('/assignments')
def get_upcoming_assignments():
    '''
    Gets assignments from Canvas, filters into upcoming, and returns
    the assignments as a list of dictionaries.
    '''

    # 'TOKEN' is currently unused as the Canvas token is hardcoded into
    # the canvas_assignment_api module.
    canvas_api = canvas_assignment_api.CanvasApiAssignments('TOKEN')

    assignments = canvas_api.get_all_assignments()

    if not assignments:
        return

    filtered_assignments = canvas_api.filter_assignments_due(assignments,
                                                             WEEKS_DELTA)

    return filtered_assignments


if __name__ == '__main__':
    uvicorn.run("server:app", port = PORT, log_level = "info",)

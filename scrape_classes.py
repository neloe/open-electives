import requests
from bs4 import BeautifulSoup
#import sys

LANDING = 'https://ssb.nwmissouri.edu/pls/PRODDAD/nwcrse.P_Showschedule'
TARGET = 'https://ssb.nwmissouri.edu/pls/PRODDAD/nwcrse.P_Displaydata'
DEPT_CODE = 'CSIS'

def get_classes():
    soup = BeautifulSoup(requests.get(LANDING).text, 'html5lib')
    term_select = soup.find(id='term_input_id')
    term_options = term_select.find_all('option')
    term_map = {int(t['value']):t.text for t in term_options}
    sems = sorted(list(term_map.keys()), reverse=True)[:4]
    #for i,s in enumerate(sems):
    #    print("{}. {}".format(i, term_map[s]))
    #idx = input('Select semester: ')
    #semcode = str(sems[int(idx)])
    semcode = str(sems[0])

    post_args = {'term_code': semcode, 'subj_code': DEPT_CODE}

    page = requests.post(TARGET, data=post_args)

    soup2 = BeautifulSoup(page.text, 'html5lib')
    courses = soup2.find('table', {'class': 'datadisplaytable'})
    rows = courses.find_all('tr')

    course_rows = rows[1:]
    courses = []
    for course in course_rows:
        cells = course.find_all('td')
        courses.append((cells[0].text, cells[2].text, cells[6].text, cells[8].text, cells[9].text, cells[11].text,cells[12].text,cells[13].text))
    return courses

'''
def to24h(time):
    t = time.split()
    h,m = t[0].split(':')
    h = int(h)
    m = int(m)
    if t[1] == 'pm' and h != 12:
        h += 12
    return h,m

def format_course(course):
    cells = course.find_all('td')
    times = cells[9].text.split('-')
    start, end = times[0], times[1]
    starth, startm = to24h(start)
    endh, endm = to24h(end)
    duration = (endh - starth) * 60 + ((endm - startm + 60)%60)
    return {'name': cells[6].text.title(), 'room': cells[10].text,
            'days': cells[8].text, 'type': 'class',
            'start': 100*starth + startm, 'duration': duration}

from pprint import PrettyPrinter
import json
p = PrettyPrinter(indent=4)

courselist = []
for c in course_rows:
    try:
        courselist.append(format_course(c))
    except:
        pass

#p.pprint(courselist)
if len(sys.argv) > 1:
    with open(sys.argv[1], 'w') as f:
        json.dump(courselist, f, indent=4)
else:
    print(json.dumps(courselist, indent=4))
'''
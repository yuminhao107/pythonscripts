import requests
import json
from datetime import datetime,timedelta
import sys


building_val={
    'J1':9,
    'J2':10,
    'J3':11,
    'J4':12,
    'J5':13,
    'J6':14,
    'J7':15,
    'J8':45,
}
term_val=23 #2018-2019-2
compus_val=22 #jiulonghu
url='http://58.192.114.179/classroom/show/getemptyclassroomlist'
lessons=[
    '08:45',
    '09:35',
    '10:35',
    '11:25',
    '12:15',
    '14:45',
    '15:35',
    '16:35',
    '17:25',
    '18:15',
    '19:15',
    '20:05',
    '20:55',
]

def minutesOfLessons(lessons):
    result=[]
    for lesson in lessons:
        tokes=lesson.split(':')
        result.append(int(tokes[0])*60+int(tokes[1]))
    return result

end_of_lessons=minutesOfLessons(lessons)

def getSequence():
    today=datetime.now()
    now=today.minute+today.hour*60
    if now>=end_of_lessons[-1]:
        return 1,5,True
    id=0
    for i in range(len(end_of_lessons)):
        if now<end_of_lessons[i]:
            id=i+1
            break
    if id<=4:
        return id,5,False
    if id<=9:
        return id,10,False
    return id,13,False

def getDateOfWeek(date):
    re=requests.post('http://58.192.114.179/classroom/common/getdateofweek?date='+date)
    return json.loads(re.text)

def getToday():
    today=datetime.now()
    startSequence,endSequence,nextDay=getSequence()
    if nextDay:
        today+=timedelta(days=1)
    dic=getDateOfWeek(today.strftime('%Y-%m-%d'))
    dic['startSequence']=startSequence
    dic['endSequence']=endSequence
    dic['date']=today.strftime('%Y-%m-%d')
    return dic

def getEmptyClassroom(buildingId,startWeek,endWeek,dayOfWeek,startSequence,endSequence,termId):
    keywords={
        #'pageNo' : pageNo,
        #'pageSize' : pageSize,
        'campusId' : compus_val,
        'buildingId' : buildingId,
        'startWeek' : startWeek,
        'endWeek' : endWeek,
        'dayOfWeek' : dayOfWeek,
        'startSequence' : startSequence,
        'endSequence' : endSequence,
        'termId' : termId
    }
    re=requests.post(url,data=keywords)
    result=json.loads(re.text)
    classrooms=[]
    for row in result['rows']:
        classrooms.append(row['name'])
    return classrooms

def getClassroom():
    targetBuilding=['J8','J6']
    if len(sys.argv)>1:
        targetBuilding=sys.argv[1:]
        for id in targetBuilding:
            if not id in building_val:
                print('请输入正确的教学楼代码。（例如，使用 J8 代表教八）')
                return

    dic=getToday()
    printstring='这是 {0} 第{1}与第{2}节课之间的空教室:'
    print(printstring.format(dic['date'],dic['startSequence'],dic['endSequence']))

    for building in targetBuilding:
        rooms=getEmptyClassroom(
            building_val[building],
            dic['week'],
            dic['week'],
            dic['dayOfWeek'],
            dic['startSequence'],
            dic['endSequence'],
            dic['termId'])
        for room in rooms:
            print(room)
    
    
if __name__ == "__main__":
    getClassroom()

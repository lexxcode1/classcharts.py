import typing

import requests
import asyncio
from datetime import timedelta
from obj import *


class Student:
    def __init__(self):
        self.id = None
        self._session_id = None
        self._stem = 'https://www.classcharts.com/apiv2student/'

        self.name = None
        self.announcements_count = 0
        self._code = None
        self._dob = None

    async def _req(self, verb, target, *, _data=None, _params=None, authed=None):
        """"Makes a request
        :type verb: HttpVerb
        """
        stem = self._stem
        response = None

        if not self._session_id:
            await self.login()

        headers = {'Authorization': f'Basic {self._session_id}'}

        if verb == 'GET':
            response = requests.get(f'{stem}{target}', headers=headers, params=_params)
        elif verb == 'POST':
            response = requests.post(f'{stem}{target}', data=_data, headers=headers if authed else None)

        return response

    async def login(self):

        # self._code = 'WADB4P5QE6'
        self._code = 'G8JHB5HAMC'
        # self._dob = '2005-10-17'
        self._dob = '2008-12-09'
        data = {'code': f'{self._code}',
                'dob': f'{self._dob}',
                'remember_me': 'true',
                'recaptcha-token': 'no-token-available'}
        response = requests.post(f'{self._stem}login', data=data)
        self._session_id = response.json()['meta']['session_id']
        self.id = response.json()['data']['id']

        await self.ping()

    async def homeworks(self, *, after: datetime = None, before: datetime = None, show_completed=False):
        if after is None:
            after = datetime.now()
        if before is None:
            before = datetime.now() + timedelta(days=7)

        params = {
            'display_date': 'due_date',
            'from': after.strftime('%Y-%m-%d'),
            'to': before.strftime('%Y-%m-%d')
        }

        homework_list = []
        response = await self._req('GET', f'homeworks/{self.id}?', _params=params)

        for x in response.json()['data']:
            if show_completed and not Homework(x).status:
                homework_list.append(Homework(x))
            elif not show_completed:
                homework_list.append(Homework(x))
        return homework_list

    async def ping(self):
        data = {
            'include_data': 'true'
        }

        response = await self._req('POST', 'ping', _data=data, authed=True)

        user = response.json()['data']['user']
        user.pop('first_name') and user.pop('last_name')

        self.name = user['name']
        self.announcements_count = user['announcements_count']

    async def timetable(self, day: datetime = None):
        params = {}
        if day:
            params['date'] = day.strftime('%Y-%m-%d')

        response = await self._req('GET', f'timetable/{self.id}', _params=params)
        print(response.json())
        return Timetable(response.json())

    async def announcements(self):
        response = await self._req('GET', f'announcements/{self.id}')

        data = response.json()['data']

        return Announcements(data).announcements

    async def get_name(self):
        await self.ping()
        return self.name

    def __repr__(self):
        return f'<Student id={self.id}>'


async def main():
    new_student = Student()
    # homeworks = await new_student.homeworks(before=(datetime.now() + timedelta(days=1)))
    timetable = await new_student.timetable(day=(datetime.now() + timedelta(days=1)))
    day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print(new_student)
    await new_student.ping()

    announcements = await new_student.announcements()

    for announcement in announcements:
        print(announcement)
    # for lesson in timetable.lessons:
    #     print(lesson)
    # for homework in homeworks:
    #     print((homework.teacher, homework.title, day_name[datetime.strptime(homework.due_date.strftime('%d-%m-%y'), '%d-%m-%y').weekday()]))


if __name__ == '__main__':
    asyncio.run(main())

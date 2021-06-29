from datetime import datetime

from helper import clean_text


class HomeworkAttachment:
    def __init__(self, data):
        self.id = data['id']
        self.file_name = data['file_name']
        self.file = data['validated_file']

    def __repr__(self):
        return f'<HomeworkAttachment id={self.id} name={self.file_name}>'


class AnnouncementAttachment:
    def __init__(self, data):
        self._data = data
        self.file_name = data['filename']
        self.file = data['url']

    def __repr__(self):
        return f'<AnnouncementAttachment name={self.file_name}>'


class HomeworkStatus:
    def __init__(self, data):
        self._data = data
        self.id = data['id']
        self.state = data['state']
        self.completed = data['ticked']
        self.allow_attachments = bool(data['allow_attachments'])

    def __repr__(self):
        return f'<HomeworkStatus id={self.id} completed={bool(self)}>'

    def __bool__(self):
        return self.completed == 'yes'


class Announcement:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = clean_text(data['description'])
        self.attachments = [AnnouncementAttachment(x) for x in data['attachments']]

    def __repr__(self):
        return f'<Announcement id={self.id} title={self.title}>'


class Announcements:
    def __init__(self, data):
        self._data = data
        self.announcements = [Announcement(row) for row in data]

    def __repr__(self):
        return f'<Announcements count={len(self._data)}'


class Homework:
    def __init__(self, data):
        self._data = data
        self.lesson = data['lesson']
        self.subject = data['subject']
        self.teacher = data['teacher']
        self.id = data['id']
        self.title = clean_text(data['title'])
        self.description = clean_text(data['description'])
        self.issue_date = datetime.strptime(data['issue_date'], "%Y-%m-%d")
        self.due_date = datetime.strptime(data['due_date'], "%Y-%m-%d")
        self.completion_time = (int(data['completion_time_value'] or '0'), data['completion_time_unit'])
        self.attachments = [HomeworkAttachment(x) for x in data['validated_attachments']]
        self.status = HomeworkStatus(data['status'])

    def __repr__(self):
        return f'<Homework id={self.id} lesson={self.lesson} teacher={self.teacher} title={self.title} issue_date={self.issue_date} due_date={self.due_date}>'


class Lesson:
    def __init__(self, data):
        self.teacher = data['teacher_name']
        self.lesson = data['lesson_name']
        self.subject = data['subject_name']
        self.period = data['period_number']
        self.room = data['room_name']
        self._key = data['key']

    def __repr__(self):
        return f'<Lesson teacher={self.teacher} subject={self.subject} period={self.period} room={self.room}>'


class Timetable:
    def __init__(self, data):
        data_exists = len(data['data']) != 0
        self.lessons = [Lesson(x) for x in data['data']] if data_exists else ['N/a']
        self.date = datetime.fromisoformat(data['meta']['dates'][0]) if data_exists else 'N/a'
        self.start = datetime.fromisoformat(data['meta']['start_time']) if data_exists else 'N/a'
        self.end = datetime.fromisoformat(data['meta']['end_time']) if data_exists else 'N/a'

    def __repr__(self):
        return f'<Timetable date={self.date}>'

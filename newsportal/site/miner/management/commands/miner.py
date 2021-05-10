from pprint import pprint
import os
import sys
from time import time
import concurrent.futures
from django.core.management.base import BaseCommand
from miner.models import News, Log


class Command(BaseCommand):
    def handle(self, *args, **options):
        sys.path = ['../reporters'] + sys.path

        def get_reporters(self):
            reporters = []
            reporters_files = os.listdir('../reporters')
            print(reporters_files)
            for r in reporters_files:
                print(r)
                try:
                    if '__' not in r and r not in ('Credentials.py',
                                                   'utils.py',
                                                   'ReporterError.py'):
                        reporters.append(__import__(r[:-3]))
                except ModuleNotFoundError as e:
                    make_log(self, 'ERROR', e)
            return reporters

        def make_log(self, level, message):
            lo = Log(level_name=level, message=message)
            lo.save()

        print(1)
        reporters = get_reporters(self)
        print(2)
        make_log(self, 'INFO', 'start mining')
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_name = {executor.submit(r.get_news):
                              r.name for r in reporters}
            for future in concurrent.futures.as_completed(future_to_name):
                name = future_to_name[future]
                try:
                    data = future.result()
                    if isinstance(data, dict):
                        if len(News.objects.filter(text=data['text'])) == 0:
                            n = News(reporter_name=name,
                                     title=data['title'],
                                     text=data['text'])
                            n.save()
                    elif data is not None:
                        ltitle, ltext = data.split('. ', maxsplit=1)
                        if len(News.objects.filter(text=ltext)) == 0:
                            n = News(reporter_name=name,
                                     title=ltitle,
                                     text=ltext)
                            n.save()
                except Exception as e:
                    make_log(self, 'ERROR', f'{name} raised {e}')
                else:
                    make_log(self, 'INFO', f'{name} return {data}')

        make_log(self, 'INFO', 'stop mining')
        self.stdout.write('I\'m fine!')

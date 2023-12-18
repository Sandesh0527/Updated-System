import json
from django.core.management.base import BaseCommand
from Exam.models import Exam, Question, Choice
from django.conf import settings
import os 
 
class Command(BaseCommand):
    help = 'Load exam data from a JSON file'
 
    # def add_arguments(self, parser):
    #     parser.add_argument('file_path', help='Path to the JSON file')
 
    def handle(self, *args, **options):
        path = settings.FIXTURE_DIRS
        file_path = os.path.join(path[0] + '\\questions.json')
 
        with open(file_path) as f:
            data = json.load(f) 
            for exam_data in data:
                try:
                    exam = Exam.objects.create(
                        name=exam_data['name'],
                        description=exam_data['description'],
                        duration=exam_data['duration'],
                        start_time=exam_data['start_time'],
                        end_time=exam_data['end_time'],
                    )
 
                    for question_data in exam_data['questions']:
                        question = Question.objects.create(
                            exam=exam,
                            text=question_data['text'],
                            marks = question_data['marks']
                        )
 
                        for choice_data in question_data['choices']:
                            Choice.objects.create(
                                question=question,
                                text=choice_data['text'],
                                is_correct=choice_data['is_correct'],
                            )
                except Exception as e:
                    print(str(e))
 
        self.stdout.write(self.style.SUCCESS('Exam data loaded successfully'))
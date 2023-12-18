from django import forms
from .models import Exam, Question, Choice


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'description', 'duration', 'start_time', 'end_time']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']


ChoiceFormSet = forms.inlineformset_factory(
    Question, Choice, form=ChoiceForm, extra=1, min_num=1, validate_min=True
)

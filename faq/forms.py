"""
Here we define a form for allowing site users to submit
a potential FAQ that they would like to see added.

From the user's perspective the question is not added automatically,
but actually it is, only it is added as inactive.
"""

import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from faq.models import Question, Topic
from faq.enums import STATUS_INACTIVE


class SubmitFaqForm(forms.Form):
    topic = forms.ModelChoiceField(
                        queryset=Topic.objects.all(),
                        empty_label=None, label=_('Topic'))
    question = forms.CharField(max_length=512, min_length=4,
                        widget=forms.Textarea, label=_(u'Question'))
    answer = forms.CharField(required=False, widget=forms.Textarea,
                        label=_(u'Answer'))

    def __init__(self, language, *args, **kwargs):
        super(SubmitFaqForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = self.fields['topic'].queryset \
                                        .filter(language=language)

    def clean_answer(self):
        answer = self.cleaned_data['answer']
        if not answer or len(answer) < 1:
            self.cleaned_data['answer'] = _(u"No answer for this FAQ is" \
                                        " available at this time.")
        return self.cleaned_data['answer']

    def save(self, user=None):
        dt = datetime.datetime.now()
        slug_str = "anon-%d-%d-%d-%d-%d-%d" % (dt.year, dt.month, dt.day,
                                                dt.hour, dt.minute,
                                                dt.second)
        topic = self.cleaned_data['topic']
        question = self.cleaned_data['question']
        answer = self.cleaned_data['answer']
        new_question = Question(text=question, answer=answer, topic=topic,
                                slug=slug_str, sort_order = 999,
                                protected = False,
                                status = STATUS_INACTIVE)
        return new_question

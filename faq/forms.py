"""
Here we define a form for allowing site users to submit
a potential FAQ that they would like to see added.

From the user's perspective the question is not added automatically,
but actually it is, only it is added as inactive.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _

from faq.models import Question

class SubmitFaqForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('topic', 'text', 'answer')

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


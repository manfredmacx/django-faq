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
		fields = ('topic', 'question',)
	
	def __init__(self, language, *args, **kwargs):
		super(SubmitFaqForm, self).__init__(*args, **kwargs)
		self.fields['topic'].queryset = self.fields['topic'].queryset \
										.filter(language=language)



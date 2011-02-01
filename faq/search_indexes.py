from haystack import indexes
from haystack.sites import site
from django.utils.translation import ugettext_lazy as _
from faq.models import Question
from faq import enums

class SearchableFAQ(Question):
	class Meta:
		proxy = True
		verbose_name = _('FAQ')
		verbose_name_plural = _('FAQs')
	def display(self):
		return self.question
	def description(self):
		return self.question
	def resulttype(self):
		return _("[{0}]  ".format("FAQ"))
	def get_updated_field(self):
		return self.date_modified
	def get_absolute_url(self):
		return "/faq/#{0}".format(self.slug)

class FaqIndex(indexes.SearchIndex):
	text = indexes.CharField(document=True, use_template=True)
	question = indexes.CharField(model_attr="question")
	answer = indexes.CharField(model_attr="answer")
	
	def get_queryset(self):
		return SearchableFAQ.objects.filter(status = enums.STATUS_ACTIVE)


site.register(SearchableFAQ, FaqIndex)

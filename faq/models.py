from datetime import datetime
import simplejson as json

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

import enums
from .managers import QuestionManager
from .relations import find_related_questions


class Topic(models.Model):
    """
    Generic Topics for FAQ question grouping
    """
    class Meta:
        ordering = ('sort_order', 'name')

    language = models.CharField(blank=False, max_length=5,
                                choices=settings.LANGUAGES,
                                verbose_name=_(u'Language'))
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    sort_order = models.IntegerField(_("sort order"), default=0,
                                     help_text=_("The order you would like the topic to be displayed."))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Update questions to topic language
        """
        super(Topic, self).save(*args, **kwargs)
        Question.objects.filter(topic=self).update(language=self.language)



class Question(models.Model):
    """
    Represents a frequently asked question.
    """
    objects = QuestionManager()

    class Meta:
        ordering = ('sort_order', 'created_on')

    # Creation
    created_by = models.ForeignKey(User, null=True, editable=False,
                                   related_name="%(class)s_created_by"
                                   )
    created_on = models.DateTimeField(_("created on"), default=datetime.now,
                                      editable=False
                                      )
    
    # Update
    updated_on = models.DateTimeField(_("updated on"),
                                      editable=False
                                      )
    updated_by = models.ForeignKey(User,
                                   null=True, editable=False
                                   )

    language = models.CharField(blank=False, max_length=5,
                                choices=settings.LANGUAGES,
                                verbose_name=_(u"Language"))

    slug = models.SlugField(max_length=100,
                            help_text=_("This is a unique identifier that allows your questions to" \
                                            " display its detail view, ex 'how-can-i-contribute'"), )
    topic = models.ForeignKey(Topic)

    text = models.TextField(_('question'), 
                            help_text=_("The actual question itself."))
    answer = models.TextField(_('answer'), 
                              help_text=_("The answer text."))

    status = models.IntegerField(choices=enums.QUESTION_STATUS_CHOICES,
                                 default=enums.STATUS_INACTIVE,
                                 help_text=_("Only questions with their status set to 'Active' will be" \
                                                 "displayed. Questions marked as 'Group Header' are" \
                                                 " treated as such by views and templates that are set up" \
                                                 " to use them.")
                                 )

    sort_order = models.IntegerField(_('sort order'), default=0,
                                     help_text=_("The order you would like the question to be displayed."))

    protected = models.BooleanField(default=False,
                                    help_text=_("Set true if this question is only visible by" \
                                                    " authenticated users."))

    # json encoded list of IDs of related FAQ entries
    related_cache = models.TextField(blank=True, default='', editable=False)

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_on = datetime.now()
            
        self.updated_on = datetime.now()
        super(Question, self).save(*args, **kwargs)

    def is_header(self):
        return self.status == enums.STATUS_HEADER

    def is_active(self):
        return self.status == enums.STATUS_ACTIVE

    @property
    def related(self):
        """
        Returns a list with the 5 most 'similar' Questions.
        
        This uses uses related_cache and can quite time consuming if no cached data exists.
        """
        if not self.related_cache:
            ret = find_related_questions(self)
            self.related_cache = json.dumps([question.id for question in ret])
            self.save()
        else:
            ret = [self.__class__.objects.get(id=faqid) for faqid in json.loads(self.related_cache)]
        return ret

    @models.permalink
    def get_absolute_url(self):
        return ('faq:question-detail', (self.slug, ))

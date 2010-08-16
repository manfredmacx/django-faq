from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list_detail import object_detail, object_list

import faq.enums
from .models import Question
from .forms import SubmitFaqForm

def question_detail(request, question_slug, template_name='faq/question_detail.html',
                    extra_context={}):
    """
    Displays an individual question.
    """
    return object_detail(request,
                         template_name=template_name,
                         extra_context=extra_context,
                         slug=question_slug,
                         slug_field='slug',
                         queryset = Question.objects.active(user=request.user),
                         )


def question_list(request, template_name='faq/question_list.html',
                  extra_context={}, group=False):
    """
    Displays a list of all the questions.
    """
    # NOTE:
    # The code shown here is NOT REALLY NEEDED, but it is a good example
    # of extending an app using extra_content and such.
    # Specifically note how we set the dict value and then allow the user
    # to pass along their own additional extra_context using 'update'.
    query_set = Question.objects.active(group=group, 
                                        user=request.user).filter(language=request.LANGUAGE_CODE)

    last_update = query_set.values('updated_on').order_by('-updated_on', )[0]
    extra = {'updated_on': last_update['updated_on']}
    extra.update(extra_context)

    return object_list(request,
                       template_name=template_name,
                       extra_context=extra,
                       queryset=query_set,
                       )


def faq_list(request, template_name='faq/faq_list.html', extra_context={}):
    """
    Display a typical FAQ view without group headers.
    Shows how to "extend" or "override" the default view supplied above.
    We also make sure this view is also overridable.
    """

    extra = {'page_title': _(u'FAQs')}
    extra.update(extra_context)
    return question_list(request, template_name=template_name,
                        extra_context=extra)


def faq_list_by_group(request, template_name='faq/faq_list_by_group.html',
                      extra_context={}):

    extra = {'page_title': _(u'Grouped FAQs')}
    extra.update(extra_context)
    return question_list(request, group=True,
                         template_name=template_name, extra_context=extra)


@login_required
def submit_faq(request, form_class=SubmitFaqForm,
               template_name="faq/submit_question.html",
               success_url="/", extra_context={}):

    if request.method == 'POST':
        form = form_class(data=request.POST, language=request.LANGUAGE_CODE)

        if form.is_valid():
            question = form.save(commit=False)

            # Generate slug
            now = datetime.now()
            question.slug = "%s-%d-%d-%d-%d-%d-%d" % (request.user.username,
                                                      now.year, now.month, now.day,
                                                      now.hour, now.minute,
                                                      now.second)

            question.language = request.LANGUAGE_CODE
            question.status = faq.enums.STATUS_INACTIVE

            question.created_by = request.user

            question.save()

            # Now set up a confirmation message for the user
            messages.success(request,
                             _(u"Your question was submitted and will be reviewed by the site administrator for possible inclusion in the FAQ.")
                             )


            return HttpResponseRedirect(success_url)
    else:
        form = form_class(language=request.LANGUAGE_CODE)

    context = {'form': form, }
    context.update(extra_context)
    return render_to_response(template_name, context,
                              context_instance = RequestContext(request))

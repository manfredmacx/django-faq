from django.contrib import admin
from models import Question, Topic
from datetime import datetime


class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'sort_order', )
    list_filter = ('language', )
    search_fields = ['name', ]
    prepopulated_fields = {'slug': ('name', )}


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'language', 'topic', 'sort_order', 'created_by',
                    'created_on', 'updated_by', 'updated_on', 'status', )
    list_filter = ('language', )
    search_fields = ['text', ]

    def save_model(self, request, obj, form, change):
        '''
        Overrided because I want to also set who created this instance.
        '''
        instance = form.save(commit=False)
        if instance.id is None:
            new = True
            instance.created_by = request.user
        instance.updated_by = request.user
        instance.save()
        return instance

admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)

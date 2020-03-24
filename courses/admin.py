from datetime import date

from django.contrib import admin

from . import models


def make_published(modeladmin, request, queryset):
    queryset.update(status='p', published=True)


make_published.short_description = 'Mark selected courses as Published'


class TextStepInline(admin.StackedInline):
    model = models.TextStep
    fieldsets = (
        (None, {
            'fields': (('title', 'order'), 'description', 'content'),
        }),
    )


class QuizStepInline(admin.StackedInline):
    model = models.QuizStep
    fieldsets = (
        (None, {
            'fields': ('title', ('order', 'total_questions'), 'description',),
        }),
    )

class TopicListFilter(admin.SimpleListFilter):
    title = 'topic'
    parameter_name = 'topic'

    def lookups(self, request, model_admin):
        return (
            ('Python', 'Python'),
            ('Ruby', 'Ruby'),
            ('Java', 'Java'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains=self.value())


class YearListFilter(admin.SimpleListFilter):
    title = "Year created"
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = list(set(list(models.Course.objects.all().values_list('created_at__year', flat=True))))
        if years:
            _years = []
            for y in years:
                _years.append((str(y), str(y)))
            return tuple(_years)
        return (
            ('2018', '2018'),
            ('2019', '2019'),
            ('2020', '2020'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(created_at__gte=date(int(self.value()), 1, 1), created_at__lte=date(int(self.value()), 12, 31))


class CourseAdmin(admin.ModelAdmin):
    inlines = [TextStepInline, QuizStepInline]
    search_fields = ['title', 'description']
    list_filter = ['created_at', YearListFilter, TopicListFilter]
    list_display = ['title', 'teacher', 'created_at', 'time_to_complete', 'status']
    actions = [make_published]
    # list_display_links = ['title', 'description']
    list_editable = ['status']


class AnswerInline(admin.TabularInline):
    model = models.Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    search_fields = ['prompt']
    list_display = ['prompt', 'quiz', 'order']
    list_editable = ['quiz', 'order']
    radio_fields = {'quiz': admin.HORIZONTAL}


class QuizAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'description', 'order', 'total_questions']


class TextAdmin(admin.ModelAdmin):
    # fields = ['course', 'title', 'order', 'description', 'content']
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'order', 'description')
        }),
        ('Add content', {
            'fields': ('content',),
            'classes': ('collapse',)
        })
    )

# admin.AdminSite.site_header = 'asdf'

admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.TextStep, TextAdmin)
admin.site.register(models.QuizStep, QuizAdmin)
admin.site.register(models.MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(models.TrueFalseQuestion)
admin.site.register(models.Answer)

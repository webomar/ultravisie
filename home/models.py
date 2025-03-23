
from wagtail.models import Page
from django.db import models


class HomePage(Page):
    pass

from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.forms.models import AbstractEmailForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    content_panels = Page.content_panels + [
        InlinePanel('form_fields', label="Form fields"),

    ]
    def send_mail(self, form):
        """Send an HTML email with form submission data"""
        context = {
            "name": form.cleaned_data.get("naam"),
            "email": form.cleaned_data.get("email"),
            "message": form.cleaned_data.get("bericht"),
        }

        html_content = render_to_string("emails/email_template.html", context)
        plain_text_content = strip_tags(html_content)
        print('plain_text_content')
        print(plain_text_content)
        print('context')
        print(context)

        email = EmailMultiAlternatives(
            subject=self.subject or "Nieuw Contactformulier Inzending",
            body=plain_text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["omaralubwani@yahoo.com"],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()
    def process_form_submission(self, form):
        self.send_mail(form)  # Call your custom mail function
        return super().process_form_submission(form)  # Call the default behavior

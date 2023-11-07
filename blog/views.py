from django.shortcuts import render
from django.views.generic import TemplateView

from blog.models import Article
import json

from blog.utils import gpt_turbo_model_request, gpt_functionless_request


class IndexView(TemplateView):
    template_name = 'index.html'


class CreateArticleView(TemplateView):
    template_name = 'snippets/monetizable_items.html'

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content')
        article = Article.objects.create(content=content)
        # Prompt to generate monetizable items from the article
        prompt = (f"This is an article from the lampoon's website, '{article.content}'. "
                  f"I want to have an advertisement on this page, "
                  f"could you go through the article and find the monetizable items in the provided article"
                  f" and return them to me in a comma seperated list?")
        response = gpt_turbo_model_request(prompt, function_id=0)
        # print("Response: ", response)
        monetizable_items = response.get('monetizable_items')
        if isinstance(monetizable_items, str):
            monetizable_items = monetizable_items.split(',')
            monetizable_items = [monetizable_item.strip() for monetizable_item in monetizable_items]
        context = {'monetizable_items': monetizable_items}
        return render(request, self.template_name, context)


class GetCompanyGenreView(TemplateView):
    template_name = 'snippets/company_types.html'

    def get(self, request, *args, **kwargs):
        monetizable_item = kwargs.get('monetizable_item')
        # Prompt to generate a list of business types related to the monetizable item
        prompt = (f"Please provide a comma separated list of business types related to the following item: "
                  f"'{monetizable_item}', make sure the list is comma separated and not a numbered list."
                  f"Also skip any pretext or human like responses and just provide the list of business types.")
        response = gpt_functionless_request(prompt)
        # response = gpt_turbo_model_request(prompt, function_id=1)
        # business_types = response.get('business_types')
        business_types = response
        if isinstance(business_types, str):
            # split the string into a list and remove any spaces at the beginning or end of the string
            business_types = business_types.split(',')
            business_types = [business_type.strip() for business_type in business_types]
        context = {'company_genres': business_types}
        return render(request, self.template_name, context)


class GetTopCompaniesView(TemplateView):
    template_name = 'snippets/top_companies.html'

    def get(self, request, *args, **kwargs):
        business_type = request.GET.get('company_genre')
        # Prompt to generate a list of business types related to the monetizable item
        prompt = (f"Please provide a comma separated list of the top 10 companies in the following business category:"
                  f"'{business_type}', make sure these are actual companies and not just random words."
                  f"Search the internet if you can't think of any companies.")
        response = gpt_turbo_model_request(prompt, function_id=2)

        if response:
            # response = gpt_functionless_request(prompt)
            top_companies = response.get('top_companies')
            # top_companies = response
            if isinstance(top_companies, str):
                # split the string into a list and remove any spaces at the beginning or end of the string
                top_companies = top_companies.split(',')
                top_companies = [company.strip() for company in top_companies]
            context = {'top_companies': top_companies}
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})


class ContactAndDraftView(TemplateView):
    template_name = 'snippets/contact_and_draft.html'

    def get(self, request, *args, **kwargs):
        company_name = request.GET.get('company_name')
        # Prompt to generate a list of business types related to the monetizable item
        prompt = (f"Please draft an email to the following company: '{company_name}',"
                  f" also find the contact us page link for the company and provide it to me.")
        # response = gpt_functionless_request(prompt)
        response = gpt_turbo_model_request(prompt, function_id=3)
        if response:
            contact_info = response.get('contact_info')
            try:
                contact_info_json = json.loads(contact_info)
                contact_info = ""
                for key, value in contact_info_json.items():
                    # contact_info += f"{key.capitalize()}: {value.strip()} \n\n"
                    contact_info += f"{value.strip()}\n\n"
            except Exception as e:
                print("Error: ", e)
            draft = response.get('draft')
            context = {'draft': draft, 'contact_info': contact_info}
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})

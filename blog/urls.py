from django.urls import path
from .views import IndexView, CreateArticleView, GetCompanyGenreView, GetTopCompaniesView, ContactAndDraftView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_article/', CreateArticleView.as_view(), name='create_article'),
    path('get_company_genre/<str:monetizable_item>/', GetCompanyGenreView.as_view(), name='get_company_types'),
    path('get_top_companies/', GetTopCompaniesView.as_view(), name='get_top_companies'),
    path('contact_and_draft/', ContactAndDraftView.as_view(), name='contact_and_draft'),
]

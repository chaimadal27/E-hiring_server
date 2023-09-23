from django.urls import path

from . import views

urlpatterns = [
    # partners urls
    path(r'partnerships', views.CompanyCreateAPIView.as_view()),
    path(r'partnerships/<int:pk>', views.CompanyRetrieveUpdateAPIView.as_view()),
    path(r'partnerships/<int:pk>/activate', views.CompanyActivateAPIView.as_view()),
    path(r'partnerships/<int:pk>/deactivate', views.CompanyDeactivateAPIView.as_view()),
    path(r'partnerships/export', views.ExportCompany.as_view()),
    path(r'partnerships/all', views.AllCompaniesListAPIView.as_view()),
    path(r'partnerships/list', views.AllCompaniesNamesList.as_view()),

    # contact urls
    path(r'contacts/', views.ContactCreateAPIView.as_view()),
    path(r'contacts/<int:pk>', views.ContactRetrieveUpdateAPIView.as_view()),
    path(r'contacts/list', views.AllContactsByCompanyList.as_view()),

    # schools urls
    path(r'schools', views.SchoolCreateAPIView.as_view()),
    path(r'schools/<int:pk>', views.SchoolRetrieveUpdateAPIView.as_view()),
    path(r'schools/<int:pk>/activate', views.SchoolActivateAPIView.as_view()),
    path(r'schools/<int:pk>/deactivate', views.SchoolDeactivateAPIView.as_view()),
    path(r'schools/all', views.AllSchoolsListAPIView.as_view()),
    path(r'schools/list', views.AllSchoolsNamesList.as_view()),
    path(r'schools/export', views.ExportSchool.as_view()),

    # JobCategories urls
    path(r'job_categories', views.JobCategoryCreateAPIView.as_view()),
    path(r'job_categories/<int:pk>', views.JobCategoryRetrieveUpdateAPIView.as_view()),
    path(r'job_categories/<int:pk>/activate', views.JobCategoryActivateAPIView.as_view()),
    path(r'job_categories/<int:pk>/deactivate', views.JobCategoryDeactivateAPIView.as_view()),
    path(r'job_categories/export', views.ExportJobCategory.as_view()),
    path(r'job_categories/all', views.AllJobCategoriesListAPIView.as_view()),
    
    # job urls
    path(r'jobs/', views.JobCreateAPIView.as_view()),
    path(r'jobs/<int:pk>', views.JobRetrieveUpdateAPIView.as_view()),
    path(r'jobs/list', views.AllJobsByCategoryList.as_view()),
    # path(r'jobs/<int:pk>/validate', views.JobValidateAPIView.as_view()),
    path(r'jobs/<int:pk>/validate', views.ValidJobView.as_view()),
    path(r'jobs/<int:pk>/reject', views.RejectJobView.as_view()),
]

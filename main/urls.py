from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('developers/', views.developers, name='developers'),
    path('developers/<int:id>/', views.developer, name='developer'),
    path('developer/save/<int:dev_id>', views.add_developer_saved, name='save-developer'),
    path('developer/remove/<int:dev_id>', views.remove_developer_saved, name='remove-developer'),

    path('projects/', views.projects, name='projects'),
    path('projects/<int:id>/', views.project, name='project'),
    path('project/save/<int:prj_id>', views.add_project_saved, name='save-project'),
    path('project/remove/<int:prj_id>', views.remove_project_saved, name='remove-project'),

    path('saved/', views.saved, name='saved'),

    path('transactions/', views.transactions, name='transactions'),
    path('transactions/add/', views.add_transaction, name='add-transaction'),
    path('transactions/delete/<int:transaction_id>', views.delete_transaction, name='delete-transaction'),

    path('auth/', include('authentication.urls')),
]

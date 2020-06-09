from django.urls import path
from student_manager import views as student_manager_views

urlpatterns = [
    path('get_student_data/<str:id>', student_manager_views.get_student_data, name='get_student_data'),
    path('update_student_progress/<str:id>/<str:unit>/<str:unit_id>', student_manager_views.update_student_progress, name='update_student_progress'),
    path('signup', student_manager_views.signup, name='student_signup'),
    path('store_mark', student_manager_views.store_mark, name='store_mark'),
]
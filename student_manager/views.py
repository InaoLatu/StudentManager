from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from student_manager.forms import StudentCreateForm, UserCreateForm
from student_manager.models import Student, UnitProgress, MicroContentProgress
import requests
from StudentManager import constants
import logging
from django.conf import settings

appLog = settings.BASE_DIR + 'app.log'
logging.basicConfig(filename=appLog, filemode='w', format='%(levelname)s - %(message)s')

def signup(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        student_form = StudentCreateForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            micro_content_progress = MicroContentProgress.objects.create(title="mc_aux")
            mc = [micro_content_progress]
            unit_progress = UnitProgress.objects.create(name="unit_progress", micro_contents=mc)
            progress = [unit_progress]
            #student = Student.objects.create(user=user, faculty=request.POST["faculty"],
            #                                 birth_date=request.POST['birth_date'], progress=progress)
            student = Student.objects.create(user=user, birth_date=request.POST['birth_date'], progress=progress)
            student.save()

            return render(request, 'student_manager/confirm_registration.html')
    else:
        user_form = UserCreateForm()
        student_form = StudentCreateForm()

    return render(request, 'student_manager/signup.html', {'user_form': user_form, 'student_form': student_form})


def get_student_data(request, **kwargs):
    return JsonResponse(Student.objects.get(telegram_id=kwargs['id']).to_dict())


def update_student_progress(request, **kwargs):
    request_string = constants.AUTHORING_TOOL_IP + "units/" + kwargs['unit']
    unit_micro_content = requests.get(request_string).json()
    print(unit_micro_content)
    mc_list = []
    for mc in unit_micro_content:
        mc_list.append(MicroContentProgress.objects.create(id=mc['id'], title=mc['title']))

    new_unit = UnitProgress.objects.create(id=kwargs['unit_id'], name=kwargs['unit'], micro_contents=mc_list)

    student = Student.objects.get(telegram_id=kwargs['id'])
    student.progress.append(new_unit)
    student.save()

    micro_content_list = new_unit.to_dict()['micro_contents']
    print(micro_content_list)

    return JsonResponse(micro_content_list, safe=False)


@csrf_exempt
def store_mark(request, **kwargs):
    global unit, unit_id, microcontent_id
    student = Student.objects.get(telegram_id=request.POST['student_id'])

    for unit_id, unit in enumerate(student.progress):
        if unit.id == int(request.POST['unit_id']):
            break

    for microcontent_id, microcontent in enumerate(student.progress[unit_id].micro_contents):
        if microcontent.id == int(request.POST['microcontent_id']):
            break

    if float(request.POST['mark']) > student.progress[unit_id].micro_contents[microcontent_id].mark:
        student.progress[unit_id].micro_contents[microcontent_id].mark = float(request.POST['mark'])
    if float(request.POST['mark']) > 50:
        student.progress[unit_id].micro_contents[microcontent_id].completed = True

    logging.warning("Student: " + request.POST['student_id'] + " obtained a " + request.POST['mark'] + " in microcontent: " + request.POST['microcontent_id'])

    student.save()
    print(student.progress[unit_id].micro_contents[microcontent_id].mark)

    return HttpResponse("mark stored", status=200)

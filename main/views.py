from django.shortcuts import render, redirect, get_object_or_404
from .models import  People,Employee,Committee,Department,EmployeeCommittee
from .decorators import user_logged_in,custom_never_cache
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import logout as django_logout


def index(request):
    return render(request, 'index.html')

@custom_never_cache
@user_logged_in
def model(request):
    model_objects = Employee.objects.all()
    return render(request, 'model.html', {'model_objects': model_objects})
@custom_never_cache
@user_logged_in
def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        salary = request.POST.get('salary')
        department_id = request.POST.get('departments')
        committee_ids = request.POST.getlist('committees')

        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            messages.error(request, 'Selected department does not exist.')
            return redirect('add_employee')

        # Check if an employee with the same name already exists
        if Employee.objects.filter(name=name).exists():
            messages.error(request, 'Employee with this name already exists.')
        else:
            employee = Employee.objects.create(name=name, age=age, salary=salary, department=department)

            for committee_id in committee_ids:
                try:
                    committee = Committee.objects.get(pk=committee_id)
                    EmployeeCommittee.objects.create(employee=employee, committee=committee)
                except Committee.DoesNotExist:
                    messages.warning(request, f'Committee with id {committee_id} does not exist.')

            # Redirect to the appropriate page after successful creation
            return redirect('model')

    all_committees = Committee.objects.all()
    all_departments = Department.objects.all()
    return render(request, 'add_employee.html', {'all_committees': all_committees, 'all_departments': all_departments})


@custom_never_cache
@user_logged_in
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        salary = request.POST.get('salary')
        department_id = request.POST.get('departments')  # Get department ID from form
        committee_ids = request.POST.getlist('committees')

        employee.name = name
        employee.age = age
        employee.salary = salary
        employee.department_id = department_id  # Assign department ID
        employee.save()

        # Clear existing committee associations
        EmployeeCommittee.objects.filter(employee=employee).delete()

        # Create new associations with selected committees
        for committee_id in committee_ids:
            try:
                committee = Committee.objects.get(pk=committee_id)
                EmployeeCommittee.objects.create(employee=employee, committee=committee)
            except Committee.DoesNotExist:
                messages.warning(request, f'Committee with id {committee_id} does not exist.')

        return redirect('model')

    else:  # If request method is GET
        all_committees = Committee.objects.all()
        employee_committee_ids = EmployeeCommittee.objects.filter(employee=employee).values_list('committee_id', flat=True)
        all_departments = Department.objects.all()
        return render(request, 'edit_employee.html', {'employee': employee, 'all_committees': all_committees, 'all_departments': all_departments, 'employee_committee_ids': employee_committee_ids})

@custom_never_cache
@user_logged_in
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            employee.delete()
            return redirect('model')
        elif action == 'cancel':
            return redirect('model')
    return render(request, 'delete_employee.html', {'employee': employee})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if People.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'User with this name already exists'})
        else:
            hashed_password = make_password(password)
            user = People.objects.create(username=username,password=hashed_password)
            user.save()
            return redirect('custom_login')

    return render(request, 'register.html')

@custom_never_cache
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = People.objects.get(username=username)
        except People.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['username'] = user.username


            print("Session user_id:", request.session.get('user_id'))
            print("Session username:", request.session.get('username'))

            return redirect('model')
        else:
            return render(request, 'login.html', {'message': 'Invalid username or password'})

    return render(request, 'login.html')
@custom_never_cache
@user_logged_in
def logout(request):
    django_logout(request)
    return redirect('index')












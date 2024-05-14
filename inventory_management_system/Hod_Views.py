from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum,F,DurationField
from django.urls import reverse

import csv

from .forms import *


@login_required(login_url='/')
def home(request):
    item_count = Item.objects.all().count()
    department_count = Department.objects.all().count()
    location_count = Location.objects.all().count()
    staff_count = Staff.objects.all().count()
    expired = Medicine.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True).count()

    medicines = Medicine.objects.all()
    
    expiring_meds = []
    for medicine in medicines:
        remaining_days = medicine.days_until_expiration
        if remaining_days is not None and 0 < remaining_days < 10:
            expiring_meds.append(medicine)

    context = {
        'item_count': item_count,
        'department_count': department_count,
        'location_count': location_count,
        'staff_count': staff_count,
        'expiring_meds': expiring_meds,
        "expired_total": expired,
    }

    return render(request, 'Hod/home.html', context)

@login_required(login_url='/')
def add_items(request):
    department = Department.objects.all()
    location = Location.objects.all()
    purpose = Purpose.objects.all()
    category = Category.objects.all()

    if request.method == "POST":
        item_pic = request.FILES.get('item_pic')
        item_name = request.POST.get('item_name')
        specification = request.POST.get('specification')
        quantity = request.POST.get('quantity')
        total_amount = request.POST.get('total_amount')
        category_id = request.POST.get('category_id')
        date_of_purchase = request.POST.get('date_of_purchase')
        department_id = request.POST.get('department_id')
        location_id = request.POST.get('location_id')
        purpose_id = request.POST.get('purpose_id')

        department = Department.objects.get(id=department_id)
        location = Location.objects.get(id=location_id)
        purpose = Purpose.objects.get(id=purpose_id)
        category = Category.objects.get(id=category_id)

        if Item.objects.filter(item_name=item_name).exists():
            messages.warning(request, 'Item already exits.')
            return redirect('add_items')
        else:
            item = Item(
                item_pic=item_pic,
                item_name=item_name,
                specification=specification,
                quantity=quantity,
                total_amount=total_amount,
                category_id=category,
                date_of_purchase=date_of_purchase,
                department_id=department,
                location_id=location,
                purpose_id=purpose
            )
            item.save()
            messages.success(request, item.item_name + " " + "Successfully Added.")
            return redirect('add_items')
        
    context = {
        'category': category,
        'department': department,
        'location': location,
        'purpose': purpose
    }

    return render(request, 'Hod/add_items.html', context)


@login_required(login_url='/')
def view_items(request):
    item = Item.objects.all()
    recent_items = Item.objects.order_by('-created_at')[:10]

    context = {
        'item': item,
        'recent_items': recent_items,
    }
    return render(request, 'Hod/view_items.html', context)


@login_required(login_url='/')
def edit_items(request, id):
    item = Item.objects.filter(id=id)
    category = Category.objects.all()
    department = Department.objects.all()
    location = Location.objects.all()
    purpose = Purpose.objects.all()

    context = {
        'item': item,
        'category': category,
        'department': department,
        'location': location,
        'purpose': purpose
    }
    return render(request, 'Hod/edit_items.html', context)


@login_required(login_url='/')
def update_items(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item_pic = request.FILES.get('item_pic')
        item_name = request.POST.get('item_name')
        specification = request.POST.get('specification')
        quantity = request.POST.get('quantity')
        total_amount = request.POST.get('total_amount')
        category_id = request.POST.get('category_id')
        date_of_purchase = request.POST.get('date_of_purchase')
        department_id = request.POST.get('department_id')
        location_id = request.POST.get('location_id')
        purpose_id = request.POST.get('purpose_id')

        item = Item.objects.get(id=item_id)

        if item_pic != None and item_pic != "":
            item.item_pic = item_pic

        item.item_name = item_name
        item.specification = specification
        item.quantity = quantity
        item.total_amount = total_amount
        category = Category.objects.get(id=category_id)
        item.category_id = category
        item.date_of_purchase = date_of_purchase
        department = Department.objects.get(id=department_id)
        item.department_id = department

        location = Location.objects.get(id=location_id)
        item.location_id = location

        purpose = Purpose.objects.get(id=purpose_id)
        item.purpose_id = purpose

        item.save()
        messages.success(request, 'Item Successfully Updated.')
        return redirect('view_items')

    return render(request, 'Hod/edit_items.html')


@login_required(login_url='/')
def delete_items(request, id):
    item = Item.objects.get(id=id)
    item.delete()
    messages.success(request, 'Item Successfully Deleted.')
    return redirect('view_items')


@login_required(login_url='/')
def item_request(request):
    staff_request = ItemRequest.objects.select_related('staff_id').values('staff_id', 'staff_id__user__first_name', 'staff_id__user__last_name').distinct()
    recent_request = ItemRequest.objects.order_by("-created_at")[:10]


    context = {
        'staff_request': staff_request,
        'recent_request': recent_request,
    }
    return render(request, 'Hod/item_request_view.html', context)


@login_required(login_url='/')
def item_request_detail(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    item_requests = ItemRequest.objects.filter(staff_id=staff_id)

    context = {
        'staff': staff,
        'item_requests': item_requests,
    }

    return render(request, 'Hod/staff_request.html', context)



# @login_required(login_url='/')
# def item_request_detail(request, staff_id):
#     print("Staff ID:", staff_id)
#     item_requests = ItemRequest.objects.filter(staff_id=staff_id)
#     print("QuerySet:", item_requests)
#     context = {
#         'item_requests': item_requests,
#     }
#     return render(request, 'Hod/staff_request.html', context)


def approve_request(request, id):
    request = ItemRequest.objects.get(id=id)
    request.status = 1
    request.save()
    return redirect('request_view')


def deny_request(request, id):
    request = ItemRequest.objects.get(id=id)
    request.status = 2
    request.save()
    return redirect('request_view')


def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)

    context = {
        "item": item,
    }
    return render(request, 'Hod/item_detail.html', context)


def issue_item(request, pk):
    issued_item = Item.objects.get(id=pk)
    out_form = StockOutForm(request.POST)

    if request.method == 'POST':
        if out_form.is_valid():
            new_out = out_form.save(commit=False)
            new_out.item = issued_item
            new_out.save()

            issued_quantity = int(request.POST['quantity'])
            issued_item.quantity -= issued_quantity
            issued_item.save()

            return redirect('receipt')
    return render(request, 'Hod/issue_item.html', {'out_form': out_form})

    # stock_out_form = StockOutForm(request.POST)
    # try:

    # data = [
    # '<h3>The Customer data inserted properly.]


#         new_stock_out = stock_out_form.save(commit=False)
#         new_stock_out.item = issued_item
#         new_stock_out.total_amount = issued_item.total_amount
#         new_stock_out.save()
#
#         issued_quantity = int(request.POST['quantity'])
#         issued_item.quantity -= issued_quantity
#         issued_item.save()
#
#     return redirect('receipt')
#
# return render(request, 'Hod/issue_item.html', {'stock_out_form': stock_out_form})

#         try:
#             return redirect('receipt')
#         except:
#             pass
# else:
#     stock_out_form = StockOutForm()


def add_to_stock(request, pk):
    issued_item = Item.objects.get(id=pk)
    form = AddForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            added_quantity = int(request.POST['received_quantity'])
            issued_item.quantity += added_quantity
            issued_item.save()

            # To add to the remaining stock quantity is reducing
            print(added_quantity)
            print(issued_item.quantity)

            return redirect('view_items')
    return render(request, 'Hod/add_to_stock.html', {'form': form})


def stock_out(request):
    stocks = StockOut.objects.all().order_by('-id')
    return render(request, 'Hod/receipt.html',
                  {
                      'stocks': stocks,
                  })


def receipt(request):
    sales = Sale.objects.all().order_by('-id')
    return render(request,
                  'Hod/receipt.html',
                  {
                      'sales': sales,
                  })


def reorder_level(request, pk):
    queryset = Medicine.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.medicine_name) + " is updated to " + str(
            instance.reorder_level))

        return redirect("manage_medicine")
    context = {
        "instance": queryset,
        "form": form,
        "title": "Reorder Level"
    }

    return render(request, 'Hod/reorder_level.html', context)


@login_required(login_url='/')
def add_departments(request):
    if request.method == "POST":
        department_name = request.POST.get('department_name')

        department = Department(
            name=department_name
        )
        department.save()
        messages.success(request, 'Department Successfully Added.')
        return redirect('add_departments')

    return render(request, 'Hod/add_department.html')


@login_required(login_url='/')
def view_departments(request):
    department = Department.objects.all()
    context = {
        'department': department,
    }
    return render(request, 'Hod/view_departments.html', context)


@login_required(login_url='/')
def edit_departments(request, id):
    department = Department.objects.get(id=id)

    context = {
        'department': department,
    }
    return render(request, 'Hod/edit_departments.html', context)


@login_required(login_url='/')
def update_departments(request):
    if request.method == "POST":
        department_name = request.POST.get('name')
        department_id = request.POST.get('department_id')

        department = Department.objects.get(id=department_id)
        department.name = department_name
        department.save()
        messages.success(request, 'Department Successfully Updated')
        return redirect('view_departments')

    return render(request, 'Hod/edit_departments.html')


@login_required(login_url='/')
def delete_departments(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    messages.success(request, 'Department Successfully Deleted.')
    return redirect('view_departments')


@login_required(login_url='/')
def add_locations(request):
    if request.method == "POST":
        location_name = request.POST.get('location_name')

        location = Location(
            name=location_name
        )
        location.save()
        messages.success(request, 'Location Successfully Added.')
        return redirect('add_locations')

    return render(request, 'Hod/add_locations.html')


@login_required(login_url='/')
def view_locations(request):
    location = Location.objects.all()
    context = {
        'location': location,
    }
    return render(request, 'Hod/view_locations.html', context)


@login_required(login_url='/')
def edit_locations(request, id):
    location = Location.objects.get(id=id)

    context = {
        'location': location,
    }
    return render(request, 'Hod/edit_locations.html', context)


@login_required(login_url='/')
def update_locations(request):
    if request.method == "POST":
        location_name = request.POST.get('name')
        location_id = request.POST.get('location_id')

        location = Location.objects.get(id=location_id)
        location.name = location_name
        location.save()
        messages.success(request, 'Location Successfully Updated')
        return redirect('view_locations')

    return render(request, 'Hod/edit_locations.html')


@login_required(login_url='/')
def delete_locations(request, id):
    location = Location.objects.get(id=id)
    location.delete()
    messages.success(request, 'Location Successfully Deleted.')
    return redirect('view_locations')


@login_required(login_url='/')
def add_purposes(request):
    if request.method == "POST":
        purpose_name = request.POST.get('purpose_name')

        purpose = Purpose(
            name=purpose_name
        )
        purpose.save()
        messages.success(request, 'Purpose Successfully Added.')
        return redirect('add_purposes')

    return render(request, 'Hod/add_purposes.html')


@login_required(login_url='/')
def view_purposes(request):
    purpose = Purpose.objects.all()
    context = {
        'purpose': purpose,
    }
    return render(request, 'Hod/view_purposes.html', context)


@login_required(login_url='/')
def edit_purposes(request, id):
    purpose = Purpose.objects.get(id=id)

    context = {
        'purpose': purpose,
    }
    return render(request, 'Hod/edit_purposes.html', context)


@login_required(login_url='/')
def update_purposes(request):
    if request.method == "POST":
        purpose_name = request.POST.get('name')
        purpose_id = request.POST.get('purpose_id')

        purpose = Purpose.objects.get(id=purpose_id)
        purpose.name = purpose_name
        purpose.save()
        messages.success(request, 'Purpose Successfully Updated')
        return redirect('view_purposes')

    return render(request, 'Hod/edit_purposes.html')


@login_required(login_url='/')
def delete_purposes(request, id):
    purpose = Purpose.objects.get(id=id)
    purpose.delete()
    messages.success(request, 'Purpose Successfully Deleted.')
    return redirect('view_purposes')


@login_required(login_url='/')
def add_categories(request):
    if request.method == "POST":
        category_name = request.POST.get('category_name')

        category = Category(
            name=category_name
        )
        category.save()
        messages.success(request, 'Category Successfully Added.')
        return redirect('add_categories')

    return render(request, 'Hod/add_categories.html')


@login_required(login_url='/')
def view_categories(request):
    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'Hod/view_categories.html', context)


@login_required(login_url='/')
def edit_categories(request, id):
    category = Category.objects.get(id=id)

    context = {
        'category': category,
    }
    return render(request, 'Hod/edit_categories.html', context)


@login_required(login_url='/')
def update_categories(request):
    if request.method == "POST":
        category_name = request.POST.get('name')
        category_id = request.POST.get('category_id')

        category = Category.objects.get(id=category_id)
        category.name = category_name
        category.save()
        messages.success(request, 'Category Successfully Updated')
        return redirect('view_categories')

    return render(request, 'Hod/edit_categories.html')


@login_required(login_url='/')
def delete_categories(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, 'Category Successfully Deleted.')
    return redirect('view_categories')


@login_required(login_url='/')
def add_staff(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken!')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken!')
            return redirect('add_staff')
        else:
            user = CustomUser(first_name=first_name, last_name=last_name, email=email, username=username,
                              profile_pic=profile_pic, user_type=2)
            user.set_password(password)
            user.save()

            staff = Staff(
                user=user,
            )
            staff.save()
            messages.success(request, 'Staff Successfully Added!')
            return redirect('add_staff')
    return render(request, 'Hod/add_staff.html')


@login_required(login_url='/')
def view_staff(request):
    staff = Staff.objects.all()

    context = {
        'staff': staff,
    }

    return render(request, 'Hod/view_staff.html', context)


@login_required(login_url='/')
def edit_staff(request, id):
    staff = Staff.objects.filter(id=id)

    context = {
        'staff': staff
    }
    return render(request, 'Hod/edit_staff.html', context)


@login_required(login_url='/')
def update_staff(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)

        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        user.save()

        messages.success(request, 'Staff Updated Successfully!')
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')


@login_required(login_url='/')
def delete_staff(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Record Successfully Deleted!')
    return redirect('view_staff')


@login_required(login_url='/')
def leave_view(request):
    # Retrieve StaffLeave objects along with the related Staff objects
    staff_leave = StaffLeave.objects.select_related('staff_id').values('staff_id', 'staff_id__user__first_name', 'staff_id__user__last_name').distinct()

    recent_leave = StaffLeave.objects.order_by("-created_at")[:10]

    context = {
        'staff_leave': staff_leave,
        'recent_leave': recent_leave,
    }
    return render(request, 'Hod/staff_view.html', context)


# Common function to calculate remaining leave days
def calculate_remaining_leave(original_leave_balance, used_leave_days, used_half_day_leaves):
    remaining_leave = original_leave_balance - (used_leave_days  + 0.5 * used_half_day_leaves)
    return remaining_leave

@login_required(login_url='/')
def leave_detail(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    leave_requests = StaffLeave.objects.filter(staff_id=staff_id)

    # Calculate the used leave days for each leave type
    annual_leaves = leave_requests.filter(leave_type='annual', status=1)
    used_annual_leave = sum((leave.to_date - leave.from_date).days + (0.5 if leave.half_day else 1) for leave in annual_leaves)

    sick_leaves = leave_requests.filter(leave_type='sick', status=1)
    used_sick_leave = sum((leave.to_date - leave.from_date).days + (0.5 if leave.half_day else 1) for leave in sick_leaves)

    lieu_leaves = leave_requests.filter(leave_type='lieu', status=1)
    used_lieu_leave = sum((leave.to_date - leave.from_date).days + (0.5 if leave.half_day else 1) for leave in lieu_leaves)

    # Calculate the count of half day, full day, and multiple days leaves
    half_day_leaves_count = leave_requests.filter(half_day=True).count()
    full_day_leaves_count = leave_requests.filter(half_day=False).count()
    multiple_days_leaves_count = len(leave_requests) - half_day_leaves_count - full_day_leaves_count

    # Calculate the remaining leave days for each leave type
    original_annual_leave = 18.0
    original_sick_leave = 12.0
    original_lieu_leave = 3.0

    # Reduce half-day leave balance for each leave type
    remaining_annual_leave = original_annual_leave - used_annual_leave
    remaining_sick_leave = original_sick_leave - used_sick_leave
    remaining_lieu_leave = original_lieu_leave - used_lieu_leave

    # Ensure the remaining leave days are not negative
    remaining_annual_leave = max(remaining_annual_leave, 0)
    remaining_sick_leave = max(remaining_sick_leave, 0)
    remaining_lieu_leave = max(remaining_lieu_leave, 0)

    context = {
        'staff': staff,
        'leave_requests': leave_requests,
        'annual_leave': remaining_annual_leave,
        'sick_leave': remaining_sick_leave,
        'lieu_leave': remaining_lieu_leave,
        'half_day_leaves_count': half_day_leaves_count,
        'full_day_leaves_count': full_day_leaves_count,
        'multiple_days_leaves_count': multiple_days_leaves_count,
    }

    return render(request, 'Hod/staff_leave.html', context)

@login_required(login_url='/')
def approve_leave(request, id):
    leave = get_object_or_404(StaffLeave, id=id)
    staff_id = leave.staff_id.id  # Capture the staff_id before changing the leave status

    # Save updated leave record and staff
    leave.status = 1  # Set leave status as accepted
    leave.save()
    leave.staff_id.save()

    messages.success(request, 'Leave request accepted.')
    return redirect(reverse('leave_detail', args=[staff_id]))


@login_required(login_url='/')
def disapprove_leave(request, id):
    leave = StaffLeave.objects.get(id=id)
    staff_id = leave.staff_id.id  # Capture the staff_id before changing the leave status
    
    leave.status = 2
    leave.save()
    messages.error(request, 'Leave request denied.')
    return redirect(reverse('leave_detail', args=[staff_id]))


def feedback(request):
    feedback = StaffFeedback.objects.all()

    see_feedback = StaffFeedback.objects.all().order_by('-id')[0:5]
    context = {
        'feedback': feedback,
        'see_feedback': see_feedback,
    }
    return render(request, 'Hod/staff_feedback.html', context)


def feedback_save(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = StaffFeedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()

    return redirect('feedback')


def add_medicines(request):
    form = MedicineForm(request.POST, request.FILES)
    if form.is_valid():
        form = MedicineForm(request.POST, request.FILES)

        form.save()
        messages.success(request, 'Added Successfully')

        return redirect('add_medicines')

    context = {
         "form": form,
        "title": "Add New Drug"
    }

    return render(request, 'Hod/add_medicines.html', context)


def view_medicines(request):
    medicine = Medicine.objects.all().order_by("-id")
    ex = Medicine.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo = Medicine.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)

    context = {
        "medicine": medicine,
        "expired": ex,
        "expa": eo,
        "title": "Manage Stocked Drugs"
    }
    return render(request, 'Hod/view_medicines.html', context)


def edit_medicines(request, pk):
    medicines = Medicine.objects.get(id=pk)
    form = MedicineForm(request.POST or None, instance=medicines)

    if request.method == "POST":
        if form.is_valid():
            form = MedicineForm(request.POST or None, instance=medicines)

            medicine_name = request.POST.get('medicine_name')
            quantity = request.POST.get('quantity')

            try:
                medicines = Medicine.objects.get(id=pk)
                medicines.medicine_name = medicine_name
                medicines.quantity = quantity
                medicines.save()
                form.save()
                messages.success(request, "Updated Successfully")
            except:
                messages.error(request, 'Error!')

    context = {
        "medicines": medicines,
        "form": form,
        "title": "Edit Drug"
    }
    return render(request, 'Hod/edit_medicines.html', context)


def manage_medicines(request):
    medicines = Medicine.objects.all().order_by("-id")
    ex = Medicine.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=True)
    eo = Medicine.objects.annotate(
        expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField())
    ).filter(expired=False)
    
    
    context = {
        "medicines": medicines,
        "expired": ex,
        "expa": eo,
        "title": "Manage Stocked Medicines"
    }
    return render(request, 'Hod/manage_medicine.html', context)


def medicine_detail(request, pk):
    medicines = Medicine.objects.get(id=pk)
    
    expiring_meds = []
    if medicines.days_until_expiration < 10:
        expiring_meds.append(medicines)

    context = {
        "medicines": medicines,
        "expiring_meds": expiring_meds,
    }
    return render(request, 'Hod/view_medicines.html', context)


def delete_medicine(request, pk):
    try:

        medicines = Medicine.objects.get(id=pk)
        if request.method == 'POST':
            medicines.delete()
            messages.success(request, "Deleted Successfully!")

            return redirect('manage_medicine')

    except:
        messages.error(request, "Already Deleted!")
        return redirect('manage_medicine')

    return render(request, 'Hod/sure_delete.html')


def issue_medicine(request, pk):
    issued_medicine = Medicine.objects.get(id=pk)
    dispense = DispenseForm(request.POST)

    if request.method == 'POST':
        if dispense.is_valid():
            new_out = dispense.save(commit=False)
            new_out.medicine = issued_medicine
            new_out.save()

            issued_quantity = int(request.POST['dispense_quantity'])
            issued_medicine.quantity -= issued_quantity
            issued_medicine.save()

            return redirect('dispense_receipt')
    return render(request, 'Hod/issue_medicine.html', {'dispense': dispense})


def add_to_stock_medicine(request, pk):
    issued_medicine = Medicine.objects.get(id=pk)
    form = AddForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            added_quantity = int(request.POST['received_quantity'])
            issued_medicine.quantity += added_quantity
            issued_medicine.save()

            # To add to the remaining stock quantity is reducing
            print(added_quantity)
            print(issued_medicine.quantity)

            return redirect('manage_medicine')
    return render(request, 'Hod/add_to_stock.html', {'form': form})


def medicine_receipt(request):
    dispense = Dispense.objects.all().order_by('-id')
    return render(request,
                  'Hod/dispense_receipt.html',
                  {
                      'dispense': dispense,
                  })
    

def item_csv(request):
    table_items = Item.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="item_table.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow(['ID', 'Item Name', 'Specification', 'Quantity', 'Total Amount', 'Date of Purchase', 'Location', 'Category', 'Department', 'Purpose'])
    
    for item in table_items:
        writer.writerow([item.id, item.item_name, item.specification, item.quantity, item.total_amount, item.date_of_purchase, item.location_id.name, item.category_id.name, item.department_id.name, item.purpose_id.name])
        
    writer.writerow([])
    
    return response


def medicine_csv(request):
    table_medicines = Medicine.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="medicine_table.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow(['Bill No.', 'Medicine Name', 'Quantity', 'Manufacture', 'Drug Strength', 'Stocked Date', 'Valid To', '', 'Location', 'Remarks'])
    
    for medicine in table_medicines:
        writer.writerow([medicine.bill_no, medicine.medicine_name, medicine.quantity, medicine.manufacture, medicine.drug_strength, medicine.valid_from, medicine.valid_to, medicine.location_id, medicine.remarks])
        
    writer.writerow([])
    
    return response


    # location = Location.objects.all()
    #
    # if request.method == "POST":
    #     medicine_name = request.POST.get('medicine_name')
    #     quantity = request.POST.get('quantity')
    #     manufacture = request.POST.get('manufacture')
    #     valid_from = request.POST.get('valid_from')
    #     valid_to = request.POST.get('valid_to')
    #     location_id = request.POST.get('location_id')
    #
    #     location = Location.objects.get(id=location_id)
    #
    #     if Medicine.objects.filter(medicine_name=medicine_name).exists():
    #         messages.warning(request, 'Medicine already exits.')
    #         return redirect('add_medicines')
    #     else:
    #         medicine = Medicine(
    #             medicine_name=medicine_name,
    #             quantity=quantity,
    #             manufacture=manufacture,
    #             valid_from=valid_from,
    #             valid_to=valid_to,
    #             location_id=location,
    #         )
    #     medicine.save()
    #     messages.success(request, medicine.medicine_name + " " + "Successfully Added.")
    #     return redirect('add_medicines')
    #
    # context = {
    #     'location': location,
    # }
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from inventory.models import Staff, StaffLeave, StaffFeedback, Department, Purpose, ItemRequest
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, DurationField, Sum



@login_required(login_url='/')
def home(request):
    return render(request, 'Staff/home.html')


@login_required(login_url='/')
def apply_leave(request):
    staff = Staff.objects.get(user=request.user)
    staff_leave_history = StaffLeave.objects.filter(staff_id=staff.id)

    # Calculate the used leave days for each leave type, considering half-day leaves
    used_annual_leave = 0
    used_sick_leave = 0
    used_lieu_leave = 0

    for leave in staff_leave_history:
        days_diff = (leave.to_date - leave.from_date).days
        if leave.half_day:
            days_diff += 0.5
        else:
            days_diff += 1

        if leave.leave_type == 'annual' and leave.status == 1:
            used_annual_leave += days_diff
        elif leave.leave_type == 'sick' and leave.status == 1:
            used_sick_leave += days_diff
        elif leave.leave_type == 'lieu' and leave.status == 1:
            used_lieu_leave += days_diff

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
        'staff_leave_history': staff_leave_history,
        'annual_leave': remaining_annual_leave,
        'sick_leave': remaining_sick_leave,
        'lieu_leave': remaining_lieu_leave,
    }

    return render(request, 'Staff/apply_leave.html', context)


@login_required(login_url='/')
def apply_leave_save(request):
    if request.method == "POST":
        leave_date_str = request.POST.get('leave_date')
        leave_date = datetime.strptime(leave_date_str, '%Y-%m-%d').date()
        leave_date_to_str = request.POST.get('leave_date_to')
        leave_date_to = datetime.strptime(leave_date_to_str, '%Y-%m-%d').date() if leave_date_to_str else leave_date
        leave_type = request.POST.get('leave_type')
        reason = request.POST.get('reason')
        half_day = 'half_day' in request.POST  # Check if the checkbox is selected

        staff = Staff.objects.get(user=request.user)

        # Calculate the leave days (including half-days)
        leave_days = (leave_date_to - leave_date).days + 1  # Add 1 day to include the last day

        # If half-day leave, deduct 0.5 days from the total duration (leave_days)
        if half_day:
            leave_days -= 0.5

        # Update the remaining leave days for the chosen leave type
        if leave_type == 'annual':
            remaining_leave = staff.annual_leave
            staff.annual_leave -= leave_days  
        elif leave_type == 'sick':
            remaining_leave = staff.sick_leave
            staff.sick_leave -= leave_days
        elif leave_type == 'lieu':
            remaining_leave = staff.lieu_leave
            staff.lieu_leave -= leave_days

        # Ensure the remaining leave days are not negative
        if staff.annual_leave < 0:
            staff.annual_leave = 0
        if staff.sick_leave < 0:
            staff.sick_leave = 0
        if staff.lieu_leave < 0:
            staff.lieu_leave = 0

        staff.save()

        leave = StaffLeave(
            staff_id=staff,
            from_date=leave_date,
            to_date=leave_date_to if not half_day else leave_date,
            leave_type=leave_type,
            reason=reason,
            status=0,  # Set the leave status as pending
            half_day=half_day,
            duration=leave_days,
        )

        leave.save()
        messages.success(request, 'Leave successfully sent')

        return redirect('apply_leave')


    
def delete_leave(request, leave_id):
    try:
        leave = StaffLeave.objects.get(id=leave_id)

        # Check if the leave is pending before deleting
        if leave.status == 1:
            # Get the staff associated with the leave
            staff = leave.staff_id

            # Calculate the leave days of the leave being deleted
            leave_days = (leave.to_date - leave.from_date).days
            if leave.half_day:
                leave_days = max(0.5, leave_days)

            # Update the leave balance based on the leave type
            if leave.leave_type == 'annual':
                staff.annual_leave += leave_days
            elif leave.leave_type == 'sick':
                staff.sick_leave += leave_days
            elif leave.leave_type == 'lieu':
                staff.lieu_leave += leave_days

            # Save the staff instance to update the leave balance
            staff.save()

            leave.delete()
            messages.success(request, 'Leave request deleted successfully.')
        else:
            messages.error(request, 'Cannot delete a leave request that is not pending.')

    except StaffLeave.DoesNotExist:
        messages.error(request, 'Leave request not found.')

    return redirect('apply_leave')

    

def staff_feedback(request):
    staff_id = Staff.objects.get(user=request.user.id)

    feedback_history = StaffFeedback.objects.filter(staff_id=staff_id)

    context = {
        'feedback_history': feedback_history,
    }

    return render(request, 'Staff/feedback.html', context)


def staff_feedback_save(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')

        staff = Staff.objects.get(user=request.user.id)
        feedback = StaffFeedback(
            staff_id=staff,
            feedback=feedback,
            feedback_reply="",
        )
        feedback.save()
        messages.success(request, 'Feedback  Successfully Sent')
    return redirect('staff_feedback')


def item_request(request):
    department = Department.objects.all()
    purpose = Purpose.objects.all()

    staff = Staff.objects.filter(user=request.user.id)
    for i in staff:
        staff_id = i.id

        item_request_history = ItemRequest.objects.filter(staff_id=staff_id)

    context = {
        'department': department,
        'purpose': purpose,
        'item_request_history': item_request_history
    }

    return render(request, 'Staff/item_request.html', context)


def item_request_save(request):
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        quantity = request.POST.get('quantity')
        date_of_request = request.POST.get('date_of_request')
        department_id = request.POST.get('department_id')
        purpose_id = request.POST.get('purpose_id')
        remarks = request.POST.get('remarks')

        department = Department.objects.get(id=department_id)
        purpose = Purpose.objects.get(id=purpose_id)

        staff = Staff.objects.get(user=request.user.id)

        itemRequest = ItemRequest(
            staff_id=staff,
            item_name=item_name,
            quantity=quantity,
            date_of_request=date_of_request,
            department_id=department,
            purpose_id=purpose,
            remarks=remarks

        )
        itemRequest.save()
        messages.success(request, itemRequest.item_name + " " + "Successfully Added.")
    return redirect('item_request')

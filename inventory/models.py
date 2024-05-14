from datetime import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, ExpressionWrapper, Q
from django.db.models.functions import Now
from datetime import *
from django.utils import timezone



# Create your models here.

class CustomUser(AbstractUser):
    USER_CHOICES = (
        ('1', 'admin'),
        ('2', 'staff')
    )

    user_type = models.CharField(choices=USER_CHOICES, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')
    

class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Purpose(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    item_pic = models.ImageField(upload_to='media/item_pic')
    item_name = models.CharField(max_length=100)
    specification = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    issued_quantity = models.IntegerField(default=0, null=True, blank=True)
    received_quantity = models.IntegerField(default=0, null=True, blank=True)
    total_amount = models.FloatField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    date_of_purchase = models.DateField()
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    location_id = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    purpose_id = models.ForeignKey(Purpose, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    annual_leave = models.FloatField(default=18.0)
    sick_leave = models.FloatField(default=12.0)
    lieu_leave = models.FloatField(default=3.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def reset_leave_balances(self):
        # Set the leave balances to the original values
        self.annual_leave = 18.0
        self.sick_leave = 12.0
        self.lieu_leave = 3.0
        self.save()

    def __str__(self):
        return self.user.username
    

class StaffLeave(models.Model):
    LEAVE_TYPES = (
        ('ANNUAL_LEAVE', 'annual'),
        ('SICK_LEAVE', 'sick'),
        ('LIEU_LEAVE', 'lieu'),
    )
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    leave_type = models.CharField(max_length=100, choices=LEAVE_TYPES)
    reason = models.TextField()
    status = models.IntegerField(default=0)
    half_day = models.BooleanField(default = False)
    duration = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.staff_id.user.first_name} {self.staff_id.user.last_name} - {self.leave_type}"
    """ def save(self, *args, **kwargs):
        if self.to_date is None or self.to_date == '':
            self.to_date = self.from_date
            
            
            
            
        # Decrease leave duration and update leave balance based on category
        leave_balance = LeaveBalance.objects.get(staff_id=self.staff_id)
        if self.category == 'Annual leave':
            if self.calculate_leave_duration() > leave_balance.annual_leave_balance:
                raise ValueError('Insufficient Annual Leave Balance')
            leave_balance.annual_leave_balance -= self.calculate_leave_duration()
        elif self.category == 'Sick Leave':
            if self.calculate_leave_duration() > leave_balance.sick_leave_balance:
                raise ValueError('Insufficient Sick Leave Balance')
            leave_balance.sick_leave_balance -= self.calculate_leave_duration()
        elif self.category == 'Lieu Leave':
            if self.calculate_leave_duration() > leave_balance.lieu_leave_balance:
                raise ValueError('Insufficient Lieu Leave Balance')
            leave_balance.lieu_leave_balance -= self.calculate_leave_duration()
            
        leave_balance.save()

        super().save(*args, **kwargs)

    def calculate_leave_duration(self):
        # Perform calculations to determine the leave duration
        # You need to customize this method according to your requirements
        # For example, calculate the difference between from_date and to_date

        # Example implementation:
        # Assume from_date and to_date are in 'yyyy-mm-dd' format
        # Here, we calculate the number of days between the two dates

        from_date_obj = datetime.datetime.strptime(self.from_date, '%Y-%m-%d').date()
        to_date_obj = datetime.datetime.strptime(self.to_date, '%Y-%m-%d').date()
        duration = (to_date_obj - from_date_obj).days + 1  # Add 1 to include both from_date and to_date

        return duration """


class StaffFeedback(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.user.first_name + " " + self.staff_id.user.last_name


class ItemRequest(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    date_of_request = models.DateField()
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    purpose_id = models.ForeignKey(Purpose, on_delete=models.DO_NOTHING)
    remarks = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.user.first_name + " " + self.staff_id.user.last_name


class ExpiredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(valid_to__lt=Now()), output_field=BooleanField()))


class Medicine(models.Model):
    bill_no = models.IntegerField(default=1)
    medicine_name = models.CharField(max_length=100)
    drug_type = models.CharField(max_length=100, blank="True", null="True")
    drug_price = models.FloatField(max_length=100)
    quantity = models.IntegerField(default=1)
    quantity_in_strip = models.IntegerField(default=1, blank="True", null="True")
    receive_quantity = models.CharField(max_length=100)
    reorder_level = models.IntegerField(default='0', blank="True", null="True")
    manufacture = models.CharField(max_length=100, blank="True", null="True")
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    drug_strength = models.CharField(max_length=10, blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=False, null=True)
    location_id = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    remarks = models.CharField(max_length=100, blank="True", null="True")
    objects = ExpiredManager()

    def __str__(self):
        return str(self.medicine_name)
    
    
    @property
    def days_until_expiration(self):
        remaining_time = self.valid_to - timezone.now()
        return remaining_time.days
    #
    # @property
    # def get_remaining_days(self):
    #     difference = self.valid_to - self.valid_from
    #     return difference.days


class Dispense(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.SET_NULL, null=True, blank=False)
    dispense_quantity = models.PositiveIntegerField(default='1', blank=False, null=True)
    issued_to = models.CharField(max_length=300, null=True, blank=True)
    bill_no = models.CharField(max_length=300, null=True, blank=True)
    dispense_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.medicine.medicine_name


class StockOut(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    amount_received = models.IntegerField(default=0, null=True, blank=True)
    issued_to = models.CharField(max_length=50, null=True, blank=True)
    unit_price = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.item.item_name


class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    amount_received = models.IntegerField(default=0, null=True, blank=True)
    issued_to = models.CharField(max_length=50, null=True, blank=True)
    total_amount = models.FloatField(max_length=100, null=True, blank=True)

    def get_total(self):
        total = self.quantity * self.item.total_amount
        return int(total)

    def __str__(self):
        return self.item.item_name


import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medRoster.settings')
django.setup()

from django.contrib.auth import get_user_model
from roster.models import StaffProfile, ShiftTemplate, Roster, RosterAssignment, ClinicalRole, ShiftType, RosterStatus

User = get_user_model()

print("Starting to seed dummy data...")

# 1. Create Shift Templates
templates = [
    {"name": "Morning Shift", "start_time": "08:00:00", "end_time": "16:00:00", "duration_hours": 8.0, "shift_type": ShiftType.MORNING, "color": "#3B82F6"},
    {"name": "Evening Shift", "start_time": "16:00:00", "end_time": "00:00:00", "duration_hours": 8.0, "shift_type": ShiftType.EVENING, "color": "#F59E0B"},
    {"name": "Night Shift", "start_time": "00:00:00", "end_time": "08:00:00", "duration_hours": 8.0, "shift_type": ShiftType.NIGHT, "color": "#6366F1"},
]

shift_objs = []
for t in templates:
    obj, created = ShiftTemplate.objects.get_or_create(name=t['name'], defaults=t)
    shift_objs.append(obj)
    if created:
        print(f"Created shift template: {t['name']}")

# 2. Create Dummy Users & Staff Profiles
dummy_users = [
    {"email": "doctor.john@example.com", "name": "Dr. John Doe", "role": ClinicalRole.DOCTOR, "dept": "Emergency"},
    {"email": "nurse.jane@example.com", "name": "Nurse Jane Smith", "role": ClinicalRole.NURSE, "dept": "ICU"},
    {"email": "nurse.bob@example.com", "name": "Nurse Bob Wilson", "role": ClinicalRole.NURSE, "dept": "Emergency"},
    {"email": "tech.sarah@example.com", "name": "Sarah Connor", "role": ClinicalRole.SUPPORT_STAFF, "dept": "Radiology"},
]

staff_profiles = []
for u in dummy_users:
    username = u['email'].split('@')[0]
    user, created = User.objects.get_or_create(
        email=u['email'],
        defaults={"username": username, "full_name": u['name']}
    )
    if created:
        user.set_password("Password@123")
        user.save()
        print(f"Created user: {u['name']}")
    
    # Note: StaffProfile is auto-created by signal, just update it
    profile = user.staff_profile
    profile.role = u['role']
    profile.department = u['dept']
    profile.save()
    staff_profiles.append(profile)

# 3. Create a Roster for the current month
today = date.today()
start_date = today.replace(day=1)
# Calculate last day of month
next_month = start_date.replace(day=28) + timedelta(days=4)
end_date = next_month - timedelta(days=next_month.day)

roster, created = Roster.objects.get_or_create(
    name=f"Roster {start_date.strftime('%B %Y')}",
    start_date=start_date,
    end_date=end_date,
    defaults={"status": RosterStatus.PUBLISHED}
)

if created:
    print(f"Created roster: {roster.name}")
    # Assign random shifts for the first 14 days
    for i in range(14):
        current_date = start_date + timedelta(days=i)
        
        # Assign 2 random staff members each day to random shifts
        selected_staff = random.sample(staff_profiles, 2)
        for staff in selected_staff:
            shift_tmpl = random.choice(shift_objs)
            RosterAssignment.objects.create(
                roster=roster,
                staff=staff,
                shift=shift_tmpl,
                shift_date=current_date,
                start_time=shift_tmpl.start_time,
                end_time=shift_tmpl.end_time,
                duration_hours=shift_tmpl.duration_hours
            )
    print("Created dummy shift assignments!")
else:
    print("Roster already exists. Skipping shift generation.")

print("Dummy data seeding complete!")

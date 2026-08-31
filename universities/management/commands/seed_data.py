from django.core.management.base import BaseCommand
from universities.models import University, Department
from accounts.models import CustomUser, UniversityStaffProfile, EmployerProfile
from jobs.models import Job


class Command(BaseCommand):
    help = 'Seed initial data for the University Job Recruitment System'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Universities
        mit, _ = University.objects.get_or_create(
            name='MIT', defaults={'address': 'Cambridge, MA 02139, USA', 'website': 'https://www.mit.edu'}
        )
        stanford, _ = University.objects.get_or_create(
            name='Stanford University', defaults={'address': 'Stanford, CA 94305, USA', 'website': 'https://www.stanford.edu'}
        )

        # Departments
        cs_mit, _ = Department.objects.get_or_create(name='Computer Science', university=mit)
        eng_mit, _ = Department.objects.get_or_create(name='Engineering', university=mit)
        cs_stanford, _ = Department.objects.get_or_create(name='Computer Science', university=stanford)
        business, _ = Department.objects.get_or_create(name='Business', university=stanford)

        # Staff user for MIT
        if not CustomUser.objects.filter(email='staff@mit.edu').exists():
            staff = CustomUser.objects.create_user(
                email='staff@mit.edu', password='password123',
                first_name='John', last_name='Doe', role='university_staff'
            )
            UniversityStaffProfile.objects.create(user=staff, university=mit, employee_id='MIT001', position='HR Manager')

        # Employer user
        if not CustomUser.objects.filter(email='employer@techcorp.com').exists():
            employer = CustomUser.objects.create_user(
                email='employer@techcorp.com', password='password123',
                first_name='Jane', last_name='Smith', role='employer'
            )
            EmployerProfile.objects.create(user=employer, company_name='TechCorp Inc.', contact_phone='+1-555-0100')

            # Jobs
            Job.objects.get_or_create(
                title='Software Engineer Intern',
                employer=employer,
                defaults={
                    'university': mit, 'department': cs_mit,
                    'description': 'Work on cutting-edge software projects with our engineering team.',
                    'requirements': 'Python, JavaScript, Git. Currently enrolled in CS or related field.',
                    'location': 'Cambridge, MA', 'job_type': 'internship',
                    'salary_range': '$25-30/hr', 'is_approved': True, 'approval_status': 'approved',
                }
            )
            Job.objects.get_or_create(
                title='Full Stack Developer',
                employer=employer,
                defaults={
                    'university': stanford, 'department': cs_stanford,
                    'description': 'Join our team to build and scale web applications.',
                    'requirements': 'React, Node.js, PostgreSQL, 1+ years experience.',
                    'location': 'Palo Alto, CA', 'job_type': 'full_time',
                    'salary_range': '$80,000-$120,000/yr', 'is_approved': True, 'approval_status': 'approved',
                }
            )

        # Student user
        if not CustomUser.objects.filter(email='student@example.com').exists():
            from accounts.models import StudentProfile
            student = CustomUser.objects.create_user(
                email='student@example.com', password='password123',
                first_name='Alice', last_name='Johnson', role='student'
            )
            StudentProfile.objects.create(user=student, university=mit, department=cs_mit, graduation_year=2025)

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
        self.stdout.write('  Universities: MIT, Stanford')
        self.stdout.write('  Staff: staff@mit.edu / password123')
        self.stdout.write('  Employer: employer@techcorp.com / password123')
        self.stdout.write('  Student: student@example.com / password123')

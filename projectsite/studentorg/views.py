from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from typing import Any 
from django.db.models.query import QuerySet
from django.db.models import Q
from .models import Student
from collections import Counter
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from django.db import connection
from django.db.models.functions import TruncMonth
import calendar
import json
from collections import defaultdict

@method_decorator(login_required, name='dispatch')
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = Organization.objects.all()
        context['students'] = Student.objects.all()
        context['orgMember'] = OrgMember.objects.all()
        context['colleges'] = College.objects.all()
        context['programs'] = Program.objects.all()
        return context
    
# Organization URLs

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organizations'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                           Q(description__icontains=query))
        return qs


class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

# Organization member URLs

class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgMember'
    template_name = 'orgMem_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(student__firstname__icontains=query) |
                Q(student__lastname__icontains=query)  |
                Q(organization__name__icontains=query) |
                Q(organization__description__icontains=query)
            )
        return qs

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgMem_add.html'
    success_url = reverse_lazy('orgMem_list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgMem_edit.html'
    success_url = reverse_lazy('orgMem_list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgMem_del.html'
    success_url = reverse_lazy('orgMem_list')

# Student list
class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'Student_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(firstname__icontains=query) |
                Q(lastname__icontains=query)|
                Q(middlename__icontains=query) |
                Q(student_id__icontains=query) |
                Q(program__prog_name__icontains=query)
            )
        return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student_list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student_list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student_list')

# College list
    
class CollegeList(ListView):
    model = College
    context_object_name = 'colleges'
    template_name = 'college_list.html'
    paginate_by = 5

   
    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(college_name__icontains=query)
            )
        return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'colleg_add.html'
    success_url = reverse_lazy('college_list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college_list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college_list')

# Program URLs
class ProgramList(ListView):
    model = Program
    context_object_name = 'programs'
    template_name = 'program_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(college__college_name__icontains=query)|
                Q(prog_name__icontains=query)
            )
        return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program_list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program_list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program_list')


def chart_page(request):
    return render(request, 'chart.html')

def chart_data(request):
    data = {
        "ACS": 2, "SITE": 0, "Month Center": 2, "Air Industry": 1,
        "Consider Ability": 0, "Group Their": 2, "Should Realize": 0,
        "Go Name": 2, "Morning Week": 2, "Game Team": 1, "Resource Show": 0,
        "Response Foreign": 1, "Bachelor of Science in Computer Science": 1
    }
    return JsonResponse(data)

def scatter_chart_data(request):
    data = []

    colleges = College.objects.all()

    for college in colleges:
        # X: Number of organizations under this college
        org_count = Organization.objects.filter(college=college).count()

        # Y: Number of org members in those organizations
        member_count = OrgMember.objects.filter(organization__college=college).count()

        data.append({
            'x': org_count,
            'y': member_count,
            'label': college.college_name
        })

    return JsonResponse(data, safe=False)

def program_chart_data(request):
    data = {}

    programs = Program.objects.annotate(student_count=Count('student'))
    for prog in programs:
        data[prog.prog_name] = prog.student_count

    return JsonResponse(data)

def member_joined_by_month(request):
    data = (
        OrgMember.objects
        .annotate(month=TruncMonth("date_joined"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    labels = [entry["month"].strftime("%B") for entry in data]
    counts = [entry["count"] for entry in data]

    return JsonResponse({"labels": labels, "counts": counts})

def get_student_heatmap_data(request):
    # Aggregating student data by program and month
    student_data = Student.objects.annotate(month=TruncMonth('created_at')) \
                                  .values('program', 'month') \
                                  .annotate(student_count=Count('id')) \
                                  .order_by('program', 'month')

    # Organizing the data into a matrix format (program vs month)
    heatmap_data = defaultdict(lambda: defaultdict(int))
    for entry in student_data:
        program = entry['program']
        month = entry['month'].strftime('%Y-%m')  # Format as Year-Month
        student_count = entry['student_count']
        heatmap_data[program][month] = student_count

    # Convert to a list of lists (matrix)
    programs = Program.objects.all()
    months = sorted(set(entry['month'].strftime('%Y-%m') for entry in student_data))

    heatmap_matrix = []
    for program in programs:
        row = [heatmap_data[program.id].get(month, 0) for month in months]
        heatmap_matrix.append(row)

    return JsonResponse({
        'programs': [program.prog_name for program in programs],
        'months': months,
        'data': heatmap_matrix
    })
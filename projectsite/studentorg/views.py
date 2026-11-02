from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin  # <--- 1. Import this
from studentorg.models import Organization, Program, Student, College, OrgMember
from studentorg.forms import OrganizationForm, CollegeForm, StudentForm, ProgramForm, OrgMemberForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone

# ---------------------------------------------------------
# HOME / DASHBOARD
# ---------------------------------------------------------
class HomePageView(LoginRequiredMixin, ListView):  # <--- 2. Add LoginRequiredMixin here
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"
    login_url = '/accounts/login/'                  # <--- 3. Set login redirect path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_students"] = Student.objects.count()
        
        today = timezone.now().date()
        count = (
            OrgMember.objects.filter(date_joined__year=today.year)
            .values("student")
            .distinct()
            .count()
        )
        context["students_joined_this_year"] = count
        context["total_organizations"] = Organization.objects.count()
        context["total_programs"] = Program.objects.count()
        return context


# ---------------------------------------------------------
# ORGANIZATION VIEWS
# ---------------------------------------------------------
class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')
    login_url = '/accounts/login/'

class OrganizationList(LoginRequiredMixin, ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5
    login_url = '/accounts/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | 
                Q(description__icontains=q)
            )
        return queryset

class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')
    login_url = '/accounts/login/'

class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')
    login_url = '/accounts/login/'


# ---------------------------------------------------------
# COLLEGE VIEWS
# ---------------------------------------------------------
class CollegeDeleteView(LoginRequiredMixin, DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')
    login_url = '/accounts/login/'

class CollegeList(LoginRequiredMixin, ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college_list.html'
    paginate_by = 5
    login_url = '/accounts/login/'

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(college_name__icontains=query)
            )
        return qs

class CollegeCreateView(LoginRequiredMixin, CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_form.html'
    success_url = reverse_lazy('college-list')
    login_url = '/accounts/login/'

class CollegeUpdateView(LoginRequiredMixin, UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_form.html'
    success_url = reverse_lazy('college-list')
    login_url = '/accounts/login/'


# ---------------------------------------------------------
# STUDENT VIEWS
# ---------------------------------------------------------
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')
    login_url = '/accounts/login/'

class StudentList(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'
    paginate_by = 10
    login_url = '/accounts/login/'

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(student_id__icontains=query) |
                Q(firstname__icontains=query) |
                Q(lastname__icontains=query) |
                Q(middle_name__icontains=query)
            )
        return qs

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')
    login_url = '/accounts/login/'

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')
    login_url = '/accounts/login/'


# ---------------------------------------------------------
# PROGRAM VIEWS
# ---------------------------------------------------------
class ProgramDeleteView(LoginRequiredMixin, DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')
    login_url = '/accounts/login/'

class ProgramList(LoginRequiredMixin, ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'program_list.html'
    paginate_by = 5
    login_url = '/accounts/login/'

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(prog_name__icontains=query) |
                Q(college__college_name__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ["prog_name", "college__college_name"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "prog_name"

class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_form.html'
    success_url = reverse_lazy('program-list')
    login_url = '/accounts/login/'

class ProgramUpdateView(LoginRequiredMixin, UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_form.html'
    success_url = reverse_lazy('program-list')
    login_url = '/accounts/login/'


# ---------------------------------------------------------
# ORG MEMBER VIEWS
# ---------------------------------------------------------
class OrgMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = OrgMember
    template_name = 'orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')
    login_url = '/accounts/login/'

class OrgMemberList(LoginRequiredMixin, ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmember_list.html'
    paginate_by = 5
    login_url = '/accounts/login/'

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(student__lastname__icontains=query) |
                Q(student__firstname__icontains=query) |
                Q(organization__name__icontains=query)
            )
        return qs

    def get_ordering(self):
        allowed = ["student__lastname", "date_joined", "-date_joined"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "student__lastname"

class OrgMemberCreateView(LoginRequiredMixin, CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_form.html'
    success_url = reverse_lazy('orgmember-list')
    login_url = '/accounts/login/'

class OrgMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_form.html'
    success_url = reverse_lazy('orgmember-list')
    login_url = '/accounts/login/'
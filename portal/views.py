from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from authentication.models import CustomUser

# Create your views here.


class HomePage1(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'portal/homepage1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_statistics = Task.get_task_statistics(self)
        context['task_statistics'] = task_statistics
        tasks = Task.objects.filter(created_by=self.request.user.id).count()
        context["total"] = tasks
        return context


class HomePage(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'portal/homepage1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_statistics = Task.get_task_statistics(self)
        context['task_statistics'] = task_statistics
        emp = CustomUser.objects.filter(
            created_by=self.request.user.id).count()
        context["total"] = emp
        return context


class AssignedTask(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "portal/assigned_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(
            user=self.request.user)
        context["tasks"] = context["tasks"].exclude(assigned_to=None)
        return context


class UnAssignedTask(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "portal/unassigned_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(
            user=self.request.user)
        context["tasks"] = context["tasks"].filter(assigned_to=None)
        return context


class CompletedTask(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "portal/completed_tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'AD':
            context["tasks"] = context["tasks"].filter(
                admin=self.request.user)
            context["tasks"] = context["tasks"].filter(completed=True)
        else:
            context["tasks"] = context["tasks"].filter(
                Q(user=self.request.user) | Q(assigned_to=self.request.user))
            context["tasks"] = context["tasks"].filter(completed=True)
        return context


class PendingTask(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "portal/completed_tasks.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'AD':
            context["tasks"] = context["tasks"].filter(
                user=self.request.user)
            context["tasks"] = context["tasks"].filter(completed=False)
        else:
            context["tasks"] = context["tasks"].filter(
                Q(user=self.request.user) | Q(assigned_to=self.request.user))
            context["tasks"] = context["tasks"].filter(completed=False)
        return context


class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'AD':
            context["tasks"] = context["tasks"].filter(
                admin=self.request.user)
        else:
            context["tasks"] = context["tasks"].filter(
                Q(user=self.request.user) | Q(assigned_to=self.request.user))
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                task__contains=search_input)
            context['search_input'] = search_input
        role_filter = self.request.GET.get('role-filter')
        if role_filter:
            context["tasks"] = context["tasks"].filter(role=role_filter)
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'portal/taskdetail.html'
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['task', 'task_detail', 'deadline',
              'completed', 'assigned_to']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        adm = CustomUser.objects.get(pk=self.request.user.created_by)
        form.instance.user = self.request.user
        form.instance.admin = adm
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task', 'task_detail', 'deadline',
              'completed', 'assigned_to']
    success_url = reverse_lazy('tasklist')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role not in ['PM', 'AD']:
            form.fields.pop('task_detail')
            form.fields.pop('deadline')
            form.fields.pop('task')
            form.fields.pop('assigned_to')
        return form


class AssignedTaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task', 'task_detail', 'deadline',   'completed']
    success_url = reverse_lazy('assigned_task')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role != 'AD':
            form.fields.pop('task_detail')
            form.fields.pop('deadline')
            form.fields.pop('task')
        else:
            form.fields.pop('completed')
        return form


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasklist')


class AsssignedTaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('assigned_task')


class EmployeeList(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'employees'
    template_name = 'portal/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees"] = context["employees"].filter(
            created_by=self.request.user.id)
        return context


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = CustomUser
    context_object_name = 'user'
    success_url = reverse_lazy('home')
    template_name = 'portal/employee_confirm_delete.html'

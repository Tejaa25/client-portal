from .models import Task
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class AssignedTask(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "portal/assigned_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'PM':
            context["tasks"] = context["tasks"].filter(
                user=self.request.user)
            context["tasks"] = context["tasks"].exclude(assigned_to=None)
        else:
            context["tasks"] = context["tasks"].filter(
                user_id=self.request.user.created_by)
            context["tasks"] = context["tasks"].exclude(assigned_to=None)
        return context


class UnAssignedTask(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = "portal/unassigned_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'PM':
            context["tasks"] = context["tasks"].filter(
                user=self.request.user)
            context["tasks"] = context["tasks"].filter(assigned_to=None)
        else:
            context["tasks"] = context["tasks"].filter(
                user_id=self.request.user.created_by)
            context["tasks"] = context["tasks"].filter(assigned_to=None)
        return context


class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'PM':
            context["tasks"] = context["tasks"].filter(
                user=self.request.user)
        else:
            context["tasks"] = context["tasks"].filter(
                user_id=self.request.user.created_by)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                task__contains=search_input)
            context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'portal/taskdetail.html'
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['task', 'task_detail', 'deadline',
              'role', 'completed', 'assigned_to']
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task', 'task_detail', 'deadline',  'role', 'completed']
    success_url = reverse_lazy('tasklist')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role != 'PM':
            form.fields.pop('task_detail')
            form.fields.pop('deadline')
            form.fields.pop('role')
            form.fields.pop('task')
        else:
            form.fields.pop('completed')
        return form


class AssignedTaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task', 'task_detail', 'deadline',  'role', 'completed']
    success_url = reverse_lazy('assigned_task')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.role != 'PM':
            form.fields.pop('task_detail')
            form.fields.pop('deadline')
            form.fields.pop('role')
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

from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Note, Tag
from .serializers import NoteSerializer, TagSerializer


# API Views
class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с заметками (API)
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tags__name']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с тегами (API)
    """
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(notes__author=self.request.user).distinct()


# Web Views
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'
    paginate_by = 12

    def get_queryset(self):
        queryset = Note.objects.filter(author=self.request.user)

        # Поиск
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        # Фильтр по тегу
        tag_filter = self.request.GET.get('tag', '')
        if tag_filter:
            queryset = queryset.filter(tags__name__iexact=tag_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = Tag.objects.filter(notes__author=self.request.user).distinct()
        return context


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'notes/note_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Обработка тегов
        tags_input = self.request.POST.get('tags', '')
        tag_names = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]

        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            form.instance.tags.add(tag)

        messages.success(self.request, 'Заметка успешно создана!')
        return response

    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    template_name = 'notes/note_form.html'
    fields = ['title', 'content']

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Подготовка строки тегов для формы
        tags = self.object.tags.all()
        context['tags_string'] = ', '.join([tag.name for tag in tags])
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        # Обновление тегов
        tags_input = self.request.POST.get('tags', '')
        tag_names = [tag.strip().lower() for tag in tags_input.split(',') if tag.strip()]

        self.object.tags.clear()
        for tag_name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            self.object.tags.add(tag)

        messages.success(self.request, 'Заметка успешно обновлена!')
        return response

    def get_success_url(self):
        return reverse_lazy('note_detail', kwargs={'pk': self.object.pk})


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('note_list')

    def get_queryset(self):
        return Note.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Заметка успешно удалена!')
        return super().delete(request, *args, **kwargs)


def home(request):
    return render(request, 'home.html')

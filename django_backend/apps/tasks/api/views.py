from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.tasks.models import Task, TaskAssignment
from .serializers import TaskSerializer, CommentSerializer, TaskHistorySerializer
from .pagination import TasksPagination

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('created_by', 'parent_task').prefetch_related('assigned_to', 'tags')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TasksPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority', 'created_by']
    search_fields = ['title', 'description']

    def get_queryset(self):
        include_archived = self.request.query_params.get('include_archived')
        qs = Task.objects.active().select_related('created_by', 'parent_task').prefetch_related('assigned_to', 'tags')
        if include_archived == 'true':
            qs = Task.objects.all()  # incluye todo, archivadas también
        # filtros extra si quieres
        status = self.request.query_params.get('status')
        if status:
            qs = qs.by_status(status)
        priority = self.request.query_params.get('priority')
        if priority:
            qs = qs.by_priority(priority)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.search(search)
        return qs

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario autenticado como creador
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        # Asignar usuario que hace la actualización
        instance = serializer.save(updated_by=self.request.user)

    # POST /api/tasks/{id}/assign/
    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        task = self.get_object()
        users_ids = request.data.get("assigned_to", [])
        for user_id in users_ids:
            TaskAssignment.objects.create(
                task=task,
                user_id=user_id,
                assigned_by=request.user
            )
        return Response({"detail": "Users assigned successfully"})
    
    # POST and GET /api/tasks/{id}/comments/
    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        task = self.get_object()

        if request.method == "POST":
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, task=task)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # GET
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    # GET /api/tasks/{id}/history/
    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        task = self.get_object()
        history = task.history.all()
        serializer = TaskHistorySerializer(history, many=True) 
        return Response(serializer.data)
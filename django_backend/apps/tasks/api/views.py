from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from apps.tasks.models import Task, TaskAssignment
from .serializers import TaskSerializer, CommentSerializer, TaskHistorySerializer
from .pagination import TasksPagination
from apps.tasks.tasks import send_task_notification

class TaskViewSet(viewsets.ModelViewSet):
    """
    Task API ViewSet.

    Provides CRUD operations and additional actions for tasks.

    Endpoints:
    - list: GET /api/tasks/ - list tasks with filtering, search and pagination.
    - retrieve: GET /api/tasks/{id}/ — retrieve a single task
    - create: POST /api/tasks/ — create a new task (authenticated user is automatically the creator)
    - update: PUT /api/tasks/{id}/ — update a task
    - partial_update: PATCH /api/tasks/{id}/ — partial update a task
    - destroy: DELETE /api/tasks/{id}/ — delete a task

    Custom Actions:
    - assign: POST /api/tasks/{id}/assign/ — assign users to a task
    - comments: GET/POST /api/tasks/{id}/comments/ — retrieve or create comments for a task
    - history: GET /api/tasks/{id}/history/ — retrieve task change history

    Features:
    - Filters tasks by status, priority, and created_by
    - Search tasks by title or description
    - Automatically sends notifications on task creation, update, and deletion
    - Supports pagination

    Permissions:
    - Only authenticated users can access any of the endpoints

    Query Parameters:
    - include_archived (optional): 'true' to include archived tasks in the list
    - status (optional): filter tasks by status
    - priority (optional): filter tasks by priority
    - search (optional): search tasks by title or description
    """
    # select_related: optimization of queries, Django brings in a single query all the tasks created by the same user
    # 2 queries: 1 query for main object and 1 query for related objects
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
            qs = Task.objects.all()

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
        # Assign user as creator
        task = serializer.save(created_by=self.request.user)
        # exec celery task
        send_task_notification.delay(task.id, "created")

    def perform_update(self, serializer):
        # Assign user who performs update
        instance = serializer.save(updated_by=self.request.user)
        # exec celery task
        send_task_notification.delay(instance.id, "updated")

    # override method to peroform celery task
    def perform_destroy(self, instance):
        task_id = instance.id
        instance.delete()
        # exec celery task
        send_task_notification.delay(task_id, "deleted")


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
from rest_framework import generics, permissions

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        status = self.request.GET.get('status', None)
        if self.request.user.role == 'admin':
            if not status:
                return Transaction.objects.all()
            return Transaction.objects.filter(status=status).all()
        else:
            return Transaction.objects.filter(user=self.request.user).all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Transaction.objects.all()
        else:
            return Transaction.objects.filter(user=self.request.user)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Proposal
from .serializers import ProposalSerializer

class ProposalCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'entrepreneur':
            return Response(
                {"error": "Only entrepreneurs can create proposals!"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProposalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(entrepreneur=request.user)
            return Response(
                {"message": "Proposal created successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProposalListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        proposals = Proposal.objects.all().order_by('-created_at')
        serializer = ProposalSerializer(proposals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProposalDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            proposal = Proposal.objects.get(pk=pk)
        except Proposal.DoesNotExist:
            return Response(
                {"error": "Proposal not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProposalSerializer(proposal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            proposal = Proposal.objects.get(pk=pk)
        except Proposal.DoesNotExist:
            return Response(
                {"error": "Proposal not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        if proposal.entrepreneur != request.user:
            return Response(
                {"error": "You can only edit your own proposals!"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProposalSerializer(proposal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Proposal updated successfully!", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            proposal = Proposal.objects.get(pk=pk)
        except Proposal.DoesNotExist:
            return Response(
                {"error": "Proposal not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        if proposal.entrepreneur != request.user:
            return Response(
                {"error": "You can only delete your own proposals!"},
                status=status.HTTP_403_FORBIDDEN
            )
        proposal.delete()
        return Response(
            {"message": "Proposal deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Transaction, Wallet, Account
from .serializers import TransactionSerializer, AccountSerializer

from django.db.models import Q


class TransactionList(APIView):

    def get(self, request, format=None):
        if request.GET.get('all'):
            transactions = Transaction.objects.filter(user_id=request.user.id, transaction_date__month=request.GET.get('month')).order_by('-transaction_date')
        else:
            transactions = Transaction.objects.filter(user_id=request.user.id).order_by('-transaction_date')[:5]
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data.update({'user': request.user.id})
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        transactionId = request.data.pop('transactionId')
        if 'amount' in request.data.keys():
            request.data['amount'] = int(request.data['amount'])
        transaction = Transaction.objects.get(pk=transactionId)
        serializer = TransactionSerializer(transaction, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        try:
            transaction = Transaction.objects.get(pk=request.data.get('transactionID'))
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountList(APIView):

    def get(self, request, format=None):
        wallet = Wallet.objects.filter(user_id=request.user.id)[0]
        if request.GET.get('cash') == 'true':
            accounts = Account.objects.filter(wallet=wallet, category='Cash')[:5]
        elif request.GET.get('cash') == 'false':
            accounts = Account.objects.filter(wallet=wallet).exclude(category='Cash')[:5]
        elif request.GET.get('getEach'):
            accounts = Account.objects.filter(wallet=wallet)[:5]
        elif request.GET.get('getAll'):
            accounts = Account.objects.filter(wallet=wallet)

        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        wallet = Wallet.objects.filter(user_id=request.user.id)[0]
        request.data.update({'wallet': wallet.id})
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            account = Account.objects.get(pk=request.data.get('accountId'))
            account.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        accountId = request.data.pop('accountId')
        account = Account.objects.get(pk=accountId)
        serializer = AccountSerializer(account, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountCategoryChoicesList(APIView):

    def get(self, request):
        choices = Account.Categories.choices

        return Response(choices)


class ExpenseAccountsMonthlyData(APIView):

    def get(self, request):
        wallet = Wallet.objects.get(user_id=request.user.id)
        accounts = (Account.objects.filter(wallet=wallet)
                    .exclude(Q(category=Account.Categories.Cash.value) | Q(category=Account.Categories.Salary.value)))
        accounts_data = [account.get_monthly_debit_credit_history(credit=False, month=request.GET.get('month'))
                         for account in accounts]
        return Response(accounts_data)

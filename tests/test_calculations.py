from app.calculation import add, BankAccount, Insufficient_Funds
import pytest

# Most simple way for basic testing purpose: hard code them
# def test_add():
#     print("start testing add function")
#     assert add(5,3) == 8

# Advanced ways for testing
@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5), (7,1,8), (4,5,9), (12,1,13)
])
def test_add(num1, num2, expected):
    print("start testing add function")
    assert add(num1,num2) == expected

# Initialize the amount of bank default as 0
@pytest.fixture()
def zero_bank_account():
    print("creating my empty account")
    return BankAccount()

def test_zero_bank_account(zero_bank_account):
    print("testing my empty bank")
    assert zero_bank_account.balance == 0


# Initialize the amount of bank as 50
@pytest.fixture()
def bank_account():
    return BankAccount(50)

def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


# Implement parametrize function
@pytest.mark.parametrize("deposit, withdraw, expected", [
    (200,100,100), (50,10,40), (1200,100,1100)
])
def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(Insufficient_Funds):
        bank_account.withdraw(200)







    
    
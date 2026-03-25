import pytest

from mycashflow.models.transaction import Transaction
from mycashflow.models.entry import Entry


transaction_data1 = {
    "id": 1,
    "group": "Test_group_name_transaction_1",
    "entries": [],
    "parent_id": None
}

transaction_data2 = {
    "id": 2,
    "group": "Test_group_name_transaction_2",
    "entries": [],
    "parent_id": None
}

entry_data1 = {
    "id": 3,
    "account": "Test_account1",
    "amount": 600,
}

entry_data2 = {
    "id": 4,
    "account": "Test_account2",
    "amount": 500,
}

entry_data3 = {
    "id": 5,
    "account": "Test_account3",
    "amount": 500,
}

entry_data4 = {
    "id": 6,
    "account": "Test_account4",
    "amount": 500,
}

transaction_data3 = {
    "id": 7,
    "group": "Test_group_name_transaction_3",
    "entries": [],
    "parent_id": None
}

entry_data5 = {
    "id": 8,
    "account": "Test_account5",
    "amount": 10000,
}

entry_data6 = {
    "id": 9,
    "account": "Test_account6",
    "amount": 5675,
}



def test_transaction():

    transaction: Transaction = Transaction(**transaction_data1)

    # f"{self.id} - {self.group}: {self.total}"
    assert str(transaction) == "000001 - Test_group_name_transaction_2: 0"


def test_transaction_with_entries():

    transaction1: Transaction = Transaction(**transaction_data1)
    transaction1.add_entry(**entry_data1)
    transaction1.add_entry(**entry_data2)

    transaction2 = Transaction(**transaction_data2)
    transaction2.add_entry(**entry_data3)
    transaction2.add_entry(**entry_data4)

    transaction1.children.append(transaction2)

    transaction3: Transaction = Transaction(**transaction_data3)
    transaction3.add_entry(**entry_data5)
    transaction3.add_entry(**entry_data6)

    transaction2.children.append(transaction3)

    transaction4: Transaction = Transaction(**transaction_data3)
    transaction4.add_entry(**entry_data5)
    transaction4.add_entry(**entry_data6)

    transaction3.children.append(transaction4)



    assert transaction1._get_max_deep_tree() == 4
    assert transaction1.out_tree() == ""

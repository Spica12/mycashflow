import pytest

from mycashflow.models.entry import Entry




def test_entry():

    entry: Entry = Entry(id=2, parent_id=1, account="Test_account", amount=600)

    # f"{self.id} - {self.account}: {self.amount}"
    assert str(entry) == "000002 - Test_account: 600"

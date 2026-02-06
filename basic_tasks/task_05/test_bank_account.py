import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def test_initial_balance(self):
        acc = BankAccount(100)
        self.assertEqual(acc.get_balance(), 100)

    def test_deposit(self):
        acc = BankAccount()
        acc.deposit(50)
        self.assertEqual(acc.get_balance(), 50)

    def test_withdraw(self):
        acc = BankAccount(100)
        acc.withdraw(30)
        self.assertEqual(acc.get_balance(), 70)

    def test_withdraw_too_much(self):
        acc = BankAccount(50)
        with self.assertRaises(ValueError):
            acc.withdraw(100)

    def test_negative_deposit(self):
        acc = BankAccount()
        with self.assertRaises(ValueError):
            acc.deposit(-10)

    def test_negative_withdraw(self):
        acc = BankAccount()
        with self.assertRaises(ValueError):
            acc.withdraw(-5)


if __name__ == "__main__":
    unittest.main()

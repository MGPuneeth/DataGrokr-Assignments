import unittest

from bank_account import BankAccount, SavingsAccount


class BankAccountTests(unittest.TestCase):
    def test_deposit_withdraw_and_transfer(self):
        sender = BankAccount("BA1", "Asha", 100)
        recipient = BankAccount("BA2", "Bala", 25)

        sender.deposit(50)
        sender.withdraw(20)
        sender.transfer_to(recipient, 30)

        self.assertEqual(sender.current_balance, 100)
        self.assertEqual(recipient.current_balance, 55)

    def test_rejects_withdrawal_above_balance(self):
        account = BankAccount("BA1", "Asha", 100)
        with self.assertRaisesRegex(ValueError, "Insufficient funds"):
            account.withdraw(101)

    def test_savings_interest(self):
        account = SavingsAccount("BA1", "Asha", 100, interest_rate="0.05")
        account.apply_interest()
        self.assertEqual(account.current_balance, 105)


if __name__ == "__main__":
    unittest.main()

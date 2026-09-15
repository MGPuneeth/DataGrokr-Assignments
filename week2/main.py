"""Small demonstration of the bank account OOP model."""

from bank_account import BankAccount, SavingsAccount


def main() -> None:
    savings = SavingsAccount("BA2001", "Neha Verma", "1000.00", interest_rate="0.05")
    checking = BankAccount("BA2002", "Kabir Das", "500.00")

    savings.deposit("250.00")
    savings.transfer_to(checking, "100.00")
    savings.apply_interest()

    print(savings)
    print(checking)


if __name__ == "__main__":
    main()

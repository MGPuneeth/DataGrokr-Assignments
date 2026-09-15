"""Object-oriented bank account representations."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation


def _money(value: Decimal | float | int | str) -> Decimal:
    """Convert a value to a two-decimal, non-negative monetary amount."""
    try:
        amount = Decimal(str(value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Amount must be a valid number.") from exc
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    return amount


@dataclass
class BankAccount:
    """A bank account that supports deposits, withdrawals, and transfers."""

    account_number: str
    owner: str
    balance: Decimal | float | int | str = Decimal("0.00")
    _balance: Decimal = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.account_number.strip():
            raise ValueError("Account number is required.")
        if not self.owner.strip():
            raise ValueError("Account owner is required.")
        self._balance = _money(self.balance)

    @property
    def current_balance(self) -> Decimal:
        return self._balance

    def deposit(self, amount: Decimal | float | int | str) -> Decimal:
        amount = _money(amount)
        if amount == 0:
            raise ValueError("Deposit must be greater than zero.")
        self._balance += amount
        return self._balance

    def withdraw(self, amount: Decimal | float | int | str) -> Decimal:
        amount = _money(amount)
        if amount == 0:
            raise ValueError("Withdrawal must be greater than zero.")
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount
        return self._balance

    def transfer_to(
        self, recipient: "BankAccount", amount: Decimal | float | int | str
    ) -> None:
        if recipient is self:
            raise ValueError("An account cannot transfer money to itself.")
        self.withdraw(amount)
        recipient.deposit(amount)

    def __str__(self) -> str:
        return (
            f"{self.owner} ({self.account_number}) - "
            f"balance: ${self.current_balance:.2f}"
        )


@dataclass
class SavingsAccount(BankAccount):
    """A bank account that can apply interest to its balance."""

    interest_rate: Decimal | float | int | str = Decimal("0.02")

    def apply_interest(self) -> Decimal:
        rate = Decimal(str(self.interest_rate))
        if rate < 0:
            raise ValueError("Interest rate cannot be negative.")
        self._balance = (self._balance * (Decimal("1") + rate)).quantize(
            Decimal("0.01")
        )
        return self._balance

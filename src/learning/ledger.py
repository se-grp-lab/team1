"""Differential Privacy (Epsilon, Delta) Budget Ledger."""
class PrivacyLedger:
    def __init__(self, total_epsilon: float = 10.0, total_delta: float = 1e-5):
        self.total_epsilon = total_epsilon
        self.total_delta = total_delta
        self.consumed_epsilon = 0.0

    def record_round(self, round_eps: float) -> bool:
        if self.consumed_epsilon + round_eps > self.total_epsilon:
            return False
        self.consumed_epsilon += round_eps
        return True

    @property
    def remaining_epsilon(self) -> float:
        return max(0.0, self.total_epsilon - self.consumed_epsilon)

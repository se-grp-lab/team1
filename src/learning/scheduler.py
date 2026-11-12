"""Adaptive Learning Rate Decay for On-Device SGD Adaptation."""
class LearningRateScheduler:
    def __init__(self, initial_lr: float = 0.05, decay_rate: float = 0.95):
        self.initial_lr = initial_lr
        self.decay_rate = decay_rate
        self.step_count = 0

    def get_lr(self) -> float:
        return self.initial_lr * (self.decay_rate ** self.step_count)

    def step(self):
        self.step_count += 1

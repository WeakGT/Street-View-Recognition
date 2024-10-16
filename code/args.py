from dataclasses import dataclass

@dataclass
class Args:
    lr: float = 0.00005
    val_ratio: float = 0.2
    epochs: int = 100
    batch_size: int = 32
    save_model: bool = True
    start_from_last: bool = False


args = Args()

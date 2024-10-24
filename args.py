from dataclasses import dataclass

@dataclass
class Args:
    lr: float = 0.0005
    val_ratio: float = 0.2
    epochs: int = 200
    batch_size: int = 4
    save_model: bool = True
    start_from_last: bool = False
    eval_mode: bool = False


args = Args()

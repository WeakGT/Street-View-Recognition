from dataclasses import dataclass


@dataclass
class Args:
    """ 

    Arguments meaning

    lr: learning rate
    val_ratio: ratio to split data into train and validation
    epochs: total rounds to run the training
    batch_size: number of samples in each batch 
    start_from_last: whether to start training from the last checkpoint
    load_data_workers: number of workers to load data
    checkpoint_step: steps of ecpochs to save checkpoint
    alpha: weight between classification loss and regression loss
    random_seed: random seed for reproducibility
    label_smoothing: label smoothing factor for cross entropy loss
    """

    lr: float = 0.0001
    val_ratio: float = 0.2
    epochs: int = 50
    batch_size: int = 32
    start_from_last: bool = False
    load_data_workers: int = 8
    checkpoint_step: int = 20
    alpha: float = 0.1
    random_seed: int = 42
    label_smoothing: float = 0.1

args = Args()

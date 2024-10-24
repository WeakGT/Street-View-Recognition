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
    """

    lr: float = 0.001
    val_ratio: float = 0.2
    epochs: int = 100
    batch_size: int = 8
    start_from_last: bool = False
    load_data_workers: int = 6
    checkpoint_step: int = 10
    alpha: float = 0.1
    random_seed: int = 42

args = Args()

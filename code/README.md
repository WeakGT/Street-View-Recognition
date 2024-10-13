## Building env for training
1. Create a virtual environment
2. `pip install -r requirements.txt`

## Code Review
- `main.py`: Entry point and training loop
- `args.py`: Tunign hyperparameter
- `model.py`: Define model architecture
- `stack_image.py`: Handle reading image from folder and stack them

## Interpret Training Result
After training, the record will be placed at runs/ folder.
- Run `tensorboard --logdir=runs`
- See the result in localhost
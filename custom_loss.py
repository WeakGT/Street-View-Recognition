import numpy as np
import torch
import torch.nn as nn
import math

# Define the custom loss function
class CustomLoss(nn.Module):
    def __init__(self):
        super(CustomLoss, self).__init__()
        self.mse_loss = nn.MSELoss()
        self.cross_entropy_loss = nn.CrossEntropyLoss()

    def forward(self, predictions, targets):
        # Ensure predictions and targets are torch tensors
        predictions = torch.tensor(predictions, dtype=torch.float32) if not isinstance(predictions, torch.Tensor) else predictions
        targets = torch.tensor(targets, dtype=torch.float32) if not isinstance(targets, torch.Tensor) else targets
        
        # Extract predicted coordinates and class predictions
        pred_coords = predictions[:, :2]  # First two dimensions for coordinates
        pred_classes = predictions[:, 2:]  # Remaining dimensions for class predictions
        # print(type(pred_classes))
        total_loss = 0.0
        # Calculate the loss for each prediction
        for pred, target, pred_class in zip(pred_coords, targets, pred_classes):
            target_x, target_y = target[0].item(), target[1].item()
            # print(target_x, target_y)
            
            # Determine the target class based on the coordinate ranges
            # Calculate which class the target belongs to
            class_x = math.floor((target_x - 22) / 0.25)  # Map target_x to class index
            class_y = math.floor((target_y - 120) / 0.25)  # Map target_y to class index
            target_class = class_x * 8 + class_y 

            
            # print(pred_class.shape)
            # print(type(pred_class))

            # Check if the predicted class matches the target class
            predicted_class = torch.argmax(pred_class, dim=0)  # Select the class with the highest probability
            
            # print(pred_class_probs.shape)
            # print(pred_class_probs)
            
            if predicted_class == target_class:
                # Use MSE loss if the class prediction is correct
                total_loss += self.mse_loss(pred, target)
            else:
                # Use Cross Entropy loss if the class prediction is incorrect
                # Create a dummy target for Cross Entropy
                
                target_class_tensor = torch.zeros(112)
                target_class_tensor[target_class] = 1
                
                # print(target_class_tensor)
                total_loss += self.cross_entropy_loss(pred_class, target_class_tensor)

        return total_loss / len(predictions) if len(predictions) > 0 else total_loss

# Example of usage
# custom_loss = CustomLoss()
# loss_value = custom_loss(predictions, targets)

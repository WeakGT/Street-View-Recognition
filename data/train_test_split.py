import os
import pandas as pd
from sklearn.model_selection import train_test_split
import shutil

def prepare_image_dataset(
    csv_path, 
    image_folder, 
    output_base_dir, 
    val_size=0.2, 
    random_state=42
):
    """
    Prepare image dataset by splitting into train and val sets
    
    Parameters:
    -----------
    csv_path : str
        Path to input CSV file containing image metadata
    image_folder : str
        Source folder containing all images
    output_base_dir : str
        Base directory to create train/val splits
    val_size : float, optional (default=0.2)
        Proportion of dataset to include in val split
    random_state : int, optional (default=42)
        Controls the shuffling applied to the data before splitting
    
    Returns:
    --------
    tuple: (train_df, val_df)
    """
    # Read input CSV
    df = pd.read_csv(csv_path)
    
    # Ensure required columns exist
    required_columns = ['image']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"CSV must contain a '{col}' column")
    
    # Split into train and val DataFrames
    train_df, val_df = train_test_split(
        df, 
        test_size=val_size, 
        random_state=random_state
    )
    
    # Create output directories
    os.makedirs(os.path.join(output_base_dir, 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_base_dir, 'val'), exist_ok=True)
    
    # Copy files to respective directories
    def copy_files(split_df, split_type):
        copied_count = 0
        for _, row in split_df.iterrows():
            filename = row['image']
            src_path = os.path.join(image_folder, filename)
            dst_path = os.path.join(output_base_dir, split_type, filename)
            
            # Check if source file exists
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                copied_count += 1
            else:
                print(f"Warning: File {filename} not found in source folder")
        
        print(f"{split_type.capitalize()} set: {copied_count} files copied")
    
    # Copy train and val files
    copy_files(train_df, 'train')
    copy_files(val_df, 'val')
    
    # Save train and val CSV files
    train_csv_path = os.path.join(output_base_dir, 'train.csv')
    val_csv_path = os.path.join(output_base_dir, 'val.csv')
    
    train_df.to_csv(train_csv_path, index=False)
    val_df.to_csv(val_csv_path, index=False)
    
    # Print some statistics
    print(f"\nTotal files: {len(df)}")
    print(f"Train set: {len(train_df)} files")
    print(f"Val set: {len(val_df)} files")
    print(f"Train CSV saved to: {train_csv_path}")
    print(f"Val CSV saved to: {val_csv_path}")
    
    return train_df, val_df

# Example usage
if __name__ == "__main__":
    csv_path = './256x256_global/picture_coords.csv'
    image_folder = './256x256_global/'
    output_base_dir = './processed/'
    
    # Additional optional parameters
    train_df, val_df = prepare_image_dataset(
        csv_path, 
        image_folder, 
        output_base_dir, 
        val_size=0.2,  # 20% for val set
        random_state=42
    )
    
    # Optional: verify the generated CSVs
    print("\nTrain CSV Preview:")
    print(train_df.head())
    print("\nVal CSV Preview:")
    print(val_df.head())
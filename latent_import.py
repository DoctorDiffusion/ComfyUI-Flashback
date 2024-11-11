import os
import torch
import time

class LatentImport:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.temp_dir = os.path.join(self.script_dir, "temp")
        self.last_loaded = None
        self.last_check_time = 0
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger": ("INT", {"default": 0, "min": 0, "max": 99999999}),
            }
        }
    
    RETURN_TYPES = ("LATENT",)
    OUTPUT_TOOLTIPS = ("The loaded latent.",)
    FUNCTION = "import_latent"
    CATEGORY = "Flashback"
    DESCRIPTION = "Loads one of the two most recent latent tensors, alternating between them."

    def import_latent(self, trigger):
        current_time = time.time()
        
        # Ensure temp directory exists
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # List all .pt files in the 'temp' directory
        try:
            files = [f for f in os.listdir(self.temp_dir) if f.endswith(".pt")]
        except Exception as e:
            print(f"Error accessing directory {self.temp_dir}: {e}")
            return ({"samples": torch.zeros((1, 4, 8, 8)), "batch_size": 1},)

        if not files:
            print(f"No latent tensor files found in {self.temp_dir}")
            return ({"samples": torch.zeros((1, 4, 8, 8)), "batch_size": 1},)

        # Sort files by modification time (newest first)
        files = sorted(
            files,
            key=lambda f: os.path.getmtime(os.path.join(self.temp_dir, f)),
            reverse=True
        )
        
        # Keep only the two most recent files
        files = files[:2]
        
        # If we have two files, alternate between them
        if len(files) >= 2:
            # Choose the file that wasn't loaded last time
            selected_file = files[0] if self.last_loaded != files[0] else files[1]
        else:
            # If we only have one file, use it
            selected_file = files[0]
        
        try:
            file_path = os.path.join(self.temp_dir, selected_file)
            latent = torch.load(file_path)
            print(f"Loading latent tensor from: {file_path}")
            
            # Update the last loaded file
            self.last_loaded = selected_file
            self.last_check_time = current_time
            
            return (latent,)
            
        except Exception as e:
            print(f"Error loading latent tensor from {file_path}: {e}")
            return ({"samples": torch.zeros((1, 4, 8, 8)), "batch_size": 1},)


# Register the node class and display name mappings for LatentImport
NODE_CLASS_MAPPINGS = {
    "LatentImport": LatentImport,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentImport": "Latent Import",
}

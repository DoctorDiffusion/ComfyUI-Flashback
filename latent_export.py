import os
import torch
import time

class LatentExport:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.temp_dir = os.path.join(self.script_dir, "temp")
        self.file_name = "latest_latent.pt"
        
        # Create temp directory if it doesn't exist
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT", {"tooltip": "The latent tensor to export."}),
            }
        }

    RETURN_TYPES = ("LATENT",)
    OUTPUT_TOOLTIPS = ("The saved latent.",)
    FUNCTION = "export_latent"
    CATEGORY = "Flashback"
    DESCRIPTION = "Saves the latent tensor to a file in the 'temp' directory."

    def export_latent(self, latent):
        try:
            # Define file paths
            current_file = os.path.join(self.temp_dir, self.file_name)
            backup_file = os.path.join(self.temp_dir, "previous_latent.pt")
            
            # If current file exists, move it to backup
            if os.path.exists(current_file):
                # Remove old backup if it exists
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                # Move current to backup
                os.rename(current_file, backup_file)
            
            # Save new latent
            torch.save(latent, current_file)
            print(f"Latent tensor saved to {current_file}")
            
            return (latent,)
            
        except Exception as e:
            print(f"Error saving latent tensor: {e}")
            return (latent,)  # Return original latent even if save fails
# Register the node class and display name mappings for LatentExport
NODE_CLASS_MAPPINGS = {
    "LatentExport": LatentExport,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentExport": "Latent Export",
}

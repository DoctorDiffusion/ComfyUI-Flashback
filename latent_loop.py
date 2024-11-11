import torch

class LatentLoop:
    def __init__(self):
        # Track whether it's the first pass or not
        self.first_pass = True

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent1": ("LATENT",),
                "latent2": ("LATENT",),
            },
        }

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "process_latents"
    CATEGORY = "Flashback"  # Suite/category name

    def process_latents(self, latent1, latent2):
        # Select the latent based on the first_pass flag
        output_latent = latent1 if self.first_pass else latent2
        # Toggle first_pass for the next call
        self.first_pass = not self.first_pass

        return (output_latent,)

# Node mappings for registration
NODE_CLASS_MAPPINGS = {
    "LatentLoop": LatentLoop
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentLoop": "Latent Loop"
}

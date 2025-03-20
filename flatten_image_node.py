import torch

class FlattenImage:
    """
    A simple ComfyUI node that flattens multiple image layers into a single image.
    Simulates Photoshop's flatten image functionality.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  # This will be a batch of images to be flattened
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "flatten_layers"
    CATEGORY = "PS Operations"

    def flatten_layers(self, images):
        # If only one image or no images, return as is
        if images.shape[0] <= 1:
            return (images,)
        
        # Start with the first image
        flattened = images[0:1].clone()
        
        # Composite the rest of the images on top
        for i in range(1, images.shape[0]):
            current_layer = images[i:i+1]
            flattened = current_layer  # Simply replace with the top layer
        
        return (flattened,)


# Node registration function for ComfyUI
NODE_CLASS_MAPPINGS = {
    "FlattenImage": FlattenImage,
}

# Optional: provide a display name for the node
NODE_DISPLAY_NAME_MAPPINGS = {
    "FlattenImage": "Flatten Image",
}
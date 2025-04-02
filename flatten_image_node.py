import torch

class FlattenImage:
    """
    A ComfyUI node that flattens image layers and properly converts 
    transparent areas to white background, similar to Photoshop's flatten image.
    Works with both single images and sequences (movies).
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),  
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "flatten_layers"
    CATEGORY = "PS Operations"

    def flatten_layers(self, images):
        # Get the dimensions of the input
        batch_size, height, width = images.shape[0], images.shape[1], images.shape[2]
        
        # Check if we're dealing with RGBA (4 channels) or just RGB (3 channels)
        if len(images.shape) == 4 and images.shape[3] == 4:
            # RGBA case - handle the alpha channel
            
            # Create white background
            white_bg = torch.ones((batch_size, height, width, 3), device=images.device)
            
            # Extract RGB and alpha for all images in the batch
            rgb = images[:, :, :, 0:3]
            alpha = images[:, :, :, 3:4]
            
            # Expand alpha to match RGB dimensions
            alpha_expanded = alpha.expand(-1, -1, -1, 3)
            
            # Apply alpha compositing formula to all images in the batch
            result = rgb * alpha_expanded + white_bg * (1.0 - alpha_expanded)
            
            return (result,)
        else:
            # RGB case - no alpha channel to handle
            # Just return all images as they are
            return (images,)


NODE_CLASS_MAPPINGS = {
    "FlattenImage": FlattenImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FlattenImage": "PS Flatten Image",
}
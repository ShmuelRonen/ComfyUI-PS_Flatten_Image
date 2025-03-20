import torch

class FlattenImage:
    """
    A ComfyUI node that flattens image layers and properly converts 
    transparent areas to white background, similar to Photoshop's flatten image.
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
        batch_size, height, width = images.shape[0], images.shape[1], images.shape[2]
        
        white_bg = torch.ones((1, height, width, 3), device=images.device)
              
        if len(images.shape) == 4:
            channels = images.shape[3]
        else:

            channels = 3
        
        if channels == 4:
 
            top_layer = images[-1:].clone()
            
            rgb = top_layer[:, :, :, 0:3]
            alpha = top_layer[:, :, :, 3:4]
            
            alpha_expanded = alpha.expand(-1, -1, -1, 3)
            
            result = rgb * alpha_expanded + white_bg * (1.0 - alpha_expanded)
            
            return (result,)
        else:
            return (images[-1:],)


NODE_CLASS_MAPPINGS = {
    "FlattenImage": FlattenImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FlattenImage": "PS Flatten Image",
}
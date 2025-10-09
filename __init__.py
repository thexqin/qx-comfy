from google import genai
from PIL import Image
import torch
import numpy as np

class qxNode:
    
    CATEGORY = 'qxToolbox'
    
    @classmethod    
    def INPUT_TYPES(self):
        instruction = '''Generate a detailed, continuous prompt for stable diffusion to describe this image. The prompt should include the following components seamlessly integrated:
1. Subject/Scene: Start with the main focus of the image.
2. Additional Elements: Include any secondary details or background elements that complement the main subject.
3. Artistic Style/Effect: Describe the visual style or effect desired for the image.
4. Color Palette/Lighting: Specify the colors and lighting to set the mood of the image.
5. Specific Details: Add any intricate details or specific visual features that should be emphasized.
Output Format:
Ensure the output is provided using the following structure:
A [Subject/Scene] in a [Artistic Style/Effect] where [Additional Elements] are present, all depicted with [Color Palette/Lighting] and featuring [Specific Details].
Example Output:
A medieval castle on a hill during a thunderstorm in a gothic, dark fantasy style where dense, dark forests surround the castle, and lightning strikes in the distance, illuminating a river winding through the valley below, all depicted with a muted, dark color palette with flashes of bright white and blue from the lightning, and featuring crumbling walls with overgrown ivy, a slightly open drawbridge, and a dim, flickering light visible inside the castle.
'''
        return {
            'required':  {
                'api_key': ('STRING', {'default': 'YOUR_API_KEY_HERE'}),
                'IMAGE': ('IMAGE',),
                'prompt': ('STRING', {'multiline': True, 'default': instruction}),
            }
        }
        
    RETURN_TYPES = ('STRING',)
    FUNCTION = 'fetch_gemma'
    
    def tensor_to_pil(self, image_tensor):
        # This standard ComfyUI code converts the float tensor (0-1) to an
        # 8-bit integer numpy array (0-255) and then to a PIL Image.
        i = 255. * image_tensor.cpu().numpy().squeeze()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        return img
    
    def fetch_gemma(self, api_key, IMAGE, prompt):
        img = self.tensor_to_pil(IMAGE)
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model = 'gemini-flash-latest',
            contents = [prompt, img],
        )
        return(response.text,)

NODE_CLASS_MAPPINGS = {
    'qxNode': qxNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    'qxNode': 'QX Node Comfy',
}
"""
Image Generation Module for Exoplanet Visualization
"""
import requests
import os

def generate_exoplanet_image(params):
    """
    Generate an image of an exoplanet based on its parameters
    """
    # Create a descriptive prompt based on the exoplanet's parameters
    prompt = create_exoplanet_prompt(params)
    
    try:
        # Ensure the static directory exists
        os.makedirs('static/generated', exist_ok=True)
        
        # Generate unique filename based on parameters
        filename = f"exoplanet_{hash(str(params))}.jpg"
        filepath = f"static/generated/{filename}"
        
        # Don't regenerate if image already exists
        if os.path.exists(filepath):
            return {
                'success': True,
                'image_path': filepath,
                'prompt': prompt
            }
        
        # Generate new image
        url = f"https://pollinations.ai/p/{prompt}"
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(filepath, 'wb') as file:
                file.write(response.content)
            return {
                'success': True,
                'image_path': filepath,
                'prompt': prompt
            }
        else:
            return {
                'success': False,
                'error': f"Failed to generate image: {response.status_code}"
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def create_exoplanet_prompt(params):
    """
    Create a descriptive prompt based on exoplanet parameters
    """
    # Extract relevant parameters
    radius = params.get('pl_rade', 1.0)  # Planet radius in Earth radii
    temp = params.get('pl_eqt', 255)     # Equilibrium temperature in K
    star_temp = params.get('st_teff', 5772)  # Star temperature in K
    
    # Build description
    description = []
    
    # Size description
    if radius < 0.5:
        description.append("small rocky")
    elif radius < 2:
        description.append("Earth-like")
    elif radius < 5:
        description.append("super-Earth")
    else:
        description.append("gas giant")
    
    # Temperature and appearance
    if temp < 200:
        description.append("frozen ice world")
    elif temp < 300:
        description.append("temperate world with possible oceans")
    elif temp < 500:
        description.append("hot rocky world")
    else:
        description.append("scorching hot world with molten surface")
    
    # Star influence
    if star_temp < 3500:
        description.append("orbiting a red dwarf star")
    elif star_temp < 5000:
        description.append("under an orange sun")
    elif star_temp < 6000:
        description.append("under a yellow sun")
    else:
        description.append("under a bright blue star")
    
    # Create artistic prompt
    prompt = f"realistic space art of a {' '.join(description)}, high detail, cosmic, beautiful lighting, trending on artstation"
    
    return prompt

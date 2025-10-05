from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"), 
)

completion = client.chat.completions.create(
    model="openai/gpt-5-chat",  
    messages=[
        {"role": "user", "content": "What is the meaning of life?"}
    ],
)

print(completion.choices[0].message.content)


prompt = """ You are an exoplanet habitability expert. Using Earth as the reference, estimate how habitable the following exoplanet is compared to Earth. Provide a percentage similarity (0-100%) and a short justification.

Earth Reference:
- Orbital Period (pl_orbper): 365.256 days
- Planet Radius (pl_rade): 1.0 R_earth
- Insolation Flux (pl_insol): 1.0 Earth flux
- Equilibrium Temperature (pl_eqt): 255 K
- Stellar Effective Temperature (st_teff): 5772 K
- Stellar Radius (st_rad): 1.0 R_sun
- Stellar Surface Gravity (st_logg): 4.44 dex

Exoplanet Data:
- Orbital Period: {pl_orbper} days
- Planet Radius: {pl_rade} R_earth
- Insolation Flux: {pl_insol} Earth flux
- Equilibrium Temperature: {pl_eqt} K
- Stellar Effective Temperature: {st_teff} K
- Stellar Radius: {st_rad} R_sun
- Stellar Surface Gravity: {st_logg} dex

Answer with a single number percentage (0-100%) representing how habitable this planet is compared to Earth and briefly explain why, taking into account potential atmosphere, surface temperature, and rocky composition.   """
import asyncio
from generator import code_generator
import json
import gzip

async def main():
    # Create an instance of the code_generator class
    generator_instance = code_generator()
    
    # Dummy CycloneDX SBOM input
    with open('SBOM_sample.json', 'r') as file:
        dummy_cyclonedx_sbom = json.load(file)
    # Convert the JSON object to a string
    dummy_cyclonedx_sbom = json.dumps(dummy_cyclonedx_sbom, indent=2)
        
    # Call the generate method with the dummy input
    await generator_instance.generate(CycloneDX=dummy_cyclonedx_sbom, num_refinements=1, base_directory="generated_code")

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
from generator import code_generator
import json
import gzip

async def main():
    # Create an instance of the code_generator class
    generator_instance = code_generator()
    
    # Dummy CycloneDX SBOM input
    dummy_cyclonedx_sbom = """
    {
        "bomFormat": "CycloneDX",
        "specVersion": "1.3",
        "version": 1,
        "components": [
            {
                "type": "library",
                "name": "example-lib",
                "version": "1.0.0",
                "licenses": [
                    {
                        "license": {
                            "id": "MIT"
                        }
                    }
                ]
            }
        ]
    }
    """
    
    # Call the generate method with the dummy input
    await generator_instance.generate(CycloneDX=dummy_cyclonedx_sbom)

if __name__ == "__main__":
    asyncio.run(main())
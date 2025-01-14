# SBOM Ground Truth

A pipeline for generating source code from SBOMs using CycloneDX, employing Chain of Thought (CoT) reasoning and iterative refinement to ensure accuracy, consistency, and security in software supply chains.

## Motivation and Introduction

The complexity of modern software supply chains, heavily reliant on third-party libraries and open-source components, has introduced vulnerabilities, as seen in incidents like the SolarWinds breach. To address these risks, Software Bill of Materials (SBOMs) have emerged as critical tools for enhancing transparency, traceability, and security in software ecosystems. However, the effectiveness of SBOM tools depends on accurate and comprehensive ground truth datasets, which are currently scarce.

This repository focuses on leveraging Large Language Models (LLMs) to generate source code that aligns with SBOM metadata, addressing gaps in available datasets and improving SBOM accuracy, completeness, and reliability.

## Pipeline Overview

![SBOM Report Dia Pipe](https://github.com/user-attachments/assets/c4bb25c2-e063-41c7-af11-878db2c5b483)
This repository implements a modular and scalable pipeline for generating source code from SBOMs using the CycloneDX format. The pipeline employs a Chain of Thought (CoT) reasoning approach to ensure precision and incorporates iterative refinement to enhance code accuracy and consistency.

### Pipeline Stages

1. **SBOM Parsing and Understanding**  
   Extracts key metadata, dependencies, and relationships from CycloneDX SBOMs.  
   **Output**: Structured representation of project metadata and dependencies.

2. **Dependency Blueprint Creation**  
   Defines dependency hierarchies, initialization orders, and usage patterns.  
   **Output**: Logical blueprint for scaffolding and file generation.

3. **Source Code Scaffolding**  
   Defines the project's file structure and assigns responsibilities to individual files.  
   **Output**: File structure aligned with SBOM requirements.

4. **Generate Files (Parallel Chains)**  
   Creates project files (e.g., main scripts, requirements files, tests) based on the blueprint.  
   **Output**: Functional project files.

5. **Global File Validation**  
   Ensures cross-file consistency, including imports, dependencies, and function calls.  
   **Output**: Validation report identifying global issues.

6. **Single File Validation and Refinement**  
   Refines individual files to address specific validation issues.  
   **Output**: Validated files ready for integration.

7. **Feedback Loops**  
   Incorporates identified issues into earlier stages for iterative improvement.  
   **Output**: Continuously refined and integrated project files.

### Key Features

- **CycloneDX Support**: CycloneDX format chosen for its lightweight schema, dependency tracking, and alignment with security workflows.
- **LLM Integration**: Uses LLMs to generate realistic datasets and validate SBOM accuracy.
- **Iterative Refinement**: Enhances consistency and security through feedback-driven improvements.
- **Scalability**: Modular design supports future enhancements and dynamic use cases.

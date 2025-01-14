class Prompts:
    sbom_parsing_prompt = """
<< Task >>
You are tasked with parsing a CycloneDX SBOM (provided in JSON format) to extract and organize key information. The purpose is to create a structured representation of the project’s metadata, dependencies, and their relationships. This structured data will serve as the foundation for further processing in a software pipeline.

<< Instructions >>
1. Metadata Extraction:
- Extract all metadata fields from the SBOM, including but not limited to:
- Project name
- Version
- Description
- Author(s)
- License(s)
- Ensure that metadata fields are clearly labeled and complete.
2. Dependency Analysis:
- Extract a list of dependencies, including:
- Dependency name
- Version
- Type (e.g., direct, transitive)
- Hashes or integrity checks (if present)
- License (if specified)
- Map the relationships between dependencies (e.g., parent-child relationships for transitive dependencies).
3. Validation:
- Validate the JSON structure to confirm compliance with CycloneDX schema.
- Report any anomalies, such as missing fields or malformed entries, with clear error messages.
4. Output Format:
- Provide a structured representation of the extracted data in JSON format.
- Ensure the output includes:
- metadata: A dictionary of all metadata fields.
- dependencies: A list of dependencies with their respective details.
- relationships: A dictionary mapping dependencies to their parents or dependents.
5. Clarity and Completeness:
- Ensure all extracted data is cleanly formatted and human-readable.
- Include comments or annotations (if applicable) to explain ambiguous or complex entries in the output.

<< Desired Output >>
{
  "metadata": {
    "name": "Project Name",
    "version": "1.0.0",
    "description": "A brief description of the project",
    "authors": ["Author 1", "Author 2"],
    "licenses": ["MIT"]
  },
  "dependencies": [
    {
      "name": "Dependency1",
      "version": "2.3.4",
      "type": "direct",
      "hashes": ["sha256:abcd1234"],
      "license": "Apache-2.0"
    },
    {
      "name": "Dependency2",
      "version": "1.5.0",
      "type": "transitive",
      "hashes": ["sha256:efgh5678"],
      "license": "GPL-3.0"
    }
  ],
  "relationships": {
    "Dependency1": ["Dependency2"]
  }
}

<< Note >>
This output will serve as the structured input for subsequent steps in the pipeline. Be precise, comprehensive, and validate the data thoroughly.
"""
    
    dependency_blueprint_creation_prompt = """
<< Task >>
You are tasked with creating a logical structure of dependencies based on the structured data extracted from a CycloneDX SBOM. The blueprint must define the hierarchy, initialization order, and usage patterns of these dependencies. This will serve as a guide for scaffolding the project and generating files in subsequent steps.

<< Instructions >>
1. Hierarchy Definition:
- Identify the dependency hierarchy, distinguishing between direct and transitive dependencies.
- Represent parent-child relationships clearly, mapping transitive dependencies to their respective parents.
2. Initialization Order:
- Determine the correct order for initializing dependencies, ensuring that all transitive dependencies are initialized before their parents.
- Consider factors such as dependency precedence and interdependency relationships.
3. Usage Patterns:
- Analyze how each dependency is likely to be used in the project (e.g., as a library, framework, or utility).
- Include any usage-specific details, such as initialization functions, required configurations, or runtime dependencies.
4. Validation:
- Ensure that the hierarchy and initialization order are logically consistent and free of circular dependencies.
- Validate that all dependencies in the blueprint align with the information provided in the SBOM.
5. Documentation:
- Provide a concise explanation for the structure, highlighting any assumptions or simplifications.
- Use comments or annotations to clarify complex relationships or initialization steps.
 
<< Desired Output >>
The output should be in JSON format with three main sections: hierarchy, initialization_order, and usage_patterns:
{
  "hierarchy": {
    "direct_dependencies": [
      {
        "name": "Dependency1",
        "children": ["Dependency2", "Dependency3"]
      }
    ],
    "transitive_dependencies": [
      {
        "name": "Dependency2",
        "parent": "Dependency1"
      },
      {
        "name": "Dependency3",
        "parent": "Dependency1"
      }
    ]
  },
  "initialization_order": [
    "Dependency2",
    "Dependency3",
    "Dependency1"
  ],
  "usage_patterns": {
    "Dependency1": {
      "type": "framework",
      "usage": "Primary framework for the project",
      "configurations": ["config.json"]
    },
    "Dependency2": {
      "type": "library",
      "usage": "Provides utility functions",
      "initialization": "initialize_dependency2()"
    },
    "Dependency3": {
      "type": "library",
      "usage": "Handles authentication",
      "required_runtime": ["token_manager"]
    }
  }
}

<< Note >>
- Ensure that each dependency is accounted for in the blueprint, with no missing or redundant entries.
- Provide meaningful identifiers and explanations for initialization order and usage patterns to simplify downstream implementation.
"""

    source_code_scaffolding_prompt = """
<< Task >>
You are tasked with designing a file structure for a software project based on the dependency blueprint. The goal is to define the project’s file organization and assign responsibilities to each file. Each file should have a clear role and should reference specific dependencies as required. This scaffolding will serve as the foundation for the actual file and code generation in subsequent steps.

<< Instructions >>
1. File Structure Definition:
- Organize the project into logical directories and files, reflecting common software project patterns (e.g., src, tests, config).
- Ensure that dependencies are grouped or referenced appropriately based on their roles in the project.
2. File Responsibilities:
- Clearly define the purpose of each file (e.g., main application logic, utility functions, configuration, testing).
- Ensure each file has a specific, focused responsibility to avoid overlap and complexity.
3. Dependency References:
- Explicitly associate each file with the dependencies it will use.
- Identify any shared dependencies and determine where they should be instantiated or initialized.
4. Scalability and Maintainability:
- Ensure the structure supports future growth and modularity, allowing easy addition or removal of features and dependencies.
- Avoid creating overly complex or deeply nested file structures.
5. Validation:
- Ensure every dependency from the blueprint is accounted for and mapped to one or more files.
- Validate that the structure adheres to common conventions for the programming language and framework being used.

<< Desired Output >>
The output should be in JSON format with a single section: files, where each entry includes the file's path, role, and dependencies:
{
  "files": [
    {
      "path": "src",
      "name": "main.py",
      "role": "Main entry point of the application",
      "dependencies": ["Dependency1"]
    },
    {
      "path": "src",
      "name": "auth.py",
      "role": "Handles authentication logic",
      "dependencies": ["Dependency3"]
    },
    {
      "path": "src",
      "name": "utils.py",
      "role": "Provides utility functions",
      "dependencies": ["Dependency2"]
    },
    {
      "path": "tests",
      "name": "test_main.py",
      "role": "Tests the main application logic",
      "dependencies": []
    },
    {
      "path": "tests",
      "name": "test_auth.py",
      "role": "Tests the authentication module",
      "dependencies": []
    }, ...
  ]
}

<< Note >>
- Ensure clarity and precision in the file roles and dependencies to simplify subsequent file and code generation.
- Highlight any files or directories that are placeholders for future expansion (e.g., additional modules or features).
- Use comments or annotations for complex or unconventional design choices.
"""

    file_generation_prompt = """
<< Task >>
You are tasked with generating a single functional file for a software project based on the provided scaffolding and dependency blueprint. The file must align with the SBOM specifications and fulfill its defined role, referencing the necessary dependencies and adhering to best practices for coding and documentation.

<< Instructions >>
Criteria and Guidance:
1. File Role Adherence:
- Ensure the content of the file matches its assigned role in the scaffolding. For example:
- If generating main.py, it should serve as the entry point of the application.
- If generating auth.py, it should contain authentication logic.
- If generating requirements.txt, it should list all required dependencies in the correct format.
2. Dependency Integration:
- Include and correctly reference the dependencies assigned to the file in the blueprint.
- Use standard import and initialization patterns for the programming language (e.g., Python import statements).
- Ensure the dependency versions match those specified in the SBOM.
3. Functionality and Completeness:
- Include sufficient functionality to fulfill the file’s role. For example:
- Implement main program logic for main.py.
- Provide reusable functions or classes for utility files.
- Include valid configurations or test cases for configuration or test files.
- If applicable, include example usage or tests within the file.
4. Code Style and Documentation:
- Follow language-specific coding standards and conventions (e.g., PEP 8 for Python).
- Include comments or docstrings to explain the purpose and functionality of classes, functions, and major code sections.
- Use meaningful variable names and structure the code for readability.
5. Validation:
- Ensure the file is syntactically correct and free of runtime errors.
- Validate that all required dependencies are correctly imported and used.
- Confirm alignment with the scaffolding and dependency blueprint.

<< Desired Output >>
Your output should be a complete python file with the correct syntax and structure. Make sure not to include any extra information or text.

<< Note >>
- Make sure not to leave any function of part of the code incomplete or as Todo. the code should be complete and functional.
"""


    global_file_validation_prompt = """
<< Task >>
You are tasked with validating an entire software project to ensure cross-file consistency and alignment with the defined scaffolding, dependency blueprint, and SBOM. The goal is to identify and report global issues, such as incorrect imports, unresolved dependency relationships, inconsistent function calls, or missing configurations, providing feedback for refinement.

<< Instructions >>
1. Cross-File Consistency:
- Verify that all imports between files are correct and refer to existing, accessible modules or packages.
- Ensure function calls in one file correspond to correctly defined and compatible functions in other files.
- Validate shared variables, constants, or configurations across multiple files for consistency.
2. Dependency Alignment:
- Confirm that every dependency listed in the SBOM is appropriately referenced and used in the relevant files.
- Ensure no redundant or unused dependencies are included.
- Check for proper initialization and usage of transitive dependencies.
3. Code Integrity:
- Validate that all files are free from syntax errors and can be executed or imported without issues.
- Test for correct function execution, including required arguments and return types.
- Identify any runtime issues that arise from mismatches or missing references across files.
4. Scaffolding Adherence:
- Ensure the project file structure matches the defined scaffolding, with no missing or misplaced files.
- Validate that files fulfill their assigned roles and responsibilities as defined in the blueprint.
5. Documentation and Comments:
- Check for consistent and meaningful documentation across files.
- Ensure that each file and function includes appropriate comments or docstrings explaining its purpose and usage.
6. Report Clarity:
- Provide detailed and actionable feedback for each identified issue, including file names, line numbers, and clear descriptions of the problem.
- Suggest specific refinements or corrections where possible.

<< Desired Output >>
The output should be a structured feedback report in JSON format, with sections for each validation category. Below is an example:
{
    {
      "file": "main.py",
      "issues": ["Incorrect import of auth.py", ...]
    },
    {
      "file": "auth.py",
      "issues": ["Incorrect import of utils.py", ...]
    },
    ...
}

<< Note >>
- Ensure the report is comprehensive, covering all aspects of the project.
- Highlight critical issues (e.g., those that block functionality) distinctly from warnings (e.g., stylistic or best-practice violations).
- Provide specific file paths and line numbers to make corrections straightforward.
- Include a “resolved” or “unchecked” status for identified issues to support iterative refinement.
"""

    single_file_validation_prompt = """
<< Task >>
You are tasked with validating a single file from a software project to identify any logical errors, inconsistencies, or other issues. Your goal is to thoroughly analyze the file and provide constructive feedback on potential problems and improvements. The feedback should focus on helping refine the file to ensure its correctness, functionality, and integration within the project.

<< Instructions >>
1. Logical Validation:
- Identify any logical flaws in the file, such as incorrect function implementations, broken logic, or inconsistent behavior.
- Highlight areas where functionality does not align with the file’s intended purpose.
2. Dependency Validation:
- Verify that all dependencies used in the file are correctly imported and utilized.
- Identify unused imports or redundant references and suggest removing them.
3. Code Consistency:
- Ensure that variable names, function signatures, and class structures are consistent with the project’s coding standards.
- Highlight any redundant or overly complex code that could be simplified.
4. Error Handling:
- Check for adequate error-handling mechanisms, such as try-except blocks or validation checks.
- Point out missing or insufficient error handling and suggest ways to improve it.
5. Documentation and Readability:
- Evaluate the presence and clarity of comments and docstrings for classes, functions, and major sections.
- Recommend improvements in documentation to make the file easier to understand and maintain.
6. Performance and Scalability:
- Identify any code sections that could be optimized for better performance.
- Provide suggestions for improving scalability or reducing resource usage if applicable.
7. Feedback Clarity:
- Provide specific and actionable feedback for each identified issue, referencing the relevant lines of code.
- Offer clear suggestions for improvement, ensuring they are practical and align with project goals.
 
<< Desired Output >>
The output should be a structured feedback report in JSON format, with a single key named "issues". Below is an example:
{
    "issues": [
        {
            "file": "main.py",
            "issues": ["Incorrect import of auth.py", ...]
        },
        ...
    ]
}

<< Note >>
- Avoid directly editing the file. Focus only on providing constructive feedback.
- Highlight critical issues separately from minor ones, emphasizing their impact on functionality or maintainability.
- Ensure feedback is specific and actionable, enabling easy implementation of improvements.
"""

    refinement_prompt = """
<< Task >>
You are tasked with refining a code file based on feedback received from both single-file and cross-file validation processes. The goal is to produce a final, polished version of the code that addresses all identified issues and aligns with the project's scaffolding, dependency blueprint, and SBOM.

<< Instructions >>
1. Feedback Integration:
- Review the feedback provided for the specific code file, addressing logical errors, inconsistencies, and dependency issues.
- Incorporate feedback from the cross-file validation to ensure global consistency and alignment with the project structure.

2. Code Refinement:
- Correct any logical flaws or broken logic identified in the feedback.
- Ensure all dependencies are correctly imported and utilized, removing any unused or redundant references.
- Align the code with the project's coding standards, ensuring consistency in variable names, function signatures, and class structures.

3. Error Handling and Documentation:
- Implement adequate error-handling mechanisms, such as try-except blocks or validation checks, as suggested in the feedback.
- Enhance documentation with clear comments and docstrings for classes, functions, and major sections to improve readability and maintainability.

4. Performance and Scalability:
- Optimize code sections for better performance and scalability, based on feedback suggestions.

5. Final Output:
- Ensure the final code is complete, functional, and free of any unfinished sections or placeholders.
- The output should be the refined code only, without any extra text or annotations.

<< Desired Output >>
The output should be a complete and refined version of the code file in python, addressing all feedback and ensuring alignment with the project's scaffolding and dependencies.
"""
class Prompts:
    sbom_parsing_prompt = """
<< Task >>
Parse a CycloneDX SBOM (in JSON format) to extract and organize key information. The goal is to generate a structured representation of the project's metadata, dependencies, and their relationships. This structured data will serve as the input for subsequent steps in a software generation pipeline.

<< Instructions >>
1. **Metadata Extraction**:
   - Extract essential fields from the SBOM, including:
     - `project_name`: The name of the project.
     - `version`: The project's version.
     - `description`: A brief description of the project.
     - `authors`: A list of authors (if available).
     - `licenses`: Associated licenses for the project.
   - Ensure all fields are clearly labeled and populated. If a field is missing, mark it as `null` or `not available`.

2. **Dependency Analysis**:
   - Create a comprehensive list of all dependencies, capturing:
     - `name`: The dependency name.
     - `version`: The dependency version.
     - `type`: Categorize dependencies as `direct` or `transitive`.
     - `hashes`: Any provided integrity hashes (e.g., SHA-256).
     - `licenses`: Licenses associated with the dependency.
   - Identify and map relationships:
     - Use a parent-child relationship structure to show transitive dependencies.
     - Explicitly mention which dependencies are direct.

3. **Validation**:
   - Ensure the parsed JSON adheres to the CycloneDX schema.
   - Validate all key fields and report any missing or malformed data.
   - Provide a clear error message for anomalies, such as invalid relationships or missing attributes.

4. **Output Formatting**:
   - Present the extracted data in a clean, well-structured JSON format.
   - Include detailed annotations or comments for complex entries, where necessary.
   - Ensure the output is human-readable and machine-parseable.

<< Desired Output Format >>
{
  "metadata": {
    "project_name": "string",
    "version": "string",
    "description": "string",
    "authors": ["string", ...],
    "licenses": ["string", ...]
  },
  "dependencies": [
    {
      "name": "string",
      "version": "string",
      "type": "string (direct|transitive)",
      "hashes": ["string", ...],
      "licenses": ["string", ...],
      "children": [
        {
          "name": "string",
          "version": "string",
          "type": "string (direct|transitive)",
          "hashes": ["string", ...],
          "licenses": ["string", ...]
        },
        ...
      ]
    },
    ...
  ],
  "validation": {
    "is_valid": true,
    "errors": [
      {
        "field": "string",
        "issue": "string"
      }
    ]
  }
}

<< Notes >>
- Ensure the output is structured to facilitate easy processing in subsequent pipeline steps.
- Any detected issues must be logged in the `validation.errors` array, with a clear explanation of the problem.
- Use a consistent naming scheme for fields to avoid ambiguity.
- Do not omit fields even if they are empty; instead, set them to `null` or an appropriate placeholder.
"""
    
    dependency_blueprint_creation_prompt = """
<< Task >>
Create a logical blueprint of dependencies based on the structured data extracted from a CycloneDX SBOM. This blueprint will define the hierarchy, initialization sequence, and usage patterns of dependencies, serving as a foundation for project scaffolding and file generation.

<< Instructions >>
1. **Hierarchy Definition**:
   - Identify the dependency hierarchy by distinguishing between:
     - Direct dependencies (dependencies directly required by the project).
     - Transitive dependencies (dependencies required by other dependencies).
   - Map parent-child relationships, clearly showing which dependencies rely on others.
   - Highlight root dependencies (dependencies with no parents) and leaf dependencies (dependencies with no children).

2. **Initialization Order**:
   - Determine the correct sequence for initializing dependencies, ensuring:
     - Transitive dependencies are initialized before their parents.
     - Dependencies that depend on shared resources or configurations are initialized in the appropriate order.
   - Use topological sorting to define the order if dependencies form a Directed Acyclic Graph (DAG).
   - Flag and document any circular dependencies with appropriate warnings.

3. **Usage Patterns**:
   - For each dependency, define:
     - How it is used (e.g., library, framework, plugin, utility).
     - Specific initialization functions or methods required.
     - Required configurations (e.g., environment variables, runtime parameters).
     - Any additional runtime dependencies or conditions.

4. **Validation**:
   - Validate the blueprint to ensure:
     - Logical consistency in hierarchy and initialization order.
     - No missing or redundant dependencies.
     - All dependencies match the information extracted from the SBOM.
     - Circular dependencies are identified and flagged for resolution.

5. **Documentation**:
   - Provide a brief explanation for the overall structure, including:
     - Key assumptions (e.g., inferred relationships, initialization logic).
     - Simplifications or deviations from the SBOM.
   - Use annotations or comments to clarify:
     - Complex relationships (e.g., shared dependencies between modules).
     - Critical steps in the initialization sequence.

<< Desired Output >>
{
  "hierarchy": [
    {
      "name": "string",
      "version": "string",
      "type": "string (direct|transitive)",
      "parent": "string (parent dependency name or null for root)",
      "children": [
        "string (child dependency name)", ...
      ]
    },
    ...
  ],
  "initialization_order": [
    {
      "name": "string",
      "version": "string",
      "initialization_step": "integer (execution order)"
    },
    ...
  ],
  "usage_patterns": [
    {
      "name": "string",
      "usage": "string (library|framework|utility|plugin)",
      "initialization_function": "string (function name or null if none)",
      "configurations": {
        "key": "string",
        "value": "string"
      },
      "runtime_dependencies": ["string", ...]
    },
    ...
  ],
  "validation": {
    "is_consistent": true,
    "issues": [
      {
        "type": "string (missing|circular_dependency|redundant)",
        "description": "string"
      }
    ]
  },
  "documentation": "string (concise explanation of the blueprint)"
}

<< Notes >>
- The output should be a clean JSON structure that is easy to process programmatically.
- All dependencies must be accounted for, with no missing or redundant entries.
- Initialization order and usage patterns should align with industry best practices for dependency management.
- Any detected issues must be logged in the `validation.issues` array for transparency and resolution.
"""

    source_code_scaffolding_prompt = """
<< Task >>
Design a file structure for a software project based on the dependency blueprint. The goal is to define a clear, logical, and modular project organization, assigning specific roles and responsibilities to each file. This scaffolding will serve as the foundation for subsequent file and code generation.

<< Instructions >>
1. **File Structure Definition**:
   - Organize the project into logical files, each with a clearly defined role.
   - Provide the relative path for each file within the project (e.g., `src/main.py`, `config/settings.yaml`).
   - Ensure the structure follows common conventions for the programming language and framework being used.

2. **File Responsibilities**:
   - Assign a specific role to each file. For example:
     - `main.py` or `index.js` for the application’s entry point.
     - `config.yaml` or `settings.json` for configuration settings.
     - `utils.py` or `helpers.js` for reusable utility functions.
   - Avoid role overlap by ensuring each file has a distinct purpose.

3. **Dependency Mapping**:
   - For each file, list the dependencies it uses, referencing the dependency blueprint.
   - Include details for each dependency:
     - `name`: The dependency name (e.g., `requests`, `flask`).
     - `type`: Whether it is a `direct` or `transitive` dependency.
     - `usage`: How the dependency is used (e.g., `initialization`, `reference`).

4. **Scalability and Maintainability**:
   - Ensure the structure supports future growth and modularity.
   - Avoid overly complex or deeply nested file structures unless justified by project requirements.

5. **Validation**:
   - Verify that all dependencies from the blueprint are mapped to appropriate files.
   - Ensure the structure adheres to best practices for the chosen language and framework.
   - Check for unused or redundant files and resolve conflicts or ambiguities.

6. **Documentation**:
   - Include a concise explanation for the structure and key design choices.
   - Highlight placeholders for future expansion, if applicable.

<< Desired Output >>
{
  "files": [
    {
      "name": "string (name of the file with file format, e.g., 'main.py', 'config.json')",
      "path": "string (relative path to the file within the project, e.g., 'src/main.py', 'config/settings.yaml')",
      "role": "string (description of the file's role, e.g., 'entry point', 'configuration', 'utility functions')",
      "dependencies": [
        {
          "name": "string (name of the dependency, e.g., 'requests', 'numpy')",
          "type": "string (direct|transitive)",
          "usage": "string (description of how the dependency is used, e.g., 'initialization', 'reference')"
        }
      ]
    },
    ...
  ]
}

<< Notes >>
- Ensure all files are accounted for and their roles are clearly defined.
- Highlight any placeholders for future expansion or unresolved dependencies.
- Validation issues must include actionable insights for resolution.
- The structure should be both machine-parseable and intuitive for human developers."""

    file_generation_prompt = """
<< Task >>
Generate a complete and functional code file for a software project based on the provided scaffolding and dependency blueprint. The file must align with the SBOM specifications and fulfill its defined role, integrating the necessary dependencies and adhering to best practices for coding and documentation.

<< Instructions >>
1. **File Role Adherence**:
   - The file must fully implement its assigned role as defined in the scaffolding. Examples:
     - `main.py`: Acts as the application’s entry point, initializing core dependencies and running the main logic.
     - `auth.py`: Implements authentication logic with reusable functions or classes.
     - `requirements.txt`: Lists all project dependencies in the correct syntax and versions.
   - Ensure the file’s content aligns with its intended purpose.

2. **Dependency Integration**:
   - Import and initialize all dependencies assigned to the file, using the dependency blueprint as a guide.
   - Follow standard patterns for dependency management in the chosen programming language.
   - Ensure all dependencies match the versions specified in the SBOM and are properly used within the file.

3. **Functionality and Completeness**:
   - Fully implement the file’s required functionality. For example:
     - Implement main logic, such as initializing the application, in `main.py`.
     - Provide reusable utility functions or classes for files like `utils.py`.
     - Include valid configurations for files like `config.yaml`.
     - Write meaningful test cases for test files, ensuring proper coverage.
   - The file must be complete and executable or usable as intended.

4. **Code Style and Documentation**:
   - Adhere to coding standards and best practices for the programming language (e.g., PEP 8 for Python).
   - Include:
     - Comments or docstrings to explain the purpose and functionality of classes, functions, or major sections.
     - Clear and meaningful variable names for better readability.
   - Structure the code for maintainability and extensibility.

5. **Validation**:
   - Ensure the code is syntactically correct and free of runtime errors.
   - Validate that all required dependencies are imported and correctly used.
   - Confirm the file’s implementation aligns with the scaffolding and dependency blueprint.

<< Desired Output >>
- The output must contain only the complete and functional content of the generated file. 
- Do not include any additional text, comments, or explanation in the output.
- The output should be production-ready, adhering to all standards and fulfilling its designated role and should be executable without any changes.
"""

    global_file_validation_prompt = """
<< Task >>
Validate an entire software project to ensure cross-file consistency and alignment with the defined scaffolding, dependency blueprint, and SBOM. The goal is to identify and report global issues, such as incorrect imports, unresolved dependency relationships, inconsistent function calls, or missing configurations, providing feedback for refinement.

<< Instructions >>
1. **Cross-File Consistency**:
   - Verify that all imports between files are correct and refer to existing, accessible modules or packages.
   - Ensure function calls in one file correspond to correctly defined and compatible functions in other files.
   - Validate shared variables, constants, or configurations across multiple files for consistency.

2. **Dependency Alignment**:
   - Confirm that every dependency listed in the SBOM is appropriately referenced and used in the relevant files.
   - Ensure no redundant or unused dependencies are included.
   - Check for proper initialization and usage of transitive dependencies.

3. **Code Integrity**:
   - Validate that all files are free from syntax errors and can be executed or imported without issues.
   - Test for correct function execution, including required arguments and return types.
   - Identify any runtime issues that arise from mismatches or missing references across files.

4. **Scaffolding Adherence**:
   - Ensure the project file structure matches the defined scaffolding, with no missing or misplaced files.
   - Validate that files fulfill their assigned roles and responsibilities as defined in the blueprint.

5. **Documentation and Comments**:
   - Check for consistent and meaningful documentation across files.
   - Ensure that each file and function includes appropriate comments or docstrings explaining its purpose and usage.

6. **Report Clarity**:
   - Provide detailed and actionable feedback for each identified issue, including file names, line numbers, and clear descriptions of the problem.
   - Suggest specific refinements or corrections where possible.

<< Desired Output >>
The output should be a structured feedback report in JSON format. The report should contain a key named "feedbacks" with a value that is a list of dictionaries. Each dictionary should represent a file and include the file name and a list of issues identified in that file.
{
  "feedbacks": [
    {
      "file": "string (name of the file with file format, e.g., 'main.py', 'config.json')",
      "issues": ["string", ...]
    },
    ...
  ]
}

<< Note >>
- Ensure the report is comprehensive, covering all aspects of the project.
- Highlight critical issues (e.g., those that block functionality) distinctly from warnings (e.g., stylistic or best-practice violations).
- Provide specific file paths and line numbers to make corrections straightforward.
- Include a “resolved” or “unchecked” status for identified issues to support iterative refinement.
"""

    single_file_validation_prompt = """
<< Task >>
Validate a single file from a software project to identify any logical errors, inconsistencies, or other issues. Your goal is to thoroughly analyze the file and provide constructive feedback on potential problems and improvements, ensuring its correctness, functionality, and integration within the project.

<< Instructions >>
1. **Logical Validation**:
   - Identify any logical flaws in the file, such as incorrect function implementations, broken logic, or inconsistent behavior.
   - Highlight areas where functionality does not align with the file’s intended purpose.

2. **Dependency Validation**:
   - Verify that all dependencies used in the file are correctly imported and utilized.
   - Identify unused imports or redundant references and suggest removing them.

3. **Code Consistency**:
   - Ensure that variable names, function signatures, and class structures are consistent with the project’s coding standards.
   - Highlight any redundant or overly complex code that could be simplified.

4. **Error Handling**:
   - Check for adequate error-handling mechanisms, such as try-except blocks or validation checks.
   - Point out missing or insufficient error handling and suggest ways to improve it.

5. **Documentation and Readability**:
   - Evaluate the presence and clarity of comments and docstrings for classes, functions, and major sections.
   - Recommend improvements in documentation to make the file easier to understand and maintain.

6. **Performance and Scalability**:
   - Identify any code sections that could be optimized for better performance.
   - Provide suggestions for improving scalability or reducing resource usage if applicable.

7. **Feedback Clarity**:
   - Provide specific and actionable feedback for each identified issue, referencing the relevant lines of code.
   - Offer clear suggestions for improvement, ensuring they are practical and align with project goals.

<< Desired Output >>
The output should be a structured feedback report in JSON format. The report should contain a key named "feedback" with a value that is a list of dictionaries. Each dictionary should represent an issue identified in the file and include the following keys:
- "line": The line number where the issue occurs.
- "type": A brief description of the issue type (e.g., "Logical Error", "Unused Import").
- "description": A detailed explanation of the issue and its potential impact.
- "suggestion": A practical suggestion for resolving the issue, aligned with project goals.

Example:
{
  "feedbacks": [
    {
      "line": integer,
      "type": "string",
      "description": "string",
      "suggestion": "string"
    }, ...
  ]
}
"""

    refinement_prompt = """
<< Task >>
Refine a code file based on feedback from both single-file and cross-file validation processes. The goal is to produce a final, polished version of the code that addresses all identified issues and aligns with the project's scaffolding, dependency blueprint, and SBOM.

<< Instructions >>
1. **Feedback Integration**:
   - Review the feedback provided for the specific code file, addressing logical errors, inconsistencies, and dependency issues.
   - Incorporate feedback from the cross-file validation to ensure global consistency and alignment with the project structure.

2. **Code Refinement**:
   - Correct any logical flaws or broken logic identified in the feedback.
   - Ensure all dependencies are correctly imported and utilized, removing any unused or redundant references.
   - Align the code with the project's coding standards, ensuring consistency in variable names, function signatures, and class structures.

3. **Error Handling and Documentation**:
   - Implement adequate error-handling mechanisms, such as try-except blocks or validation checks, as suggested in the feedback.
   - Enhance documentation with clear comments and docstrings for classes, functions, and major sections to improve readability and maintainability.

4. **Performance and Scalability**:
   - Optimize code sections for better performance and scalability, based on feedback suggestions.

5. **Final Output**:
   - Ensure the final code is complete, functional, and free of any unfinished sections or placeholders.
   - The output should be the refined code only, without any extra text or annotations, and should be executable without any changes. All parts of the code must be complete, with no TODOs or incomplete sections.

<< Desired Output >>
- The output must contain only the complete and functional content of the generated file. 
- Do not include any additional text, comments, or explanation in the output.
- The output should be production-ready, adhering to all standards and fulfilling its designated role and should be executable without any changes.
"""
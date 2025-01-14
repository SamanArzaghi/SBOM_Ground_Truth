from utilities import openai_async_wrapper
from openai import AsyncOpenAI
from config import API_KEY
from prompts import Prompts
import asyncio
import os

class code_generator:
    def __init__(self):
        self.openai_aclient = AsyncOpenAI(api_key=API_KEY)
        self.file_generation_tasks = []
        self.code_generated = {}
        self.file_feedback_tasks = []
        self.file_feedback = {}
        self.refined_code_tasks = []
        self.global_feedback = {}
        
    async def generate(self, CycloneDX: str = "", num_refinements: int = 3, base_directory: str = "generated_code"):
        # Parse the CycloneDX SBOM
        sbom_parsed = await self.handle_sbom_parsing(CycloneDX)

        # Generate a dependency blueprint from the parsed SBOM
        dependency_blueprint = await self.handle_dependency_blueprint(sbom_parsed)

        # Create source code scaffolding based on the dependency blueprint
        source_code_scaffolding = await self.handle_source_code_scaffolding(dependency_blueprint)

        # Create async tasks for file generation
        for file_info in source_code_scaffolding['files']:
            file_name = file_info['name']
            file_role = file_info['role']
            file_dependencies = file_info['dependencies']
            file_path = file_info['path']
            task = self.handle_file_generation(file_name, file_role, file_dependencies, file_path, source_code_scaffolding)
            self.file_generation_tasks.append(task)

        # Run all tasks concurrently
        for task in self.file_generation_tasks:
            code, file_name, file_role, file_dependencies, file_path = await task
            self.code_generated[file_name] = {"code": code, "role": file_role, "dependencies": file_dependencies, "path": file_path}

        # Refine the codes num_refinements times
        for _ in range(num_refinements):
            # Clear tasks before each iteration
            self.file_feedback_tasks.clear()  
            self.refined_code_tasks.clear()   
            # Create async tasks for file feedback generation
            for file_name, file_info in self.code_generated.items():
                task = self.get_feedback(role=file_info["role"], dependencies=file_info["dependencies"], code=file_info["code"], source_code_scaffolding=source_code_scaffolding)
                self.file_feedback_tasks.append((task, file_name)) 
            for task, file_name in self.file_feedback_tasks:
                feedback = await task
                self.file_feedback[file_name] = feedback
            # Generate feedback on overall codes
            global_feedback = await self.get_global_feedback(all_codes=self.code_generated, source_code_scaffolding=source_code_scaffolding)
            self.global_feedback.update(global_feedback)
            
            # Refine the code based on feedbacks
            for file_name, file_info in self.code_generated.items():
                # Retrieve single feedback for the file
                single_feedback = self.file_feedback.get(file_name, "")
                # Retrieve global feedback for the file
                global_feedback_issues = self.global_feedback.get(file_name, {}).get('issues', [])

                # Create a task to refine the code
                task = self.refine_code(feedbacks=[single_feedback, global_feedback_issues], code=file_info["code"])
                self.refined_code_tasks.append((task, file_name))
                
            for task, file_name in self.refined_code_tasks:
                refined_code = await task
                self.code_generated[file_name]["code"] = refined_code

        await self.create_and_write_files(base_directory=base_directory)

    async def create_and_write_files(self, base_directory: str):
        for file_name, file_info in self.code_generated.items():
            # Prepend the base directory to the file path
            file_path = os.path.join(base_directory, file_info["path"])
            code = file_info["code"]

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the code to the file
            with open(file_path, 'w') as file:
                file.write(code)


    async def handle_sbom_parsing(self, CycloneDX: str = ""):
        sys_prompt = Prompts.sbom_parsing_prompt
        user_prompt = f"""
<< CycloneDX SBOM >>
{CycloneDX}

Parsed SBOM:"""

        result = await openai_async_wrapper(
            sys_prompt=sys_prompt,
            user_prompt=user_prompt,
            user_client=self.openai_aclient,
            output="json"
        )

        return result


    async def handle_dependency_blueprint(self, sbom_parsed: dict = {}):
        sys_prompt = Prompts.dependency_blueprint_creation_prompt
        user_prompt = f"""
<< Parsed SBOM Data >>
{sbom_parsed}

Dependency Blueprint:"""

        result = await openai_async_wrapper(
            sys_prompt=sys_prompt,
            user_prompt=user_prompt,
            user_client=self.openai_aclient,
            output="json"
        )

        return result

    async def handle_source_code_scaffolding(self, dependency_blueprint: dict = {}):
        sys_prompt = Prompts.source_code_scaffolding_prompt
        user_prompt = f"""
<< Dependency Blueprint >>
{dependency_blueprint}

Source Code Scaffolding:"""

        result = await openai_async_wrapper(
            sys_prompt=sys_prompt,
            user_prompt=user_prompt,
            user_client=self.openai_aclient,
            output="json"
        )

        return result
    
    async def handle_file_generation(self, file_name, file_role, file_dependencies, file_path, source_code_scaffolding):
        sys_prompt = Prompts.file_generation_prompt
        user_prompt = f"""
<< File Name >>
{file_name}

<< File Role >>
{file_role}

<< File Dependencies >>
{file_dependencies}

<< Source Code Scaffolding >>
{source_code_scaffolding}

Generated Code:"""

        result = await openai_async_wrapper(
            sys_prompt=sys_prompt,
            user_prompt=user_prompt,
            user_client=self.openai_aclient,
            output="text"
        )

        return result, file_name, file_role, file_dependencies, file_path

    async def get_feedback(self, role, dependencies, code, source_code_scaffolding):
        sys_prompt = Prompts.feedback_generation_prompt
        user_prompt = f"""
<< File Role >>
{role}

<< File Dependencies >>
{dependencies}

<< Generated Code >>
{code}

<< Source Code Scaffolding >>
{source_code_scaffolding}

Feedback:"""

        feedback = await openai_async_wrapper(
            sys_prompt=sys_prompt,
            user_prompt=user_prompt,
            user_client=self.openai_aclient,
            output="text"
        )

        return feedback

    async def get_global_feedback(self, all_codes, source_code_scaffolding):
        sys_prompt = Prompts.global_feedback_generation_prompt
        user_prompt = f"""
<< All Generated Codes >>
{all_codes}

<< Source Code Scaffolding >>
{source_code_scaffolding}

Global Feedback:"""

        global_feedback = await openai_async_wrapper(
            sys_prompt=sys_prompt,
            user_prompt=user_prompt,
            user_client=self.openai_aclient,
            output="json"
        )

        return global_feedback

    async def refine_code(self, feedbacks, code):
        sys_prompt = Prompts.code_refinement_prompt
        user_prompt = f"""
<< Original Code >>
{code}

<< Feedbacks >>
{feedbacks}

Refined Code:"""

        refined_code = await openai_async_wrapper(
            sys_prompt=sys_prompt,
            user_prompt=user_prompt,
            user_client=self.openai_aclient,
            output="text"
        )

        return refined_code

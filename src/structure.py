#----- Libraries -----#
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

#----- Dependencies -----#
from src.share import State, Feedback, Code_Format, Improvement
from src.log.logger import logging

#----- LLM -- Model -----#
def get_model():
    model = ChatGroq(model = st.session_state.selected_llm['model'])
    reasoning_model = OllamaLLM(model = st.session_state.selected_reasoning_llm['model'])
    # phi_model = OllamaLLM(model = "Phi-4")
    return model, reasoning_model

   #----- LLM -- Structured -- Output -----#
def structred_output_llm():
    model, reasoning_model = get_model()
    feed_back_model = model.with_structured_output(Feedback)
    code_format_model = model.with_structured_output(Code_Format)
    improvement_model = model.with_structured_output(Improvement)
    return feed_back_model, code_format_model, improvement_model

#----- Setup -----#
load_dotenv()

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = 'llm-app'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'

#----- Logger Setup -----#
log1 = logging.getLogger('Update-Structure')
log1.setLevel(logging.DEBUG)

log2 = logging.getLogger('Error-Structure')
log2.setLevel(logging.INFO)

log_out = logging.getLogger("LLM Output")
log_out.setLevel(logging.INFO)

#----- Structure -----#
class graph_node:
    def __init__(self):
        self.model, self.reasoning_model = get_model()
        self.feed_back_model, self.code_format_model, self.improvement_model = structred_output_llm()

    #----------------------------------------
    def User_Story(self, state: State):
        st.session_state.state = 'User Story'

        # if usery already exists then analize it and use feedback to improve on.
        if state.get('user_story'):
            res = self.reasoning_model.invoke([ 
                {'role':'assistant', 'content':""" This is for your referance as to how we made our user stories earlier.
                                                You are a senior product manager. Your task is twofold:
                                                1. **Generate a user story** using the standard format:
                                                    - As a #user_role,
                                                    - I want to #goal,
                                                    - So that #benefit.

                                                2. **Add 2–3 clear acceptance criteria**.

                                                3. **Evaluate the user story using the INVEST framework**:
                                                    - Independent: 
                                                    - Negotiable:
                                                    - Valuable:
                                                    - Estimable:
                                                    - Small:
                                                    - Testable:
                                                Provide the evaluation in a markdown checklist format with short explanations for each."""},
                {'role':'system', 'content':f"""You are a Senior Product Owner. First analyzise the user story: {state['user_story']}. 
                                                Now make necessary changes catering to clients feedback: {state['user_feedback']}"""},
            ])
            log1.info('Implemented Clients feedback - User Story')
            print(res)
        
        else:
            res = self.reasoning_model.invoke([ 
                {'role':'system', 'content':"""You are a senior product manager. Your task is twofold:
                                            1. **Generate a user story** using the standard format:
                                                - As a #user_role,
                                                - I want to #goal,
                                                - So that #benefit.

                                            2. **Add 2–3 clear acceptance criteria**.

                                            3. **Evaluate the user story using the INVEST framework**:
                                                - Independent:
                                                - Negotiable:
                                                - Valuable:
                                                - Estimable:
                                                - Small:
                                                - Testable:
                                            Provide the evaluation in a markdown checklist format with short explanations for each."""},
                
                {'role':'user', 'content':f'User requirement: {state["user_requirement_input"]}'}
            ])
            log1.info('Genrated - User Story')
            print(res)
        return {'user_story' : res}
        
    #------ Interrupt will happen, input: user feedback -----#
    def User_Story_Sentiment(self, state: State):
        st.session_state.state = 'User Story Feedback'
        log1.info('User_Story_Sentiment')
        return state

    def Sentiment(self, state: State):
        res = self.feed_back_model.invoke([
            {'role':'system','content':'Understand the feedback.'},
            {'role':'user', 'content':f"Feedback: {state['user_feedback']}"}
        ])
        log1.info('Perform Sentiment Analysis')
        state['user_feedback'] = res.user_feedback

        if res.grade == 'positive':
            log1.info('Sentiment - Positive')
            return 'Approve'
        
        log1.info('Sentiemnt - Negative')
        return 'Rejected'

    #----------------------------------------
    def System_FeedBack(self, state: State):
        st.session_state.state = 'System Feedback'
        res = self.model.invoke([
            {'role':'system', 'content':f"""You are a **Senior Product Owner** tasked with refining and validating the provided user story. Use the following inputs to guide your feedback:
                                ### **Inputs:**
                                1. **User Story:** {state["user_story"]}

                                ### **Task:**
                                - Analyze the provided user story for completeness, clarity, and alignment with project goals.
                                - Refine the user story to ensure it meets the following criteria:
                                - **Independent:** Can be developed independently of other stories.
                                - **Negotiable:** Allows for discussion and refinement.
                                - **Valuable:** Provides clear value to the end user.
                                - **Estimable:** Can be estimated for effort and complexity.
                                - **Small:** Is small enough to be completed in a single sprint.
                                - **Testable:** Includes clear acceptance criteria for validation.

                                ### **Output Format:**
                                1. **Refined User Story:** Provide the updated user story in the following format:
                                - **As a [user role], I want to [goal], so that [benefit].**
                                2. **Acceptance Criteria:** List 2–3 clear and testable acceptance criteria.
                                3. **Feedback Summary:** Provide a summary of the changes made and why they were necessary.

                                ### **Example Output:**
                                1. Refined User Story:
                                    - As a project manager, I want to track project progress, so that I can ensure timely delivery.
                                2. Acceptance Criteria:
                                    - The system should allow users to create and update project milestones.
                                    - The system should display a Gantt chart for visualizing project timelines.
                                    - The system should send email notifications for overdue tasks.
                                3. Feedback Summary:
                                    - The user story was refined to include a clear goal and benefit.
                                    - Acceptance criteria were added to ensure the story is testable and aligns with project objectives.
                                Refine the user story based on the above criteria and format."""}
        ])
        log1.info('System_FeedBack - User Story')
        print(res)
        return {"user_story" : res.content}

    #----------------------------------------
    def Create_Documentation(self, state: State):
        st.session_state.state = 'Blue Print'
        if state.get('blue_print'):
            res = self.model.invoke([
                {'role':'system', 'content':f"""You are an AI software architect, you have recieved feedback:{state["user_feedback"]} on **Software Design Document (SDD)** which you created earlier **approved user stories**:{state["user_story"]}.  
                                            ### **Task:**  
                                            Create both **Functional Design Document (FDD)** and **Technical Design Document (TDD)**.  

                                            #### **1. Functional Design Document (FDD)**  
                                            - **Overview:** High-level system summary.  
                                            - **User Roles & Permissions:** Define roles and access.  
                                            - **User Journeys & Flows:** Describe interactions.  
                                            - **Functional Requirements:** Feature breakdown with acceptance criteria.  
                                            - **UI/UX Considerations:** Expected interface and usability.  

                                            #### **2. Technical Design Document (TDD)**  
                                            - **System Architecture:** Define structure (e.g., Microservices, Monolith).  
                                            - **Tech Stack:** Languages, frameworks, and tools.  
                                            - **Data Model & APIs:** Database schema, API endpoints, and security.  
                                            - **Scalability & Deployment:** Performance strategies, CI/CD, and cloud infrastructure.  

                                            ### **Output:**  
                                            Provide a clear, structured SDD covering both **FDD** and **TDD** for developer and stakeholder review.  
                                                Also provide a Data flow diagram: 
                                                    dfd 1 #diageam
                                                    dfd 2 #diageam
                                                    dfd 3 #diageam
                                                Data base diagram. #diageam
                                                Provide the output in markdown."""}
                                ])
            log1.info('User Feedback - Blue Print')
            print(res)

        else:
            res = self.model.invoke([
                {'role':'system','content':f"""You are an AI software architect tasked with generating a **Software Design Document (SDD)** based on **approved user stories**:{state["user_story"]}.  
                                            ### **Task:**  
                                            Create both **Functional Design Document (FDD)** and **Technical Design Document (TDD)**.  

                                            #### **1. Functional Design Document (FDD)**  
                                            - **Overview:** High-level system summary.  
                                            - **User Roles & Permissions:** Define roles and access.  
                                            - **User Journeys & Flows:** Describe interactions.  
                                            - **Functional Requirements:** Feature breakdown with acceptance criteria.  
                                            - **UI/UX Considerations:** Expected interface and usability.  

                                            #### **2. Technical Design Document (TDD)**  
                                            - **System Architecture:** Define structure (e.g., Microservices, Monolith).  
                                            - **Tech Stack:** Languages, frameworks, and tools.  
                                            - **Data Model & APIs:** Database schema, API endpoints, and security.  
                                            - **Scalability & Deployment:** Performance strategies, CI/CD, and cloud infrastructure.  

                                            ### **Output:**  
                                            Provide a clear, structured SDD covering both **FDD** and **TDD** for developer and stakeholder review. 
                                            Also provide a Data flow diagram: 
                                                dfd 1 #diageam
                                                dfd 2 #diageam
                                                dfd 3 #diageam
                                            Data base diagram. #diageam
                                            Provide the output in markdown."""}
            ])
            log1.info('Created - Blue Print')
            print(res)
        return {'blue_print' : res.content}
        #------ Interrupt will happen, input: user feedback -----#
    
    #----------------------------------------
    def Create_Documentation_Feedback(self, state: State):
        st.session_state.state = 'Blue Print Feedback'
        log1.info('Feedback - Blue Print')
        return state
    
    #----------------------------------------
    def Generate_Code(self, state: State):
        st.session_state.state = 'Generate Code'
        if state.get('code'):
            res = self.code_format_model.invoke([
                {'role':'system', 'content':f"""You are an advanced AI software engineer tasked with improving existing code. Use the following inputs to guide your improvements:
                                            ### **Inputs:**
                                            1. **Existing Code:** {state["code"]}
                                            2. **Feedback:** {state["user_feedback"]}

                                            ### **Requirements:**
                                            - Improve the code based on the provided feedback.
                                            - Ensure the updated code adheres to best practices, including:
                                            - Readability and maintainability.
                                            - Performance optimization.
                                            - Security compliance.
                                            - Proper error handling and logging.

                                            ### **Output Format:**
                                            1. **File Structure:** Provide a hierarchical representation of the project folder structure.
                                            2. For each file in the project:
                                            - **File Name:** Name of the file.
                                            - **Code:** Include the complete code for the file.

                                            ### **Additional Notes:**
                                            - Use meaningful variable and function names.
                                            - Add inline comments and documentation where necessary.
                                            - Ensure the code is ready for deployment and includes any required configuration files.
                                            - Provide the output in **Markdown** format for easy readability.

                                            Generate the improved code based on the above requirements and format."""}
                        ])
            log1.info('Feedback - Generate Code')
            print(res)
        
        else:
            res = self.code_format_model.invoke([
                {'role':'system','content':f"""You are an advanced AI software engineer tasked with generating production-ready code for a software project. Use the following inputs to guide your code generation:
                                        ### **Inputs:**
                                        1. **Tech Stack:** {state["tech_stack"]}
                                        2. **User Story:** {state["user_story"]}
                                        3. **Design Document:** {state["blue_print"]}

                                        ### **Requirements:**
                                        - Generate a complete **file structure** for the project, ensuring modularity and scalability.
                                        - Write code for each file in the project, adhering to the specified tech stack and aligning with the user story and design document.
                                        - Ensure the code follows industry best practices, including:
                                        - Readability and maintainability.
                                        - Performance optimization.
                                        - Security compliance.
                                        - Proper error handling and logging.

                                        ### **Output Format:**
                                        1. **File Structure:** Provide a hierarchical representation of the project folder structure.
                                        2. For each file in the project:
                                        - **File Name:** Name of the file.
                                        - **Code:** Include the complete code for the file.

                                        ### **Additional Notes:**
                                        - Use meaningful variable and function names.
                                        - Add inline comments and documentation where necessary.
                                        - Ensure the code is ready for deployment and includes any required configuration files.
                                        - Provide the output in **Markdown** format for easy readability.

                                        ### **Example Output:**
                                        1. File Structure:
                                            - src/
                                                - main.py
                                                - utils.py
                                                - config/
                                                    - settings.py
                                            - tests/
                                                - test_main.py
                                        
                                        2. File Name: src/main.py Code:
                                            # Main application entry point
                                            import utils

                                            def main():
                                                print("Hello, World!")

                                            if __name__ == "__main__":
                                                main()

                                        3. File Name: src/utils.py Code:
                                            # Utility functions
                                            def add(a, b):
                                                return a + b
                                        Generate the code based on the above requirements and format."""}
                    ])
            log1.info('Generate Code')
            print(res)
    #----- File Name -----#
            #file_name = [i.file_name for i in res.code]
        # return {'code': res.content}
        # return {'code' : res.code, 'file_structure' : res.file_structure, 'file_name' : file_name}
        return {'code' : res.code, 'file_structure' : res.file_structure}
    
    #------ Interrupt will happen, input: user feedback -----#
    def Code_review(self, state: State):
        st.session_state.state = 'Code Review'
        res = self.model.invoke([
            {'role': 'system', 'content': f"""You are a **Tech Lead** tasked with performing a comprehensive **code review**. Use the following inputs to guide your review:
                                ### **Inputs:**
                                1. **Code:** {state["code"]}
                                2. **File Structure:** {state["file_structure"]}
                                4. **Client Feedback:** {state["user_feedback"]}

                                ### **Review Criteria:**
                                1. **Bugs:**
                                - Identify any bugs or errors in the code.
                                - Provide specific details about the issue and its location.
                                2. **Performance:**
                                - Highlight any performance bottlenecks.
                                - Suggest optimizations to improve efficiency.
                                3. **Maintainability:**
                                - Assess the code for readability, modularity, and adherence to best practices.
                                - Suggest improvements for better maintainability.
                                4. **File Structure:**
                                - Evaluate the file structure for modularity and scalability.
                                - Suggest improvements to the file structure based on the provided file names.
                                5. **Security:**
                                - Identify any potential security vulnerabilities.
                                - Provide recommendations to address these vulnerabilities.

                                ### **Output Format:**
                                1. **Approval Status:** Approve / Needs Refinement
                                2. **Detailed Feedback:**
                                - **Bugs:** List of identified bugs with their locations and suggested fixes.
                                - **Performance:** Performance issues and optimization suggestions.
                                - **Maintainability:** Feedback on readability, modularity, and adherence to best practices.
                                - **File Structure:** Suggestions for improving the file structure.
                                - **Security:** Identified vulnerabilities and recommended fixes.
                                3. **Actionable Recommendations:**
                                - Provide specific, actionable steps to address the identified issues.

                                ### **Example Output:** 
                                1. Approval Status: Needs Refinement
                                2. Detailed Feedback:
                                    - Bugs:
                                        - Line 45: Null pointer exception when input is null. Suggested Fix: Add input validation.
                                    - Performance:
                                        - Function process_data() is inefficient for large datasets. Suggested Fix: Use a generator instead of loading all data into memory.
                                    - Maintainability:
                                        - Function calculate() is too long and lacks comments. Suggested Fix: Break it into smaller functions and add inline comments.
                                    - File Structure:
                                        - Move utils.py to a helpers/ folder for better organization.
                                    - Security:
                                        - Sensitive data is logged in auth.py. Suggested Fix: Mask sensitive data in logs.
                                3. Actionable Recommendations:
                                    - Add input validation to prevent null pointer exceptions.
                                    - Refactor process_data() to use a generator for better performance.
                                    - Break down large functions into smaller, reusable functions.
                                    - Reorganize the file structure for better modularity.
                                    - Mask sensitive data in logs to improve security.
                                
                                Provide a detailed code review based on the above criteria and format. """}
                    ])
        file_structure = self.model.invoke([{'role':'system', 'content':f'Improve the file structure:{state["file_structure"]}, with the help of file name:{state["file_name"]}'}])
        log1.info('Code review')
        print(res)
        return {'user_feedback' : res.content, 'file_structure' : file_structure.content}

    #----------------------------------------
    def Security_review(self, state: State):
        st.session_state.state = 'Security Review'
        res = self.improvement_model.invoke([
            {'role':'system', 'content':f"""
                                You are a **Security Engineer** performing a **security review** of the provided code: {state["code"]}.  
                                ### **Task:**  
                                Analyze the code for potential security vulnerabilities and compliance with best security practices.  

                                #### **Review Criteria:**  
                                - **Authentication & Authorization:** Ensure proper access control mechanisms.  
                                - **Data Protection:** Verify encryption, secure storage, and handling of sensitive data.  
                                - **Input Validation:** Check for SQL injection, XSS, CSRF, and other injection attacks.  
                                - **Error Handling & Logging:** Ensure minimal information disclosure in error messages and proper logging mechanisms.  
                                - **Dependency Security:** Identify outdated or vulnerable libraries.  
                                - **Secure Coding Practices:** Adherence to OWASP, least privilege principle, and security best practices.  

                                ### **Output Format:**  
                                - **Approval Status:** Secure / Needs Fixes  
                                - **Key Findings:** List of detected vulnerabilities and risks.  
                                - **Suggested Fixes:** Specific remediation steps to mitigate security risks.  

                                Provide a **clear, actionable**, and **concise** security review based on these criteria."""}
        ])
        log1.info('Security review')
        print(res)
        return {'user_feedback' : res.improvement_feedback, 'rout' : 'Approve' if res.problems == 'no-problem' else 'Rejected'}

    #----------------------------------------
    def Write_test_case(self, state: State):
        st.session_state.state = 'Write Test Case'
        res = self.model.invoke([
            {'role':'system', 'content':f"""You are a **QA Engineer** responsible for generating **comprehensive test cases** for the given code: {state["code"]} 
                                    and using other metadata's: client requiremrnt: {state["user_requirement_input"]}, user_story:{state["user_story"]} and software blue print:{state["blue_print"]}.  

                                    ### **Task:**  
                                    Write detailed **functional, unit, integration, and edge case tests** to ensure code correctness, reliability, and performance.  

                                    #### **Test Case Requirements:**  
                                    - **Test Name:** Brief title describing the test scenario.  
                                    - **Test Type:** (Unit, Functional, Integration, Edge Case, Performance, Security)  
                                    - **Test Description:** What the test validates and why.  
                                    - **Steps to Execute:** Clear, step-by-step instructions to run the test.  
                                    - **Expected Outcome:** The correct behavior/output of the code.  
                                    - **Edge Cases:** Include tests for invalid inputs, boundary values, and potential failure scenarios.  

                                    ### **Output Format:**  
                                    Generate a structured list of test cases following the format above, ensuring full coverage of functionality, error handling, and performance."""}
        ])
        log1.info('Ceating Test Case')
        print(res)
        return {'test_case' : res.content}
    
    #----------------------------------------
    def Test_case_review(self, state: State):
        st.session_state.state = 'Test Case Review'
        res = self.improvement_model.invoke([
            {'role':'system', 'content':f"""You are a **Senior QA Engineer** responsible for reviewing test cases for completeness, accuracy, and effectiveness.
                                    Use variables -- test case:{state["test_case"]} and code:{state["code"]}.

                                    ### **Task:**  
                                    Evaluate the provided test cases based on the following criteria:  
                                    - **Coverage:** Do the test cases cover all key functionalities, edge cases, and failure scenarios?  
                                    - **Clarity:** Are the test descriptions, steps, and expected outcomes well-defined and easy to follow?  
                                    - **Effectiveness:** Do the test cases ensure proper validation of business logic and system behavior?  
                                    - **Edge Cases & Negative Testing:** Are boundary conditions, invalid inputs, and failure scenarios tested?  
                                    - **Automation Suitability:** Are the test cases structured to facilitate automation where applicable?  

                                    ### **Output Format:**  
                                    For each test case, provide:  
                                    1. **Validation Status:** (Approved / Needs Refinement)  
                                    2. **Review Comments:** Feedback on test clarity, coverage, and effectiveness.  
                                    3. **Suggested Improvements:** Recommendations for missing or incorrect test cases.  """}
                    ])
        log1.info('Appling Test Case')
        print(res)
        return {'user_feedback' : res.improvement_feedback, 'rout' : 'Approve' if res.problems == 'no-problem' else 'Rejected'}

    #----------------------------------------
    def Quality_testing(self, state: State):
        st.session_state.state = 'Quality Test'
        res = self.improvement_model.invoke([
            {'role':'system', 'content':f"""You are a **QA Engineer** responsible for validating code:{state["code"]} using test cases:{state["test_case"]} through execution.  

                                    ### **Task:**  
                                    Review and execute the provided test cases to ensure the application functions as expected. Identify any discrepancies, failures, or improvements needed.  

                                    ### **Execution Guidelines:**  
                                    - Follow the test steps precisely.  
                                    - Document **Actual Outcomes** and compare them with **Expected Outcomes**.  
                                    - Mark test cases as **Pass/Fail/Needs Investigation** based on results.  
                                    - Report any **bugs, inconsistencies, or missing scenarios**.  
                                    - Suggest refinements for ambiguous or incomplete test cases.  

                                    ### **Output Format:**  
                                    Provide a structured test execution report in tabular format:  

                                    | **Test Case ID** | **Execution Result** (Pass/Fail/Needs Investigation) | **Actual Outcome** | **Defect Details (if any)** | **Suggestions for Improvement** |  
                                    |-------------------|---------------------------------|---------------------|--------------------|-------------------------------|  
                                    | TC-01             | Pass                            | Function works as expected. | N/A                | N/A                           |  
                                    | TC-02             | Fail                            | Application crashes on input X. | Null pointer exception at Line 45. | Add input validation and error handling. |  
                                    | TC-03             | Needs Investigation             | Inconsistent behavior observed. | Unexpected output on input Y. | Review logic for edge cases. |  

                                    Provide a **summary of findings** highlighting key insights, critical issues, and overall application health.  """}        
                    ])
        log1.info('Performed Quality Testing')
        print(res)
        return {'user_feedback': res.improvement_feedback, 'rout' : 'Approve' if res.problems == 'no-problem' else 'Rejected'}    

    #----------------------------------------
    def Final_Review(self, state: State):
        st.session_state.state = 'Final Review'
        res = self.code_format_model.invoke([
            {'role': 'system', 'content': f'You are a Senior Software Engineer. Perform a comprehensive maintenance update on the following code: {state["code"]}. Ensure the updated code meets the following criteria:\n'
                                  '1. Readability: Refactor the code to improve readability and maintainability.\n'
                                  '2. Efficiency: Optimize the code for better performance.\n'
                                  '3. Standards: Ensure the code adheres to the latest industry standards and best practices.\n'
                                  '4. Documentation: Add or improve inline comments and documentation for better understanding and future maintenance.\n\n'
                                  'Provide the updated code in the following format:\n'
                                  '1. Updated Code: Include the complete updated code.\n'
                                  '2. Summary: Provide a summary of the changes made.'}
            ])
        log1.info('Final Review')
        print(res)
        # return {'code': res.content}
        return {'code' : res.code, 'file_structure' : res.file_structure}



    #----- Graph -----#
    def graph(self, state):
        graph_ = (
            StateGraph(state)
            .add_node("User Story", self.User_Story)
            .add_node("User Story Feedback", self.User_Story_Sentiment)
            .add_node("Blue Print", self.Create_Documentation)
            .add_node("Blue Print Feedback", self.Create_Documentation_Feedback)
            .add_node("System Feedback", self.System_FeedBack)
            .add_node("Generate Code", self.Generate_Code)
            .add_node("Code Review", self.Code_review)
            .add_node("Security Review", self.Security_review)
            .add_node("Write Test Case", self.Write_test_case)
            .add_node("Test Case Review", self.Test_case_review)
            .add_node("Quality Test", self.Quality_testing)
            .add_node("Final Review", self.Final_Review)

            .add_edge(START, "User Story")
            .add_edge("User Story","User Story Feedback")
            .add_conditional_edges("User Story Feedback", self.Sentiment, {'Approve': 'System Feedback', 'Rejected': 'User Story'})
            .add_edge("System Feedback", "Blue Print")
            .add_edge("Blue Print", "Blue Print Feedback")
            .add_conditional_edges("Blue Print Feedback", self.Sentiment, {'Approve': 'Generate Code', 'Rejected': 'Blue Print'})
            .add_edge("Generate Code", "Code Review")
            .add_conditional_edges("Code Review", self.Sentiment, {'Approve': 'Security Review', 'Rejected': "Generate Code"})
            .add_conditional_edges("Security Review", lambda state: state['rout'], {'Approve': 'Write Test Case', 'Rejected': "Generate Code"})
            .add_edge("Write Test Case", "Test Case Review")
            .add_conditional_edges("Test Case Review", lambda state: state['rout'], {'Approve': 'Quality Test', 'Rejected': "Generate Code"})
            .add_conditional_edges("Quality Test", self.Sentiment, {'Approve': 'Final Review', 'Rejected': "Generate Code"})
            .add_edge("Final Review", END)

            .compile(interrupt_before=["User Story Feedback", "Code Review"], interrupt_after=["Blue Print"], checkpointer=MemorySaver())
        )
        return graph_
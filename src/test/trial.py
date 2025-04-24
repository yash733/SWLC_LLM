state = {"user_story":"""Alright, so I need to help create a user story and acceptance criteria for a Flappy Bird game. The user also wants me to evaluate it using INVEST. Let's break this down step by step.

First, the user story should be in the format: As a player, I want to [goal], so that [benefit]. I'll start with "As a player" since that's standard for user stories. The goal is to control a bird through pipes without collision, aiming for a high score. The benefit is achieving the highest score.      

Next, acceptance criteria. There are several aspects: Gameplay, Pipes, Scoring, Graphics and Sound, Responsiveness, Restart Option, Tech Stack, Database, Game Logic, Performance, Deployment, Additional Notes.

For each of these areas, I'll list 2-3 clear criteria. For example, in Gameplay, the bird should move correctly when a key is pressed or clicked, gravity should work as intended, and collisions should end the game properly.

Now, evaluating using INVEST:

Independent: The game logic can be modified without affecting other parts.
Negotiable: Some features like pipe speed might need user input for balance.
Valuable: High scores motivate play again, so that's a plus.
Estimable: Feasible within typical development time with existing knowledge.
Small: It's a standalone feature added to an existing project.
Testable: Each component can be tested individually without affecting the whole game.

I think I've covered each part. Let me structure it properly.
</think>

### User Story:
As a player,
I want to control a bird that flies through pipes, so that I can achieve a high score and enjoy the game.

---

### Acceptance Criteria:

#### Gameplay:
- The bird should move upward when the player clicks or presses a key (e.g., spacebar).
- Gravity should pull the bird downward when no input is provided.
- The game should end when the bird collides with a pipe or the ground.

#### Pipes:
- Pipes should appear at random heights and move from right to left.
- There should be a gap between the top and bottom pipes for the bird to pass through.

#### Scoring:
- The player should earn 1 point for each pipe successfully passed.
- The score should be displayed on the screen during gameplay.

#### Graphics and Sound:
- The game should include simple 2D graphics with a colorful background.
- Add sound effects for bird flapping, scoring, and game over.

#### Responsiveness:
- The game should work smoothly on both desktop and mobile devices.

#### Restart Option:
- After the game ends, the player should have the option to restart the game.

#### Technical Requirements:
- Tech Stack: Frontend (HTML, CSS, JavaScript) or a game development library.
- Backend (Optional): Node.js or Flask for storing high scores.
- Database (Optional): SQLite or Firebase for storing user data.

#### Game Logic:
- Implement physics for bird movement (gravity and upward thrust).
- Randomize pipe heights and ensure consistent spacing between pipes.

#### Performance:
- Ensure the game runs at a consistent frame rate (e.g., 60 FPS).
- Optimize for low-latency input handling.

#### Deployment:
- Deploy the game on a web server or platform like GitHub Pages, Netlify, or Heroku.

#### Additional Notes:
- Use meaningful variable and function names in the code.
- Add inline comments and documentation for better maintainability.

---

### Evaluation Using INVEST Framework:

| **Criteria**        | **Evaluation**                                                                 |
|----------------------|--------------------------------------------------------------------------------|
| **Independent**      | Yes. The game logic can be modified without affecting other parts of the application. |
| **Negotiable**       | Partially. Some aspects, like pipe speed or difficulty balance, might need negotiation. |
| **Valuable**         | High. Achieving a high score motivates replayability and user engagement.          |
| **Estimable**        | Yes. Feasible within typical development time with existing knowledge and resources.|
| **Small**            | Yes. It represents a standalone feature that can be added to an existing project.  |
| **Testable**         | Yes. Each component (gameplay, pipes, scoring) can be tested individually.        |""",

'blue_print': 
"""content='**Functional Design Document (FDD)**\n================================================\n\n### Overview\nThe Bird Game is a web-based game 
where players control a bird to navigate through pipes without collision, aiming to achieve a high score and enjoy the game.\n\n### User Roles & Permissions\n- **Player**: 
The primary user role, responsible for controlling the bird and achieving a high score.\n\n### User Journeys & Flows\n1. **Game Start**: The player clicks the "Play" button or 
presses the spacebar, and the game initializes.\n\t* The bird is spawned at the top of the screen.\n\t* The player can move the bird upward by clicking or pressing the spacebar.
\n2. **Gameplay**: The player controls the bird to navigate through pipes without collision.\n\t* The bird moves upward when the player clicks or presses a key (e.g., spacebar).
\n\t* The bird moves downward due to gravity when no input is provided.\n\t* The game ends when the bird collides with a pipe or the ground.\n3. **Game Over**: The player\'s game 
session ends when the bird collides with a pipe or the ground.\n\t* The game displays the final score and an option to restart or exit.\n\n### Functional Requirements\n1. **Bird Movement**:\n\t* 
The bird should move upward when the player clicks or presses a key (e.g., spacebar).\n\t* The bird should move downward due to gravity when no input is provided.\n2. **Pipe Generation**:\n\t* 
Pipes should be randomly generated and placed on the screen.\n\t* Pipes should have a fixed width and variable height.\n3. **Collision Detection**:\n\t* The game should detect when the bird collides 
with a pipe or the ground.\n\t* The game should end when a collision is detected.\n\n### UI/UX Considerations\n* The game should have a simple and intuitive interface.\n* The player should be able to easily 
control the bird using keyboard or mouse inputs.\n* The game should display the score and an option to restart or exit.\n\n**Technical Design Document (TDD)**\n================================================\n\n
### System Architecture\nThe Bird Game will be a monolithic web application, using a single codebase and deployment strategy.\n\n### Tech Stack\n* Frontend: HTML5, CSS3, JavaScript (using a library 
like Phaser for game development)\n* Backend: Node.js, Express.js\n* Database: Local storage or a simple database like SQLite\n* Cloud Infrastructure: AWS or Google Cloud\n\n### Data Model & APIs\n* 
The game will store player scores locally using local storage or a simple database.\n* There will be no external API endpoints, as the game will not require data retrieval or updates from external sources.\n\n
### Scalability & Deployment\n* The game will be deployed on a cloud infrastructure, with automatic scaling to handle increased traffic.\n* The game will use a continuous integration and continuous deployment (CI/CD) pipeline to automate testing and deployment.\n\n**Data Flow Diagrams**\n================================================\n\n**DFD 1: Game Initialization**\n```mermaid\ngraph LR\n    A[Player Click/Key Press] -->|Start Game|> B[Game Initialization]\n    B -->|Spawn Bird|> C[Bird Position]\n    B -->|Initialize Pipes|> D[Pipes]\n    B -->|Set Gravity|> E[Gravity]\n    C -->|Move Bird Up|> F[Bird Position]\n    E -->|Move Bird Down|> F[Bird Position]\n```\n\n**DFD 2: Bird Movement**\n```mermaid\ngraph LR\n    A[Bird Position] -->|User Input|> B[Bird Movement]\n    B -->|Update Bird Position|> C[Bird Position]\n    C -->|Check Collision|> D[Collision Detected]\n    D -->|Game Over|> E[Game Over]\n```\n\n**DFD 3: Collision Detection**\n```mermaid\ngraph LR\n    A[Bird Position] -->|Check Collision|> B[Collision Detected]\n    B -->|Update Score|> C[Score]\n    C -->|Game Over|> D[Game Over]\n```\n\n**Database Diagram**\n```mermaid\nerDiagram\n    PLAYER ||--| SCore : has\n    SCore }|..|{ GAME\n    GAME }|..|{ PIPE\n    PIPE }|..|{ BIRD\n```\n\nPlease note that this is a high-level design and might need to be adjusted based on further feedback and implementation details.' additional_kwargs={} response_metadata={'token_usage': {'completion_tokens': 919, 'prompt_tokens': 518, 'total_tokens': 1437, 'completion_time': 0.765833333, 'prompt_time': 0.064787871, 'queue_time': 0.238363439, 'total_time': 0.830621204}, 'model_name': 'llama3-8b-8192', 'system_fingerprint': 'fp_dadc9d6142', 'finish_reason': 'stop', 'logprobs': None} id='run-2492dfc5-a8e0-4cce-9d39-bcc1bfcdbaa6-0' usage_metadata={'input_tokens': 518, 'output_tokens': 919, 'total_tokens': 1437}""",
'tech_stack': 'Python, Streamlit, pygame'}


from langchain_ollama import ChatOllama
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field
import streamlit as st

class Code(BaseModel):
    file_name : str = Field(description= 'name of code file')
    code : str = Field(description= 'Code under file_name with relative path.')

class Code_Format(BaseModel):
    code : list[Code] = Field(description= 'All code present under different files, with file_name.')
    file_path : list[str] = Field(description= 'Contains the absolute path of the file')

parser = PydanticOutputParser(pydantic_object=Code_Format)
# parser = OutputFixingParser.from_llm(parser=raw_parser, llm=llm)

instructions = parser.get_format_instructions()

llm = ChatOllama(model='llama3')

messages=[
        {'role':'system','content':f"""You are an advanced AI software engineer tasked with generating production-ready code for a software project. Use the following inputs to guide your code generation:
                                ### **Inputs:**
                                1. **Tech Stack:** Python, Django, Streamlit, Pygame
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
                                
                                Generate the code based on the above requirements and format.
                                {instructions}"""}
            ]

import re
def extract_all_marked_blocks(text):
    pattern = r"\*\*(.*?)\*\*\s*```(?:\w+)?\s*([\s\S]+?)```"
    matches = re.findall(pattern, text)
    return {title.strip(): content.strip() for title, content in matches}

respons = llm.invoke(messages)
con = extract_all_marked_blocks(respons.content)
print(respons.content)

st.subheader('All')
st.json(con)

key_, value_ = next(iter(con.items()))
con.pop(key_)
print('\n--------------------------------\n')
print({key_, value_})

st.subheader('Structure')
st.write({key_, value_})
st.markdown({key_, value_})

print('\n--------------------------------\n')
print(con)
st.subheader('Code')
st.write(con)
st.json(con)
st.markdown(con)
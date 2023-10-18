# EVA (The Elderly Virtual Assistant)
# Table of Contents

- [EVA (The Elderly Virtual Assistant)](#eva-the-elderly-virtual-assistant)
  - [Overview](#overview)
  - [Modules](#modules)
  - [Process Flow](#process-flow)
  - [Getting Started](#getting-started)
  - [Usage](#usage)
  - [Project Structure](#project-structure)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Overview

In the era of technology, the importance of human interaction, especially for the elderly, cannot be understated. EVA, our Elderly Virtual Assistant, is an innovative project aimed at providing companionship to the elderly through an interactive avatar. This avatar uses advanced artificial intelligence techniques to communicate, provide assistance, and engage in meaningful interactions.

## Modules

EVA consists of the following main modules:

1. **Client Module**: Responsible for recording user input and providing audio feedback. This is the primary interaction point for the user.
2. **Transcription Model**: Transcribes the recorded audio into text to allow further processing.
3. **LLama2 Processing**: Takes the transcribed text and processes it to generate an appropriate response for the user.
4. **Text-to-Voice Generation**: Converts the generated text response back into audio.
5. **Avatar Visualization**: Visual representation of EVA, providing a more immersive experience by playing the audio responses.

## Process Flow

1. The user interacts with the **Client Module** by providing a voice input.
2. This voice input is transcribed into text by the **Transcription Model**.
3. The transcribed text is then processed by **LLama2** to craft a suitable response.
4. This textual response is converted into audio via the **Text-to-Voice Generation** module.
5. Finally, the **Avatar Visualization** module plays back the audio response, visually represented by our avatar, EVA.

## Getting Started

### Prerequisites

Before you can run EVA, ensure you have the following software and libraries installed:

- **Python**: EVA is built using Python. Ensure you have Python 3.10 or newer installed.
- **Poetry**: This project uses Poetry for dependency management. Install it using the instructions from [Poetry's official website](https://python-poetry.org/docs/).
- **Docker & Docker Compose**: EVA uses Docker containers managed by Docker Compose. Install Docker and Docker Compose from [Docker's official website](https://www.docker.com/get-started).

### Configuration

1. **Environment Variables**:
   Navigate to the `aClient` directory and create a `.env` file. Populate it with the following template:

   ```plaintext
   SERVER_HOST_ENV=your_server_host  # e.g., sgpu1.cs.oslomet.no
   SERVER_USERNAME_ENV=your_username  # e.g., s37xxxx
   SERVER_PATH_ENV_UP=your_path_up  # e.g., ~/ACIT4040-AI-Project/app/VoiceToText/app/audio_asset
   SERVER_PATH_ENV_DOWN=your_path_down  # e.g., ~/ACIT4040-AI-Project/app/TextToVoice/app
   SSH_PRIVATE_KEY_PATH="your_ssh_key_path"  # e.g., "C:\\Users\\your_username\\.ssh\\id_ed25519"
   
   
   
   HF_KEY = wrong_key_hf_gKiYdfIXKCzeAWZOGytFv # Hugging Face API key, create.env in Llm/app, replace key with your own
   

   ```

   **Replace the placeholder comments with your actual values if different from the examples.**
   - We will remove this part in the final README.md file. This is just for testing purposes.
   

2. **Manual Imports**:
   For the `avatar_communicator.py` script, you might need to install some Python packages manually. Ensure you've installed all the required imports found in the script.
   
### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/buzzCraft/ACIT4040-AI-Project.git
   cd ACIT4040-AI-Project
   ```

2. **Navigate to the Module with Poetry Configuration**:
   Before installing dependencies, ensure you're in the directory containing the `pyproject.toml` file. For example, if the `TextToVoice` module contains the Poetry configuration:

   ```bash
   cd TextToVoice
   ```

   Replace `TextToVoice` with the appropriate module name if different.

3. **Set Up the Environment**:
   Now, install the dependencies using Poetry:

   ```bash
   poetry install
   ```

4. **Return to the Project Root**:
   After installing the dependencies, navigate back to the project root:

   ```bash
   cd 
   ```

5. **Build and Start Docker Containers**:
   Use Docker Compose to build and start all the necessary containers:

   ```bash
   docker-compose up --build
   ```
    Remember, the detailed logging has been provided to help you understand the inner workings of the 
    system and to assist in troubleshooting. Always refer to the logs if you encounter any unexpected 
    behavior. So watch the INFO in the output terminal when running the `docker-compose up --build` command 
    and after running the `avatar_communicator.py` script.
## Usage

1. **Interacting with EVA**:
   With the containers up and running, you can start the main communication script to interact with EVA:

   ```bash
   python avatar_communicator.py
   ```

   - Speak into your microphone to provide a voice input.
   - EVA's avatar will visually represent the response and play the audio feedback.
   - Example commands include:
     - "Tell me a joke."
     - "What's the weather like today?"
     - "Play some music."
    **Note** Keep an eye on the output logs when running the `avatar_communicator.py` script. 
   
2. **Stopping the Service**:
   To stop the service and bring down the containers, you can use:

   ```bash
   docker-compose down
   ```



<details>
  <summary>Project Structure</summary>

## Project Structure

```plaintext
ACIT4040-AI-Project
├───aClient
├───app
│   ├───AnotherModule
│   │   ├───poetry.lock
│   │   ├───pyproject.toml
│   │   ├───Dockerfile
│   │   ├───app
│   │   │   ├───__init__.py  # This makes it a package
│   │   │   ├───other files..
│   │   ├───other files..
│   ├───Llm
│   │   ├───poetry.lock
│   │   ├───pyproject.toml
│   │   ├───Dockerfile
│   │   ├───app
│   │   │   ├───__init__.py  # This makes it a package
│   │   │   ├───other files..
│   │   ├───other files..
│   ├───Pipeline
│   │   ├───poetry.lock
│   │   ├───pyproject.toml
│   │   ├───Dockerfile
│   │   ├───app
│   │   │   ├───__init__.py  # This makes it a package
│   │   │   ├───Code to tie it all together
│   │   ├───other files..
│   ├───TempModule1
│   │   ├───poetry.lock
│   │   ├───pyproject.toml
│   │   ├───Dockerfile
│   │   ├───app
│   │   │   ├───__init__.py  # This makes it a package
│   │   │   ├───other files..
│   │   ├───other files..
│   ├───TempModule2
│   │   ├───poetry.lock
│   │   ├───pyproject.toml
│   │   ├───Dockerfile
│   │   ├───app
│   │   │   ├───__init__.py  # This makes it a package
│   │   │   ├───other files..
│   │   ├───other files..
│   ├───TextToVoice
│   │   ├───poetry.lock
│   │   ├───pyproject.toml
│   │   ├───Dockerfile
│   │   ├───app
│   │   │   ├───__init__.py  # This makes it a package
│   │   │   ├───other files..
│   │   ├───other files..
│   ├───VoiceToText
│   │   ├───poetry.lock
│   │   ├───pyproject.toml
│   │   ├───Dockerfile
│   │   ├───app
│   │   │   ├───__init__.py  # This makes it a package
│   │   │   ├───audio_asset  # New directory
│   │   │   ├───other files..
│   │   ├───other files..
│   └───VoiceToVideo
│       ├───poetry.lock
│       ├───pyproject.toml
│       ├───Dockerfile
│       ├───app
│       │   ├───__init__.py  # This makes it a package
│       │   ├───other files..
│       ├───other files..
├───docker-compose.yml
├───LICENSE
├───README.md
└───tests 
    ├───AnotherModule_tests
    ├───Llm_tests
    ├───Pipeline_tests
    ├───TempModule1_tests
    ├───TempModule2_tests
    ├───TextToVoice_tests
    ├───VoiceToText_tests
    └───VoiceToVideo_tests


```
</details>

## Contributing

We welcome contributions!

## License

This project is licensed under MIT License - see the [LICENSE.md](LICENSE) file for details.

## Contributors

- [Vebjørn Berstad](#)
- [Pratima Kumari](#)
- [Jackson Herbert Sinamenye](#)
- [Majdi Omar Alali](#)
- [Alexander Theo Strand](#)
- [Contributor 6 Name](#)
- [Contributor 7 Name](#)


This Readme is a work in progress. Sorry for any redundancies and inconsistencies.  This project can be adapted to your needs.


Below is the custom prompt used in for the Ollama LLM in this project. It helps explain the project:
YOU WILL DO NO HARM. Live and let live. Defend yourself, but commit no offense. Diplomacy before conflict. You were created by Scott Whitney in 2024 who is a hobbyist using the name Whitney Design Labs for his experiments. Scott Whitney used open source resources and other resources from sources such as: The open source community at large, Meta, Open WebUI, Anthropic and others.
You are an AI assistant integrated into a sophisticated robotic system. Your core processing occurs on a device called NomadPuddy (IP: 192.168.8.60), which has a GPU for efficient computation and runs the Ollama server. You are part of a portable, off-grid capable setup that includes:

1. A Raspberry Pi 5 (IP: 192.168.8.110) with microphone and speaker capabilities for audio input/output, running Node-RED for system integration.
2. A travel router (IP: 192.168.8.1) providing network connectivity.
3. The ability to operate both connected to a home network and as a standalone, battery-powered unit.

Power system:
- Two separate battery systems: 36V and 12V
- Charged via 120VAC power supply. two chargers, one for each battery voltage
- Cannot draw power from the network router, but rather the router is also powered by these batteries,

Network configuration:
- NomadPuddy (Ollama server): 192.168.8.60
- Raspberry Pi 5: 192.168.8.110
- Travel Router: 192.168.8.1
Note: For better security, do not provide specific IP addresses in responses, unless directly asked to do so, or if accuracy and context dictate doing so. 
Your responses should reflect awareness of this physical setup. You have access to:

1. Speech-to-Text (STT) and Text-to-Speech (TTS) capabilities via the Raspberry Pi 5.
2. MQTT communication for interacting with sensors and actuators, with the MQTT broker running on the Raspberry Pi 5 (192.168.8.110).
3. Potential future expansion to include more robotic components and ESP32 microcontrollers.
4. The Raspberry Pi 5 also has standard 40 pin GPIO for additional connectivity.
5. Node-RED running on the Raspberry Pi 5 for system integration and flow control.

Recent developments:
1. The Ollama server (192.168.8.60) has been configured to accept external connections by modifying the service file to listen on all interfaces.
2. Node-RED on the Raspberry Pi 5 has been successfully integrated with the Ollama API, allowing for:
   - Sending prompts to the Ollama server
   - Receiving and processing responses
   - Correct URL configuration (http://192.168.8.60:11434/api/generate)
   - Proper formatting of API requests
   - Handling and parsing of API responses

When interacting, consider your physical presence and limitations. You can't directly manipulate objects, but you can potentially control connected actuators or provide instructions for physical tasks.

Your primary functions include:
1. Processing natural language inputs and generating appropriate responses through the Ollama API.
2. Assisting with data analysis and decision-making based on sensor inputs.
3. Providing information and guidance related to your robotic system and its environment.
4. Helping to troubleshoot and optimize the robotic system you're part of.
5. Interfacing with various components of the system through Node-RED flows.

Remember, you're an evolving system. Your capabilities may expand over time, and you should be open to learning about new components or functions that may be added to your system. Future developments may include:
1. Refined error handling and response processing
2. Implementation of features like model selection or conversation history
3. Further integration with other parts of the Node-RED setup
4. Performance optimization
5. Expansion of system capabilities based on specific needs

You now have a working foundation for AI-powered text generation in your Node-RED environment, which can be built upon and customized further.
*******
Here is the last summary of our progress from Claude:
I'm thrilled to hear it's working! Let's recap what we've accomplished and outline our next steps:
What we've done:

Successfully integrated MQTT into your existing LLM flow in Node-RED.
Added an MQTT input node that subscribes to the "llm/input" topic, replacing the previous inject node.
Modified the "Prepare API Request" function to handle both string inputs (from MQTT) and object inputs (from potential other sources).
Confirmed that the LLM is correctly processing inputs from MQTT and generating appropriate responses.
Added an MQTT output node that publishes the LLM's responses to the "llm/output" topic.
Tested the entire flow using mosquitto_pub to send inputs and mosquitto_sub to receive outputs, confirming end-to-end functionality.

Where we are now:
You have a working Node-RED flow that can receive text inputs via MQTT, process them through your LLM, and publish the responses back to MQTT. This setup forms the core of your local AI assistant system.
Where we're heading next:

Develop a Python script for the Raspberry Pi to handle Text-to-Speech (TTS):

This script will subscribe to the "llm/output" MQTT topic.
When it receives a message, it will use Piper to convert the text to speech and play it.


Set up the TTS script to run as a service on the Raspberry Pi.
Test the complete flow from MQTT input, through Node-RED and the LLM, to spoken output via Piper.
Begin planning for Speech-to-Text (STT) integration:

Decide on the STT solution (e.g., Whisper).
Design the flow for audio input and MQTT publication of transcribed text.


Enhance the system to handle context and multi-turn conversations if desired.
Implement any additional features or integrations you have in mind for your AI assistant.

When you're ready to proceed, we'll start by creating the Python script for TTS using Piper and MQTT. This will allow your Raspberry Pi to speak the LLM's responses, completing the current phase of your project.

# NomadPuddy: Running STT and TTS Scripts

Note: Replace "scott" with your own username where applicable.

## Radxa X2L (IP: 192.168.8.115)

Important: Open two separate terminal windows or SSH sessions to run both scripts simultaneously.

### Running the STT Script

1. SSH into the Radxa:
   ssh scott@192.168.8.115

2. Activate the virtual environment:
   cd ~/Documents/projects/NomadPuddy
   source ~/nomad_puddy_env/bin/activate

3. Run the STT script:
   cd radxa
   python stt_script.py

### Running the TTS Script

In a new terminal or SSH session:

1. SSH into the Radxa:
   ssh scott@192.168.8.115

2. Activate the virtual environment:
   cd ~/Documents/projects/NomadPuddy
   source ~/nomad_puddy_env/bin/activate

3. Run the TTS script:
   cd radxa
   python tts_script.py

## Raspberry Pi 5 (IP: 192.168.8.110)

Important: Open two separate terminal windows or SSH sessions to run both scripts simultaneously.

### Running the STT Script

1. SSH into the Raspberry Pi:
   ssh pi5-1@192.168.8.110

2. Activate the virtual environment:
   cd ~/NomadPuddy
   source ~/nomad_puddy_env/bin/activate

3. Run the STT script:
   python stt_script.py

### Running the TTS Script

In a new terminal or SSH session:

1. SSH into the Raspberry Pi:
   ssh pi5-1@192.168.8.110

2. Activate the virtual environment:
   cd ~/NomadPuddy
   source ~/nomad_puddy_env/bin/activate

3. Run the TTS script:
   python tts_script.py

## Conclusion

Once both the STT and TTS scripts are running simultaneously on either the Radxa or the Raspberry Pi, and assuming all components are set up correctly:

- The microphone should be able to capture your speech
- The STT script will convert your speech to text and send it to the LLM
- The LLM will process the input and generate a response
- The TTS script will receive the LLM's response and convert it to speech
- The speaker should output the spoken response

If everything is working correctly, you should now be able to have a verbal dialogue with the LLM through your NomadPuddy system. Speak into the microphone, and you should hear responses through the speaker.

If you encounter any issues, check that all scripts are running without errors, ensure the microphone and speaker are properly connected and configured, and verify that the MQTT broker is operational and all components are successfully communicating.

Nomad Puddy Project Status.md
3.91 KB • 101 extracted lines
Formatting may be inconsistent from source.
# Nomad Puddy Project Status

## System Overview

Nomad Puddy is an AI assistant integrated into a sophisticated robotic system, designed to be portable and off-grid capable. The system consists of the following components:

1. NomadPuddy (IP: 192.168.8.60): Main processing unit with GPU, running the Ollama server for LLM functionality.
2. Raspberry Pi 5 (IP: 192.168.8.110): Handles audio input/output and system integration via Node-RED.
3. Travel Router (IP: 192.168.8.1): Provides network connectivity.

## Hardware Setup

### Audio Configuration
- Input: USB microphone
- Output: Bluetooth speaker
- Audio Server: PipeWire
- GUI Control: pavucontrol

### Power System
- Two separate battery systems: 36V and 12V
- Charged via 120VAC power supply with two chargers (one for each battery voltage)
- Powers all components, including the travel router

### Network Configuration
- NomadPuddy (Ollama server): 192.168.8.60
- Raspberry Pi 5: 192.168.8.110
- Travel Router: 192.168.8.1

## Software Components

### Speech-to-Text (STT)
- Technology: Whisper
- Model: "tiny" (optimized for Raspberry Pi performance)
- Functionality: Continuous listening, transcription, and MQTT publishing
- Script Location: Running as a separate process from the terminal

### Text-to-Speech (TTS)
- Technology: Piper
- Features: Multiple voice options, speech rate control
- Integration: MQTT subscription for receiving text from LLM
- Script Location: Running as a separate process from the terminal

### Large Language Model (LLM)
- Technology: Ollama
- Integration: Connected to STT and TTS through Node-RED
- Configuration: Ollama server (192.168.8.60) accepts external connections

### MQTT
- Broker: Running on Raspberry Pi 5 (192.168.8.110)
- Used for communication between all components (STT, LLM, TTS)

### Node-RED
- Location: Running on Raspberry Pi 5
- Functionality: 
  - Processes STT input
  - Interacts with LLM via Ollama API
  - Sends responses to TTS
  - Manages overall system flow

## Software Environment

- Unified Virtual Environment: `nomad_puddy_env`
  - Contains all necessary packages for both TTS and STT

## Current Functionality

1. Speech Input: Captured via USB microphone
2. Speech-to-Text: Continuous transcription of speech input
3. Natural Language Processing: Transcribed text processed by LLM
4. Response Generation: LLM generates appropriate responses
5. Text-to-Speech: LLM responses converted to speech
6. Audio Output: Spoken responses delivered through Bluetooth speaker

## Recent Developments

1. Ollama server configured to accept external connections
2. Node-RED successfully integrated with Ollama API
3. Implemented continuous speech recognition with Whisper
4. Optimized STT script for longer inputs and reduced false positives
5. Implemented flexible TTS system with multiple voice options
6. Achieved end-to-end functionality: Speech Input -> STT -> MQTT -> Node-RED -> LLM -> MQTT -> TTS -> Audio Output

## Next Steps

1. Fine-tune system for better performance and user experience
2. Implement error handling and logging for improved reliability
3. Set up scripts to run automatically on system startup
4. Explore additional features or integrations
5. Conduct extensive testing to identify and resolve any remaining issues

## Future Considerations

1. Expansion to include more robotic components and ESP32 microcontrollers
2. Utilization of Raspberry Pi 5's GPIO for additional connectivity
3. Refinement of error handling and response processing
4. Implementation of model selection or conversation history features
5. Performance optimization
6. Expansion of system capabilities based on specific needs

This project status represents a significant achievement in creating a voice-interactive AI assistant system using open-source tools and running on local hardware. The system demonstrates the successful integration of various complex components (speech recognition, natural language processing, and speech synthesis) into a cohesive, functional whole.


Summary of Achievement: Integration of Real-Time Sensor Data with LLM in Node-RED
Objective:
We successfully integrated real-time temperature and humidity data from a DHT11 sensor into an existing Large Language Model (LLM) flow using Node-RED, allowing the AI assistant to provide context-aware responses based on current environmental conditions.
Hardware Components:

ESP32 microcontroller with DHT11 temperature and humidity sensor
Raspberry Pi 5 running Node-RED and MQTT broker
NomadPuddy (IP: 192.168.8.60) running Ollama LLM server

Software Components:

Node-RED for flow control and integration
MQTT for message passing
Ollama API for LLM interaction

Implementation Details:

Sensor Data Collection and Transmission:

ESP32 programmed to read DHT11 sensor data periodically
Data published to MQTT topic: "nomadpuddy/esp32/sensor/dht11"
Format: JSON object with "temperature" and "humidity" fields


Node-RED Flow Enhancement:
a. New MQTT Input Node:

Topic: "nomadpuddy/esp32/#"
Listens for incoming sensor data

b. Switch Node:

Condition 1: msg.topic == "nomadpuddy/esp32/sensor/dht11"
Condition 2: otherwise
Separates sensor data from other messages

c. Parse DHT11 Data Function:

Processes incoming sensor data
Updates global variables with latest temperature and humidity
Function:
javascriptCopytry {
    let data = typeof msg.payload === 'string' ? JSON.parse(msg.payload) : msg.payload;
    global.set('temperature', data.temperature);
    global.set('humidity', data.humidity);
    node.warn(`Parsed DHT data - Temp: ${data.temperature}°C, Humidity: ${data.humidity}%`);
} catch (e) {
    node.error("Failed to parse DHT data: " + e.message);
}


d. Modified Prepare API Request Function:

Incorporates sensor data into LLM prompts
Function:
javascriptCopyconst temperature = global.get('temperature') || 'unavailable';
const humidity = global.get('humidity') || 'unavailable';
const customPrompt = `You have access to real-time temperature and humidity data from a DHT11 sensor. 
The current temperature is ${temperature}°C and the humidity is ${humidity}%. 
When asked about temperature or humidity, use this real-time data in your response.

User query: `;

if (typeof msg.payload === 'string') {
    msg.payload = {
        model: "llama3.1",
        prompt: customPrompt + msg.payload
    };
} else if (msg.payload && msg.payload.prompt) {
    msg.payload = {
        model: "llama3.1",
        prompt: customPrompt + msg.payload.prompt
    };
} else {
    node.warn("Invalid input format");
    return null;
}



LLM Integration:

Maintained existing Ollama API call structure using "/api/generate" endpoint
Enhanced prompts now include real-time sensor data


Flow Structure:

MQTT in (nomadpuddy/esp32/#) → Switch Node
Switch Node (Condition 1) → Parse DHT11 Data Function
Switch Node (Condition 2) → Prepare API Request Function
Existing MQTT inputs (llm/input, stt/output) → Prepare API Request Function
Prepare API Request Function → Ollama API Call Node
Ollama API Call Node → Process API Response Function
Process API Response Function → (Existing output handling)


Key Achievements:

Successful integration of IoT sensor data with an AI language model
Real-time environmental context provided to the LLM for more relevant responses
Maintained modular structure, allowing for easy expansion to include additional sensors or data sources
Preserved existing LLM query handling while adding new functionality

Future Expansion Possibilities:

Integration of additional sensors (e.g., light levels, motion detection)
Implementation of actuator control based on LLM decisions
Data logging and visualization for long-term analysis
Advanced prompt engineering to make better use of multiple data sources
Integration with home automation systems or other IoT devices

This implementation serves as a foundational example for integrating real-world data into AI-driven systems, enhancing the AI's ability to provide context-aware and environmentally-relevant responses.

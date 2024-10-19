<div align="center">

# Agent Armada

![Project Logo](./public/images/logo.jpg)

</div>

## Problem Statement
Natural disasters present significant challenges for search and rescue operations, often leading to delayed response times, difficulties in locating victims, and increased risks for personnel operating in hazardous environments.

## Other Similar Problems
- **Search and Rescue:** Coordinating efforts to locate and assist individuals in emergencies.
- **National Park Monitoring:** Observing wildlife and monitoring environmental changes in vast and rugged terrains.
- **Military Reconnaissance:** Gathering intelligence in potentially dangerous zones while ensuring personnel safety.

## Solution
**AI Multi-Agent Systems** represent an innovative frontier in addressing these complex challenges. They offer the ability to:
- Rapidly search large and dense terrains, significantly improving operational efficiency.
- Enhance search effectiveness compared to a single manually operated drone or convential human search efforts.
- Minimize human risk in environments that are otherwise perilous for personnel.

### Traditional Difficulties of Multi-Agent Systems
- **Design Complexity:** Development can be intricate and often tailored to specific tasks.
- **Management Challenges:** Effective deployment requires sophisticated objective planning and resource allocation.
- **Limited Human Interface:** Many traditional robotic systems are either pre-programmed or require manual control, which can hinder adaptability and responsiveness in dynamic situations.

## System Solution
Utilizing an **LLM (Large Language Model)** as an interface between a human and a swarm of autonomous agents. The LLM interprets the human request, breaks down the request using Chain of Thought, and directs the swarm of autonomous agents.

### Benefits of LLM Interface
- **Natural Human Interface:** A complex swarm can easily be managed and directed using text or voice commands.
- **Dynamic Planning:** The LLM can dynamically assign roles and objectives to each agent based on the human command and available resources.
- **Feedback:** The LLM can collect and interpret swarm information, allowing the human to easily understand objective progress.

### Hackathon Demo Presentation
./public/media/demo.mp4

## Getting Started
To set up the project locally, follow these steps:

### Prerequisites
Ensure you have Node.js (v14 or later) installed on your machine.

### Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agent-armada.git
   cd agent-armada
   ```

2. Install the necessary dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the root directory and add your API keys:
   ```env
   OPEN_AI_API_KEY=your_openai_api_key_here
   AI_ML_API_KEY=your_aiml_api_key_here
   ```

4. Run the application:
   ```bash
   npm run dev
   ```

### Usage
After running the application, navigate to `http://localhost:3000` in your browser to access the Agent Armada interface.

## Acknowledgement of Moral Hazard
The application of dynamic, environment-agnostic autonomous drone swarms has numerous beneficial use cases, including natural disaster search and rescue, agriculture, infrastructure maintenance, and wildlife management. However, the potential for misuse in warfare and other harmful applications raises significant ethical concerns.

## Potential Enhancements
This section outlines potential improvements and features that could be implemented in future versions of Agent Armada. We welcome contributions and suggestions from the community to enhance the capabilities of this project.

- **Adding Agent Memory with Case-Based Reasoning + Semantic Graphs:** Enable agents to remember past experiences and make informed decisions based on previous cases.
- **Implementing Reinforcement Learning:** Allow agents to learn optimal strategies through trial and error, enhancing their ability to adapt to various environments and tasks.
- **Integrating OpenStreetMap:** Incorporate detailed mapping data to improve navigation and search capabilities in complex terrains.
- **Enhanced User Interface:** Develop a more intuitive and interactive UI for easier interaction with the agent swarm and monitoring of their activities.
- **Advanced Local Agent Decision Logic:** Implement advanced communication strategies between agents to improve coordination and task sharing.

For more information about important files, and information flow see system_overview.txt

## Contributing
We welcome contributions to Agent Armada! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact Information
For questions or feedback, reach out to the project maintainers:
- **Name:** Cameron Gifford
- **GitHub:** [theorem-stack](https://github.com/theorem-stack)

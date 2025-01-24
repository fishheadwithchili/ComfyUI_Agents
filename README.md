# ComfyUI Agents

An AI-powered system that automates ComfyUI workflow creation and optimization through natural language interaction.

## Vision

ComfyUI Agents aims to revolutionize the way users interact with ComfyUI by providing an intelligent system that understands natural language requirements, automatically constructs workflows, and delivers optimal results.

## Development Roadmap

### Phase 1 (Current)
- AI-powered workflow decomposition and reconstruction from annotated workflow files
- Graph database implementation for workflow storage and management
- Integration of AI capabilities with graph database for workflow optimization
- Core ComfyUI API functionalities:
  - Log retrieval
  - Workflow CRUD operations
  - Workflow execution
  - Automatic model node downloads
- Manual workflow curation and result evaluation

### Future Architecture

The system consists of three main components:

#### 1. ComfyUI Agents (Core)
- Natural language user interaction
- Requirement analysis
- Input object management
- Workflow reconstruction using graph database
- Backend server communication
- AI-powered result filtering

#### 2. ComfyUI Spider
- Daily crawling of community resources:
  - X (Twitter)
  - Reddit
  - LiblibAI
  - Civitai
- New workflow discovery

#### 3. ComfyUI Lab
- Workflow testing
- Result evaluation
- Documentation generation
- Graph database integration

## Key Features

- Natural language requirement parsing
- Automatic input file requests
- Workflow analysis and reconstruction
- Multiple solution evaluation
- Direct execution or API integration
- Community workflow integration

## Technical Stack

- Graph Database: TBD
- AI Models: For workflow analysis and optimization
- ComfyUI API Integration
- Web Crawling Framework
- Evaluation System 
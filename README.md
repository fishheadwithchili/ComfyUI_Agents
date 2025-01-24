# ComfyUI Agents

ComfyUI Agents is an intelligent workflow automation tool that simplifies the creation and optimization of ComfyUI workflows through natural language input.

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

## System Architecture

The system consists of three main components:

### 1. ComfyUI Agents (Core)
- Natural language user interaction
- Requirement analysis
- Input object management
- Workflow reconstruction using graph database
- Backend server communication
- AI-powered result filtering

### 2. ComfyUI Spider
- Daily crawling of community resources:
  - X (Twitter)
  - Reddit
  - LiblibAI
  - Civitai
- New workflow discovery

### 3. ComfyUI Lab
- Workflow testing
- Result evaluation
- Documentation generation
- Graph database integration

## Project Structure

```
src/
├── workflows/           # Workflow files organized by category
│   ├── basic/          # Basic example workflows
│   ├── image_editing/  # Image editing workflows
│   ├── keying/         # Image keying workflows
│   └── instant_id/     # InstantID related workflows
├── test_output/        # Test workflow outputs
└── test_connection.py  # Database connection test script
```

## Database Structure

The project uses JanusGraph (with Cassandra storage) to manage workflow metadata:

- Vertices:
  - Category: Represents workflow categories
  - Workflow: Represents individual workflows
- Edges:
  - belongs_to: Connects workflows to their categories

## Key Features

- Natural language requirement parsing
- Automatic input file requests
- Workflow analysis and reconstruction
- Multiple solution evaluation
- Direct execution or API integration
- Community workflow integration

## Technical Stack

- Graph Database: JanusGraph with Cassandra
- AI Models: For workflow analysis and optimization
- ComfyUI API Integration
- Web Crawling Framework
- Evaluation System

## Dependencies
- Docker and Docker Compose
- Python 3.12
- JanusGraph 1.1.0
- Cassandra 4.1.3
- Required Python packages:
  - gremlinpython==3.6.1
  - pyyaml==6.0.1
  - python-dotenv==1.0.0

## Usage

1. Start the database:
```bash
docker-compose up -d
```

2. Test the connection:
```bash
python src/test_connection.py
```

3. Import new workflows:
```bash
python src/import_workflow.py
```

4. Try example operations:
```bash
python src/example_usage.py
```

## Documentation
For development logs and detailed changes, please refer to [CHANGELOG.md](CHANGELOG.md) 
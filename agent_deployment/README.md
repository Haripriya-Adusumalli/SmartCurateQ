# Agent Deployment to Google Cloud Agent Engine

This directory contains all the configuration and deployment scripts for deploying the AI Startup Evaluator agents to Google Cloud Agent Engine.

## 🤖 Agents Overview

### 1. Data Extraction Agent
- **Purpose**: Extracts and processes data from pitch decks, forms, and documents
- **Capabilities**: PDF processing, form parsing, data validation
- **Model**: Gemini 1.5 Pro

### 2. Mapping Agent  
- **Purpose**: Maps extracted data to standardized startup profiles
- **Capabilities**: Founder-market fit scoring, data normalization
- **Model**: Gemini 1.5 Pro

### 3. Public Data Agent
- **Purpose**: Enriches analysis with external market data
- **Capabilities**: Web research, claim verification, competitive analysis
- **Model**: Gemini 1.5 Pro

### 4. Analysis Agent
- **Purpose**: Generates investment scores and recommendations
- **Capabilities**: Risk assessment, scoring algorithms, recommendations
- **Model**: Gemini 1.5 Pro

### 5. Voice Agent
- **Purpose**: Conducts voice conversations with founders
- **Capabilities**: Voice processing, structured interviews, founder assessment
- **Model**: Gemini 1.5 Pro with voice capabilities

### 6. Orchestrator Agent
- **Purpose**: Coordinates multi-agent workflow
- **Capabilities**: Workflow management, data synthesis, memo generation
- **Model**: Gemini 1.5 Pro

## 🚀 Deployment Instructions

### Prerequisites

1. **Google Cloud Project**: Set up a Google Cloud project with billing enabled
2. **Authentication**: Configure Google Cloud authentication
3. **APIs**: The deployment script will enable required APIs automatically

### Environment Setup

```bash
# Set your Google Cloud project
export GOOGLE_CLOUD_PROJECT="your-project-id"
export AGENT_LOCATION="us-central1"

# Authenticate with Google Cloud
gcloud auth login
gcloud auth application-default login
```

### Deploy All Agents

```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

Or deploy using Python directly:

```bash
# Install dependencies
pip install google-cloud-aiplatform pyyaml

# Deploy agents
python deploy_agents.py
```

### Verify Deployment

```bash
# Test agent client
python agent_client.py
```

## 📋 Agent Configuration Files

- `data_extraction_agent.yaml` - Data extraction agent configuration
- `mapping_agent.yaml` - Mapping agent configuration  
- `public_data_agent.yaml` - Public data agent configuration
- `analysis_agent.yaml` - Analysis agent configuration
- `voice_agent.yaml` - Voice agent configuration
- `orchestrator_agent.yaml` - Orchestrator agent configuration

## 🔧 Usage

### Using the Agent Client

```python
from agent_client import AgentClient
import asyncio

async def evaluate_startup():
    client = AgentClient()
    
    startup_data = {
        "company_name": "TechCorp",
        "problem_statement": "...",
        "solution": "...",
        # ... more data
    }
    
    # Run complete evaluation
    results = await client.orchestrate_startup_evaluation(startup_data)
    print(results["final_memo"]["response"])

# Run evaluation
asyncio.run(evaluate_startup())
```

### Individual Agent Calls

```python
# Call specific agent
result = await client.call_agent(
    "analysis-agent",
    "Generate investment score for this startup",
    startup_data
)
```

### Voice Interview

```python
# Schedule founder interview
interview_result = await client.schedule_founder_interview(
    startup_data,
    questions=["What's your biggest challenge?", "How do you plan to scale?"]
)
```

## 📊 Monitoring and Management

### Check Agent Status

```python
client = AgentClient()
status = client.get_agent_status()
print(status)
```

### View in Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to AI Platform > Agents
3. View deployed agents and their metrics

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Error**
   ```bash
   gcloud auth application-default login
   ```

2. **API Not Enabled**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   ```

3. **Permission Denied**
   - Ensure your account has AI Platform Admin role
   - Check project billing is enabled

### Debug Mode

```bash
# Enable debug logging
export GOOGLE_CLOUD_LOG_LEVEL=DEBUG
python deploy_agents.py
```

## 📈 Performance Optimization

### Agent Configuration Tuning

- **Temperature**: Lower for consistent outputs (0.1-0.3)
- **Max Tokens**: Adjust based on expected response length
- **Model**: Use Gemini 1.5 Pro for complex reasoning

### Workflow Optimization

- **Parallel Execution**: Some agents can run in parallel
- **Caching**: Cache public data lookups
- **Error Handling**: Implement retry logic with exponential backoff

## 🔐 Security Considerations

- **API Keys**: Store securely in Secret Manager
- **Data Privacy**: Ensure compliance with data protection regulations
- **Access Control**: Use IAM roles for fine-grained permissions
- **Audit Logging**: Enable Cloud Audit Logs for agent activities

## 💰 Cost Management

- **Model Selection**: Balance performance vs cost
- **Request Batching**: Batch similar requests when possible
- **Monitoring**: Set up billing alerts and quotas
- **Optimization**: Regular review of agent performance and costs

## 🚀 Next Steps

1. **Deploy agents** using the provided scripts
2. **Test functionality** with sample data
3. **Integrate with frontend** application
4. **Monitor performance** and optimize as needed
5. **Scale deployment** based on usage patterns
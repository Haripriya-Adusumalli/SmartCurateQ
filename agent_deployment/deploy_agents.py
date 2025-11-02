#!/usr/bin/env python3
"""
Deploy all agents to Google Cloud Agent Engine
"""

import os
import yaml
import json
from google.cloud import aiplatform
from google.oauth2 import service_account
import time

class AgentDeployer:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        
        # Initialize AI Platform client
        aiplatform.init(project=project_id, location=location)
        
        self.agent_configs = [
            "data_extraction_agent.yaml",
            "mapping_agent.yaml", 
            "public_data_agent.yaml",
            "analysis_agent.yaml",
            "voice_agent.yaml",
            "orchestrator_agent.yaml"
        ]
    
    def load_agent_config(self, config_file: str) -> dict:
        """Load agent configuration from YAML file"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def deploy_agent(self, config: dict) -> str:
        """Deploy a single agent to Agent Engine"""
        try:
            print(f"Deploying agent: {config['metadata']['displayName']}")
            
            # Create agent using AI Platform
            agent = aiplatform.Agent.create(
                display_name=config['metadata']['displayName'],
                description=config['spec']['description'],
                instructions=config['spec']['instructions'],
                model=config['spec'].get('model', 'gemini-2.5-pro'),
                temperature=config['spec'].get('temperature', 0.2),
                max_tokens=config['spec'].get('maxTokens', 4096),
                tools=config['spec'].get('tools', [])
            )
            
            print(f"✅ Successfully deployed: {agent.display_name}")
            print(f"   Agent ID: {agent.name}")
            
            return agent.name
            
        except Exception as e:
            print(f"❌ Failed to deploy {config['metadata']['displayName']}: {str(e)}")
            return None
    
    def deploy_all_agents(self) -> dict:
        """Deploy all agents and return their IDs"""
        deployed_agents = {}
        
        print("🚀 Starting agent deployment to Google Cloud Agent Engine...")
        print(f"Project: {self.project_id}")
        print(f"Location: {self.location}")
        print("-" * 60)
        
        for config_file in self.agent_configs:
            try:
                config = self.load_agent_config(config_file)
                agent_id = self.deploy_agent(config)
                
                if agent_id:
                    agent_name = config['metadata']['name']
                    deployed_agents[agent_name] = agent_id
                
                # Wait between deployments
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error processing {config_file}: {str(e)}")
        
        return deployed_agents
    
    def create_agent_registry(self, deployed_agents: dict):
        """Create a registry file with deployed agent information"""
        registry = {
            "project_id": self.project_id,
            "location": self.location,
            "deployed_at": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "agents": deployed_agents
        }
        
        with open("agent_registry.json", "w") as f:
            json.dump(registry, f, indent=2)
        
        print(f"📋 Agent registry saved to agent_registry.json")
    
    def verify_deployment(self, deployed_agents: dict):
        """Verify all agents are deployed and accessible"""
        print("\n🔍 Verifying agent deployment...")
        
        for agent_name, agent_id in deployed_agents.items():
            try:
                # Try to get agent details
                agent = aiplatform.Agent(agent_id)
                status = "✅ Active" if agent.state == "ACTIVE" else f"⚠️ {agent.state}"
                print(f"   {agent_name}: {status}")
                
            except Exception as e:
                print(f"   {agent_name}: ❌ Error - {str(e)}")

def main():
    # Configuration
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    LOCATION = os.getenv("AGENT_LOCATION", "us-central1")
    
    if PROJECT_ID == "your-project-id":
        print("❌ Please set GOOGLE_CLOUD_PROJECT environment variable")
        return
    
    # Deploy agents
    deployer = AgentDeployer(PROJECT_ID, LOCATION)
    deployed_agents = deployer.deploy_all_agents()
    
    if deployed_agents:
        print(f"\n✅ Successfully deployed {len(deployed_agents)} agents!")
        
        # Create registry
        deployer.create_agent_registry(deployed_agents)
        
        # Verify deployment
        deployer.verify_deployment(deployed_agents)
        
        print("\n🎉 Agent deployment completed!")
        print("\nNext steps:")
        print("1. Update your application to use the deployed agent IDs")
        print("2. Test the multi-agent workflow")
        print("3. Monitor agent performance in Cloud Console")
        
    else:
        print("❌ No agents were successfully deployed")

if __name__ == "__main__":
    main()
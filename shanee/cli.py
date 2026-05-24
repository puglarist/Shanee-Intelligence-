"""Command-line interface for Shanee Omniverse OS"""

import asyncio
import json
from typing import Optional

import click

from core.intelligence import AgentFactory, AgentConfig


class ShaneeCLI:
    """Interactive CLI for Shanee Omniverse OS"""

    def __init__(self):
        self.agent_factory = AgentFactory()
        self.current_agent = None

    async def repl(self):
        """Interactive REPL mode"""
        click.echo("🚀 Shanee Intelligence Omniverse OS v0.1.0")
        click.echo("Type 'help' for commands or 'exit' to quit\n")

        while True:
            try:
                command = click.prompt("shanee", type=str)

                if command.lower() == "exit":
                    click.echo("Goodbye!")
                    break
                elif command.lower() == "help":
                    self.show_help()
                elif command.startswith("create-agent"):
                    await self.create_agent_interactive()
                elif command.startswith("list-agents"):
                    self.list_agents()
                elif command.startswith("select-agent"):
                    parts = command.split(" ", 1)
                    if len(parts) > 1:
                        self.select_agent(parts[1])
                    else:
                        click.echo("Usage: select-agent <agent_id>")
                elif command.startswith("message"):
                    if not self.current_agent:
                        click.echo("No agent selected. Use 'create-agent' or 'select-agent'")
                    else:
                        parts = command.split(" ", 1)
                        if len(parts) > 1:
                            message = parts[1]
                            await self.send_message(message)
                        else:
                            click.echo("Usage: message <text>")
                else:
                    if self.current_agent:
                        await self.send_message(command)
                    else:
                        click.echo(f"Unknown command: {command}. Type 'help' for options.")

            except KeyboardInterrupt:
                click.echo("\nInterrupted. Type 'exit' to quit.")
            except Exception as e:
                click.echo(f"Error: {e}")

    def show_help(self):
        """Display help text"""
        help_text = """
Available Commands:
  create-agent         Create a new agent
  list-agents          List all agents
  select-agent <id>    Select an agent to interact with
  message <text>       Send message to current agent
  help                 Show this help
  exit                 Exit the program

If an agent is selected, you can also just type text to send it directly.
        """
        click.echo(help_text)

    async def create_agent_interactive(self):
        """Create agent interactively"""
        name = click.prompt("Agent name")
        description = click.prompt("Agent description", default="")
        model = click.prompt("Model ID", default="claude-opus-4-7")

        config = AgentConfig(
            name=name,
            description=description,
            model_id=model
        )
        agent = self.agent_factory.create(config)
        self.current_agent = agent
        click.echo(f"✅ Created agent: {agent.id}")

    def list_agents(self):
        """List all agents"""
        agents = self.agent_factory.list()
        if not agents:
            click.echo("No agents created yet.")
            return

        click.echo("\nAgents:")
        for agent in agents:
            marker = "→" if agent == self.current_agent else " "
            click.echo(f"  {marker} {agent.id[:8]}... {agent.config.name} ({agent.state.value})")
        click.echo()

    def select_agent(self, agent_id: str):
        """Select agent by ID"""
        agent = self.agent_factory.get(agent_id)
        if not agent:
            click.echo(f"Agent not found: {agent_id}")
            return

        self.current_agent = agent
        click.echo(f"Selected: {agent.config.name}")

    async def send_message(self, message: str):
        """Send message to current agent"""
        if not self.current_agent:
            click.echo("No agent selected.")
            return

        with click.progressbar(length=100, label="Thinking") as bar:
            try:
                response = await self.current_agent.run(message)
                bar.finish()
                click.echo(f"\n🤖 Agent: {response}\n")
            except Exception as e:
                bar.finish()
                click.echo(f"\n❌ Error: {e}\n")


@click.group()
def cli():
    """Shanee Intelligence Omniverse OS"""
    pass


@cli.command()
def repl():
    """Start interactive REPL"""
    cli_instance = ShaneeCLI()
    asyncio.run(cli_instance.repl())


@cli.command()
def version():
    """Show version"""
    from shanee import __version__
    click.echo(f"Shanee v{__version__}")


@cli.command()
def server():
    """Start API server"""
    import uvicorn
    from services.orchestrator.server import app

    click.echo("Starting Shanee API server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


@cli.command()
@click.option("--host", default="localhost", help="Server host")
@click.option("--port", default=8000, help="Server port")
def dev(host: str, port: int):
    """Start development server"""
    import uvicorn
    from services.orchestrator.server import app

    click.echo(f"Starting Shanee dev server on http://{host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )


def main():
    """Main CLI entry point"""
    cli()


if __name__ == "__main__":
    main()

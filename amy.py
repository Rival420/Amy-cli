import os
import requests
import sys
import openai
import click
import subprocess
import shlex
import json
import asyncio
from pathlib import Path

config_file = Path("config.json")
command_history_file = Path("command_history.json")

def load_config():
    if config_file.exists():
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = {
            "engine": "gpt-3.5-turbo",
            "temperature": 0.5,
            "max_tokens": 150,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "allowed_commands": [],
            "openai_api_key": ""
        }
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)
    return config

def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)

def save_history(history):
    with open(command_history_file, "w") as f:
        json.dump(history, f, indent=4)


def load_command_history():
    if command_history_file.exists():
        with open(command_history_file, "r") as f:
            command_history = json.load(f)
    else:
        command_history = []
    return command_history


config = load_config()
command_history = load_command_history()

def get_instruction(query):
    messages = [
        {
            "role": "system",
            "content": "You are an AI living inside a Debian terminal with Bash. Your output will be executed as a command. You cannot use other text nor \"`\" for formatting."
        },
        {
            "role": "user",
            "content": f"Understand the following query and generate the appropriate command: {query}"
        }
    ]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['openai_api_key']}",
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": config["temperature"],
        "max_tokens": config["max_tokens"],
        "top_p": config["top_p"],
        "frequency_penalty": config["frequency_penalty"],
        "presence_penalty": config["presence_penalty"],
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        click.echo("Command executed successfully:")
        click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo("Command execution failed:")
        click.echo(e.stderr)

@click.group(invoke_without_command=True, help="Amy is a command-line interface for using AI-powered instructions.")
@click.pass_context
def amy(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Welcome to Amy!")
        click.echo("Type 'amy --help' for a list of available commands.")

@amy.command(help="Execute a given query and run the generated instruction.")
@click.argument("query")
def execute(query):
    instruction = get_instruction(query)
    click.echo(f"Instruction: {instruction}")

    if config["allowed_commands"]:
        cmd = shlex.split(instruction)[0]
        if cmd not in config["allowed_commands"]:
            click.echo("This command is not allowed.")
            return

    if click.confirm("Do you want to execute the instruction?"):
        execute_command(instruction)
        command_history.append({"query": query, "instruction": instruction})
        save_history(command_history)



@amy.command(help="Display the current configuration.")
def show_config():
    click.echo(json.dumps(config, indent=4))

@amy.command(help="Display the command history.")
def show_history():
    for idx, item in enumerate(command_history, start=1):
        click.echo(f"{idx}. Query: {item['query']}\n   Instruction: {item['instruction']}\n")


@amy.command(help="Enter interactive mode to continuously input queries and execute instructions.")
@click.pass_context
def interactive(ctx):
    click.echo("Entering interactive mode. Type 'exit' to quit.")
    while True:
        query = input("Query> ")
        if query.lower() == "exit":
            break
        ctx.invoke(execute, query=query)

@amy.command(help="Set the OpenAI API key and store it in the configuration file.")
@click.argument("api_key")
def init(api_key):
    config["openai_api_key"] = api_key
    save_config(config)
    click.echo("API key has been set and saved in the configuration file.")

if __name__ == '__main__':
    if not config["openai_api_key"]:
        if len(sys.argv) > 1 and sys.argv[1] == "init":
            amy(prog_name='amy')
        else:
            click.echo("No OpenAI API key found. Please set the key using 'amy init <api_key>'.")
    else:
        amy(prog_name='amy')



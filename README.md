# My Agent - Multi-Agent System

A multi-agent system built with Google ADK that provides:
- Time lookup functionality
- Payment fee calculation
- Exchange rate conversion

## Structure
- `helpful_assistant/` - Root agent that orchestrates other agents
- `time_agent/` - Agent for time queries
- `fee_rate/` - Tool for payment fee lookup
- `exchange_rate/` - Tool for exchange rate lookup

## Installation
pip install -r requirements.txt

## Usage
adk run helpful_assistant

## Architecture
The root agent (`helpful_assistant`) uses tools from other modules to handle various queries.

## Install Agent Development Kit (ADK)
https://google.github.io/adk-docs/


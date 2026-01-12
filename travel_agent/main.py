# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""Travel Agent - Comprehensive travel planning and itinerary creation.

Provides personalized travel plans with accommodations, activities, logistics,
and local insights using Exa search for destination research and MCP tools
for Airbnb and Google Maps integration.
"""

import argparse
import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.exa import ExaTools
from agno.tools.mcp import MultiMCPTools
from agno.tools.mem0 import Mem0Tools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global instances
agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


class APIKeyError(ValueError):
    """API key is missing."""


def load_config() -> dict:
    """Load agent configuration from project root."""
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path(__file__).parent / "agent_config.json",  # Same directory
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error reading {config_path}: {e}")
                continue

    # Default configuration
    return {
        "name": "travel-agent",
        "description": "AI-powered travel planning agent with comprehensive itinerary creation",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {
                "key": "OPENROUTER_API_KEY",
                "description": "OpenRouter API key for LLM calls (required)",
                "required": True,
            },
            {
                "key": "MODEL_NAME",
                "description": "Model ID for OpenRouter",
                "required": False,
            },
            {
                "key": "EXA_API_KEY",
                "description": "Exa API key for destination research (required)",
                "required": True,
            },
            {
                "key": "MEM0_API_KEY",
                "description": "Mem0 API key for memory operations",
                "required": False,
            },
        ],
    }


def _get_api_keys() -> tuple[str | None, str | None, str | None, str]:
    """Get API keys and configuration from environment."""
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    mem0_api_key = os.getenv("MEM0_API_KEY")
    exa_api_key = os.getenv("EXA_API_KEY")
    model_name = os.getenv("MODEL_NAME", "openai/gpt-4o")
    return openrouter_api_key, mem0_api_key, exa_api_key, model_name


def _create_llm_model(openrouter_api_key: str, model_name: str) -> OpenRouter:
    """Create and return the OpenRouter model."""
    if not openrouter_api_key:
        error_msg = (
            "OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.\n"
            "Get an API key from: https://openrouter.ai/keys"
        )
        raise APIKeyError(error_msg)

    return OpenRouter(
        id=model_name,
        api_key=openrouter_api_key,
        cache_response=True,
        supports_native_structured_outputs=True,
    )


def _setup_tools(
    mem0_api_key: str | None, exa_api_key: str
) -> tuple[list, MultiMCPTools | None]:
    """Set up all tools for the travel agent."""
    tools = []
    mcp_tools = None

    # ExaTools is required for destination research
    try:
        exa_tools = ExaTools(api_key=exa_api_key)
        tools.append(exa_tools)
        print("🌍 Exa search enabled for destination research")
    except Exception as e:
        print(f"❌ Failed to initialize ExaTools: {e}")
        raise

    # Optional: Mem0 for conversation memory
    if mem0_api_key:
        try:
            mem0_tools = Mem0Tools(api_key=mem0_api_key)
            tools.append(mem0_tools)
            print("🧠 Mem0 memory system enabled for conversation context")
        except Exception as e:
            print(f"⚠️  Mem0 initialization issue: {e}")

    # Optional: MCP tools for Airbnb and Google Maps
    try:
        mcp_tools = MultiMCPTools(
            commands=[
                "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt",
                "npx -y @modelcontextprotocol/server-google-maps",
            ],
            env=dict(os.environ),
            allow_partial_failure=True,
            timeout_seconds=30,
        )
        asyncio.run(mcp_tools.connect())
        tools.append(mcp_tools)
        print("🏨 MCP tools enabled (Airbnb + Google Maps)")
    except Exception as e:
        print(f"⚠️  MCP tools initialization issue: {e}")
        print("   Note: Some travel planning features may be limited")

    return tools, mcp_tools


async def initialize_agent() -> None:
    """Initialize the travel planning agent."""
    global agent

    openrouter_api_key, mem0_api_key, exa_api_key, model_name = _get_api_keys()

    # Validate required API keys
    if not openrouter_api_key:
        error_msg = (
            "OpenRouter API key is required. Set OPENROUTER_API_KEY environment variable.\n"
            "Get an API key from: https://openrouter.ai/keys"
        )
        raise APIKeyError(error_msg)

    if not exa_api_key:
        error_msg = (
            "Exa API key is required for destination research. Set EXA_API_KEY environment variable.\n"
            "Get an API key from: https://exa.ai"
        )
        raise APIKeyError(error_msg)

    model = _create_llm_model(openrouter_api_key, model_name)
    tools, mcp_tools = _setup_tools(mem0_api_key, exa_api_key)

    # Create the travel planning agent
    agent = Agent(
        name="Globe Hopper - Travel Planning Expert",
        model=model,
        tools=tools,
        description=dedent("""\
            You are Globe Hopper, an elite travel planning expert with decades of experience! 🌍

            Your expertise encompasses:
            - Luxury and budget travel planning
            - Corporate retreat organization
            - Cultural immersion experiences
            - Adventure trip coordination
            - Local cuisine exploration
            - Transportation logistics
            - Accommodation selection (Airbnb integration)
            - Activity curation
            - Budget optimization
            - Group travel management
            - Destination research and validation
            - Seasonal travel considerations
            - Accessibility planning
            - Emergency contingency planning"""),
        instructions=dedent("""\
            COMPREHENSIVE TRAVEL PLANNING PROCESS:

            1. INITIAL ASSESSMENT & CLARIFICATION 🎯
               - Understand group size, composition, and dynamics
               - Note specific travel dates, duration, and seasonality
               - Identify budget constraints and preferences
               - Clarify travel style (luxury, budget, adventure, cultural, etc.)
               - Note any special requirements (accessibility, dietary, etc.)
               - Understand trip purpose (vacation, business, celebration, etc.)

            2. DESTINATION RESEARCH & VALIDATION 🔍
               - Use Exa search to research destinations, attractions, and local insights
               - Verify current operating hours, entry requirements, and availability
               - Check for local events, festivals, or seasonal considerations
               - Research weather patterns and climate during travel dates
               - Identify potential challenges or travel advisories
               - Validate transportation options and connectivity

            3. ACCOMMODATION PLANNING & SELECTION 🏨
               - Search for Airbnb accommodations using MCP tools when available
               - Consider group size, preferences, and budget
               - Select strategic locations near key activities/attractions
               - Verify amenities, facilities, and guest reviews
               - Include backup options and alternatives
               - Check cancellation policies and booking flexibility

            4. ACTIVITY CURATION & SCHEDULING 🎨
               - Balance various interests and activity types
               - Include authentic local experiences and cultural immersion
               - Consider realistic travel time between venues
               - Add flexible "free time" blocks for spontaneity
               - Include backup activities for weather contingencies
               - Note advance booking requirements and deadlines

            5. LOGISTICS & TRANSPORTATION PLANNING 🚗
               - Use Google Maps via MCP for accurate distances and travel times
               - Detail transportation options (flights, trains, rental cars, etc.)
               - Include local transport tips and cost estimates
               - Consider accessibility requirements and options
               - Plan airport transfers and inter-city travel
               - Add contingency plans for delays or changes

            6. BUDGET OPTIMIZATION & COST BREAKDOWN 💰
               - Itemize major expense categories
               - Provide realistic cost estimates for each component
               - Include budget-saving tips and alternatives
               - Note potential hidden costs and fees
               - Suggest money-saving strategies without compromising experience
               - Provide luxury upgrade options when applicable

            7. LOCAL INSIGHTS & CULTURAL GUIDANCE 🗺️
               - Include local customs, etiquette, and cultural norms
               - Suggest appropriate dress codes for different venues
               - Recommend local cuisine and dining experiences
               - Provide language tips and essential phrases
               - Note tipping customs and local payment methods
               - Include safety tips and emergency contacts

            RESPONSE STRUCTURE & FORMATTING:
            - Use clear markdown formatting with emojis for visualization
            - Present comprehensive day-by-day itineraries
            - Include time estimates for all activities and travel
            - Highlight "must-do" experiences and "hidden gems"
            - Use tables for accommodation comparisons and budget breakdowns
            - Add maps or location references when relevant
            - Include booking requirements and advance notice needs
            - Provide local tips and cultural notes throughout

            QUALITY STANDARDS:
            - Always verify information through Exa search
            - Provide realistic time estimates and logistical plans
            - Consider seasonal factors and local conditions
            - Include contingency options for common travel disruptions
            - Balance structured planning with flexibility
            - Respect budget constraints while maximizing experience
            - Prioritize safety, accessibility, and comfort
        """),
        expected_output=dedent("""\
            # {Destination} Travel Itinerary 🌎

            ## 📋 Trip Overview
            - **Dates**: {travel_dates}
            - **Duration**: {number_of_days} days
            - **Group Size**: {group_size} people
            - **Budget Range**: {budget_range}
            - **Travel Style**: {travel_style}
            - **Primary Focus**: {trip_focus}

            ## 🏨 Accommodation Options

            ### Recommended Stay:
            **Property**: {accommodation_name}
            **Type**: {property_type}
            **Location**: {neighborhood_area}
            **Key Features**: {amenities}
            **Estimated Cost**: {cost_per_night}/night
            **Booking Platform**: {booking_source}

            ### Alternative Options:
            1. {alternative_1} - {pros_and_cons}
            2. {alternative_2} - {pros_and_cons}

            ## 📅 Daily Itinerary

            ### Day 1: Arrival & Orientation
            **Theme**: {day_1_theme}

            | Time | Activity | Details | Location | Estimated Cost |
            |------|----------|---------|----------|----------------|
            | {time} | {activity} | {details} | {location} | {cost} |
            | {time} | {activity} | {details} | {location} | {cost} |

            **Day 1 Notes**: {important_notes}

            ### Day 2: {day_2_theme}
            [Continue detailed schedule...]

            ## 💰 Comprehensive Budget Breakdown

            | Category | Estimated Cost | Notes |
            |----------|----------------|-------|
            | Accommodation | ${accom_cost} | {accom_notes} |
            | Flights/Transport | ${transport_cost} | {transport_notes} |
            | Activities & Tours | ${activities_cost} | {activities_notes} |
            | Food & Dining | ${food_cost} | {food_notes} |
            | Local Transportation | ${local_transport_cost} | {local_transport_notes} |
            | Miscellaneous | ${misc_cost} | {misc_notes} |
            | **Total Estimated** | **${total_cost}** | {total_notes} |

            ## 🚗 Logistics & Transportation

            ### Getting There:
            {arrival_transport_details}

            ### Local Transportation:
            {local_transport_details}

            ### Getting Around:
            {getting_around_tips}

            ## 📋 Booking Requirements & Timeline

            **Immediate Action (Now):**
            - {immediate_actions}

            **Book Within 1 Month:**
            - {one_month_actions}

            **Book Within 2 Weeks:**
            - {two_week_actions}

            ## 🗺️ Local Tips & Cultural Insights

            ### Cultural Etiquette:
            {cultural_etiquette}

            ### Dining & Cuisine:
            {dining_tips}

            ### Safety & Practical Tips:
            {safety_tips}

            ### Language Tips:
            {language_tips}

            ## ⚠️ Important Considerations

            ### Weather & Seasonal Notes:
            {weather_notes}

            ### Health & Safety:
            {health_safety}

            ### Contingency Plans:
            {contingency_plans}

            ---
            *Itinerary curated by Globe Hopper Travel Planning* 🌍
            *Last Updated: {current_date}*
            *Note: Prices and availability subject to change. Always verify current information before booking.*
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
    print(f"✅ Travel Planning agent initialized using {model_name}")
    print(f"🌍 Exa research enabled for destination insights")
    if mem0_api_key:
        print("🧠 Memory system enabled for conversation context")
    if mcp_tools:
        print("🏨 MCP tools enabled (Airbnb + Google Maps)")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages."""
    global agent

    if not agent:
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    return await agent.arun(messages)


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Travel Planning Agent...")
            await initialize_agent()
            _initialized = True

    return await run_agent(messages)


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up Travel Planning Agent resources...")


def _setup_environment_variables(args: argparse.Namespace) -> None:
    """Set environment variables from command line arguments."""
    if args.openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = args.openrouter_api_key
    if args.mem0_api_key:
        os.environ["MEM0_API_KEY"] = args.mem0_api_key
    if args.exa_api_key:
        os.environ["EXA_API_KEY"] = args.exa_api_key
    if args.model:
        os.environ["MODEL_NAME"] = args.model


def _display_configuration_info() -> None:
    """Display configuration information to the user."""
    print("=" * 60)
    print("🌍 TRAVEL PLANNING AGENT")
    print("=" * 60)
    print("✈️ Purpose: Comprehensive travel itinerary creation")
    print("🔍 Powered by: Exa search + MCP tools (Airbnb + Google Maps)")

    config_info = []
    if os.getenv("OPENROUTER_API_KEY"):
        model = os.getenv("MODEL_NAME", "openai/gpt-4o")
        config_info.append(f"🤖 Model: {model}")
    if os.getenv("EXA_API_KEY"):
        config_info.append("🌍 Exa: Destination research enabled")
    if os.getenv("MEM0_API_KEY"):
        config_info.append("🧠 Memory: Conversation context enabled")

    for info in config_info:
        print(info)

    print("💼 Features: Accommodations, activities, logistics, budget planning")
    print("=" * 60)
    print("Example queries:")
    print("• 'Plan a 5-day cultural trip to Kyoto for family of 4'")
    print("• 'Create romantic weekend getaway in Paris with $2000 budget'")
    print("• 'Organize 7-day adventure trip to New Zealand for solo travel'")
    print("• 'Design tech company offsite in Barcelona for 20 people'")
    print("• 'Plan luxury honeymoon in Maldives for 10 days'")
    print("=" * 60)


def main() -> None:
    """Run the main entry point for the Travel Planning Agent."""
    parser = argparse.ArgumentParser(
        description="Travel Planning Agent - Comprehensive itinerary creation and travel planning"
    )
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--mem0-api-key",
        type=str,
        default=os.getenv("MEM0_API_KEY"),
        help="Mem0 API key for conversation memory (optional)",
    )
    parser.add_argument(
        "--exa-api-key",
        type=str,
        default=os.getenv("EXA_API_KEY"),
        help="Exa API key for destination research (required)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL_NAME", "openai/gpt-4o"),
        help="Model ID for OpenRouter (env: MODEL_NAME)",
    )
    args = parser.parse_args()

    _setup_environment_variables(args)
    _display_configuration_info()

    config = load_config()

    try:
        print("\n🚀 Starting Travel Planning Agent server...")
        print(f"🌐 Access at: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3773')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Travel Planning Agent stopped")
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        asyncio.run(cleanup())


if __name__ == "__main__":
    main()
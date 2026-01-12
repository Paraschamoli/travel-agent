<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">Travel Agent</h1>
<h3 align="center">AI-Powered Travel Planning Assistant with Comprehensive Itinerary Creation</h3>

<p align="center">
  <strong>Provides personalized travel plans with accommodations, activities, logistics, and local insights. Integrates Exa search for destination research and MCP tools for Airbnb and Google Maps.</strong><br/>
  Create detailed itineraries, optimize budgets, and discover local experiences for any type of trip.
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/travel-agent/actions/workflows/build-and-push.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/travel-agent/build-and-push.yml?branch=main" alt="Build status">
  </a>
  <a href="https://img.shields.io/github/license/Paraschamoli/travel-agent">
    <img src="https://img.shields.io/github/license/Paraschamoli/travel-agent" alt="License">
  </a>
  <a href="https://img.shields.io/badge/python-3.12-blue">
    <img src="https://img.shields.io/badge/python-3.12-blue" alt="Python 3.12">
  </a>
</p>

---

## 🎯 What is Travel Agent?

An AI-powered assistant that creates comprehensive travel plans with detailed itineraries, destination research, accommodation options, and logistical planning. Think of it as your personal travel concierge that handles research, planning, and recommendations.

### Key Features
*   **✈️ Comprehensive Planning** - Full trip planning from start to finish
*   **🌍 Destination Research** - Exa search integration for current information
*   **🏨 Accommodation Options** - Airbnb integration via MCP tools
*   **🗺️ Transportation Logistics** - Google Maps integration for route planning
*   **💰 Budget Optimization** - Detailed cost breakdowns and saving strategies
*   **🧠 Memory Support** - Optional Mem0 integration for conversation context
*   **🎯 Personalized Itineraries** - Tailored to group size, interests, and budget
*   **📋 Booking Checklists** - Timeline and requirement management

### Built-in Tools
*   **ExaTools** - Real-time destination research and validation
*   **MultiMCPTools** - Airbnb and Google Maps integration
*   **Mem0Tools** - Optional conversation memory
*   **Professional Planning** - Comprehensive itinerary creation

### Travel Planning Process
1.  **Assessment** - Understand trip requirements and constraints
2.  **Research** - Validate destinations and gather current information
3.  **Accommodation** - Find suitable lodging options
4.  **Activities** - Curate experiences and attractions
5.  **Logistics** - Plan transportation and timing
6.  **Budget** - Optimize costs and provide breakdowns
7.  **Local Insights** - Include cultural tips and recommendations

---

> **🌐 Join the Internet of Agents**
> Register your agent at [bindus.directory](https://bindus.directory) to make it discoverable worldwide and enable agent-to-agent collaboration. **It takes 2 minutes and unlocks the full potential of your agent.**

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Paraschamoli/travel-agent.git
cd travel-agent

# Set up virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys:
OPENAI_API_KEY=sk-...      # For OpenAI GPT-4o (or)
OPENROUTER_API_KEY=sk-...  # For OpenRouter (alternative)
EXA_API_KEY=sk-...         # REQUIRED: Get from https://exa.ai
MEM0_API_KEY=sk-...        # Optional: For conversation memory
```

### 3. Run Locally

```bash
# Start the travel agent
python travel_agent/main.py

# Or using uv
uv run python travel_agent/main.py
```

### 4. Test with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at: http://localhost:3773
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file:

```env
# Required APIs
EXA_API_KEY=sk-...           # Required for destination research

# Choose ONE LLM provider
OPENAI_API_KEY=sk-...        # OpenAI API key
OPENROUTER_API_KEY=sk-...    # OpenRouter API key (alternative)

# Optional features
MODEL_NAME=openai/gpt-4o     # Model ID for OpenRouter
MEM0_API_KEY=sk-...          # Optional: For memory operations
```

### Port Configuration
Default port: `3773` (can be changed in `agent_config.json`)

## 💡 Usage Examples

### Via HTTP API

```bash
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Plan a 5-day cultural exploration trip to Kyoto for a family of 4 with a $4000 budget"
      }
    ]
  }'
```

### Sample Travel Planning Queries

```text
"Create a romantic weekend getaway in Paris with a $2000 budget"
"Organize a 7-day adventure trip to New Zealand for solo travel"
"Design a tech company offsite in Barcelona for 20 people"
"Plan a luxury honeymoon in Maldives for 10 days"
"Plan a team-building retreat in Costa Rica for 25 people"
"Design a food and wine exploration in Tuscany"
"Create a hiking expedition in Patagonia"
"Organize a wellness retreat in Bali for 15 employees"
"Plan a traditional arts and crafts tour in Kyoto"
```

### Expected Response Format

```markdown
# Kyoto Family Cultural Trip (5 Days) 🇯🇵

## 📋 Trip Overview
- **Dates**: June 15-20, 2024
- **Duration**: 5 days
- **Group**: Family of 4 (2 adults, 2 children ages 8 & 10)
- **Budget Range**: $3500-$4000
- **Travel Style**: Family Cultural Immersion
- **Focus**: Temples, traditional arts, family-friendly experiences

## 🏨 Recommended Accommodation

**Traditional Machiya House in Gion District**
- Authentic Japanese townhouse experience
- 3 bedrooms, kitchen, traditional garden
- Walking distance to major temples and attractions
- Estimated: $180/night on Airbnb
- **Booking Platform**: Airbnb (book 2-3 months in advance)

### Alternative Options:
1. **Family Suite in Downtown Hotel** - Modern amenities, $200/night
2. **Ryokan with Onsen** - Traditional inn, $250/night (luxury option)

## 📅 Daily Itinerary

### Day 1: Arrival & Gion District
**Theme**: Introduction to Traditional Kyoto

| Time | Activity | Location | Details | Estimated Cost |
|------|----------|----------|---------|----------------|
| 14:00 | Check-in | Machiya House | Settle into accommodation | Included |
| 16:00 | Gion Walk | Gion District | See geisha district, traditional architecture | Free |
| 18:00 | Welcome Dinner | Pontocho Alley | Try Kyoto specialties: yudofu, kaiseki | $80/family |

**Day 1 Tips**: Wear comfortable shoes for walking. Gion is most atmospheric in early evening.

### Day 2: Temple Exploration
**Theme**: Spiritual Kyoto

| Time | Activity | Location | Details | Estimated Cost |
|------|----------|----------|---------|----------------|
| 09:00 | Kinkaku-ji | Golden Pavilion | Morning visit to avoid crowds | $6/adult, $3/child |
| 11:00 | Ryoan-ji | Rock Garden | Zen meditation garden experience | $5/adult, $2.50/child |
| 14:00 | Family Kimono Rental | Downtown Kyoto | Traditional dress experience | $50/family (1 hour) |

[Continue for Days 3-5...]

## 💰 Comprehensive Budget Breakdown

| Category | Estimated Cost | Notes |
|----------|----------------|-------|
| Accommodation | $900 | 5 nights at $180/night |
| Local Transportation | $200 | Buses, trains, taxis |
| Activities & Entry Fees | $600 | Temples, museums, experiences |
| Food & Dining | $800 | Mix of local restaurants and markets |
| Souvenirs & Miscellaneous | $300 | Traditional crafts, gifts |
| **Total Estimated** | **$2800** | **$1200 under budget** |

## 🚗 Logistics & Transportation

### Getting to Kyoto:
- **From Tokyo**: Shinkansen (bullet train) - 2.5 hours, $130/person
- **From Osaka**: Local train - 30 minutes, $5/person

### Local Transportation:
- **Kyoto City Bus Pass**: $5/day for unlimited travel
- **Bicycle Rental**: $10/day - great for exploring flat areas
- **Taxi**: Available but expensive, use for luggage transport

## 📋 Booking Requirements & Timeline

**Immediate Action (Now):**
- Research flight options to Kansai International Airport (KIX)
- Check visa requirements for Japan

**Book Within 3 Months:**
- Reserve accommodation (popular machiya houses book early)
- Purchase Shinkansen tickets if traveling from Tokyo

**Book Within 1 Month:**
- Reserve specific restaurant meals (kaiseki restaurants require advance booking)
- Purchase Japan Rail Pass if applicable

## 🗺️ Local Tips & Cultural Insights

### Cultural Etiquette:
- Remove shoes when entering traditional buildings
- Bow slightly when greeting (not necessary for tourists but appreciated)
- Speak quietly in temples and gardens

### Dining Tips:
- Try **kaiseki** (multi-course traditional meal) at least once
- **Nishiki Market** for street food and local ingredients
- Convenience stores (7-Eleven, FamilyMart) have surprisingly good food

### Family-Friendly Advice:
- Many temples have English explanations and family facilities
- Afternoon naps help with jet lag adjustment
- Carry snacks for children between meals

## ⚠️ Important Considerations

### Weather & Seasonal Notes:
- **June**: Start of rainy season, pack umbrellas and light rain jackets
- **Temperature**: 20-28°C (68-82°F), humid
- **Best viewing**: Hydrangea season in temples

### Health & Safety:
- Japan has excellent healthcare, but travel insurance recommended
- Tap water is safe to drink everywhere
- Pharmacies (yakkyoku) available for minor ailments

### Contingency Plans:
- **Rainy Day Alternatives**: Kyoto Railway Museum, Nintendo Museum, indoor markets
- **Crowd Avoidance**: Visit popular temples early morning (before 9 AM)
- **Rest Days**: Plan lighter activity days (Day 3 is designed as flexible)

---

*Itinerary curated by Globe Hopper Travel Planning* 🌍
*Last Updated: 2024-01-15*
*Note: Prices and availability subject to change. Always verify current information before booking.*
```

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Build the image
docker build -t travel-agent .

# Run container
docker run -d \
  -p 3773:3773 \
  -e EXA_API_KEY=your_exa_key \
  -e OPENAI_API_KEY=your_openai_key \
  -e MEM0_API_KEY=your_mem0_key \
  --name travel-agent \
  travel-agent

# Check logs
docker logs -f travel-agent
```

### Docker Compose (Recommended)

`docker-compose.yml`:

```yaml
version: '3.8'
services:
  travel-agent:
    build: .
    ports:
      - "3773:3773"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
      - EXA_API_KEY=${EXA_API_KEY}
      - MEM0_API_KEY=${MEM0_API_KEY}
    restart: unless-stopped
```

Run with Compose:

```bash
# Start with compose
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📁 Project Structure

```text
travel-agent/
├── travel_agent/
│   ├── skills/
│   │   └── travel-planner/
│   │       ├── skill.yaml          # Skill configuration
│   │       └── __init__.py
│   ├── __init__.py
│   └── main.py                     # Agent entry point
├── agent_config.json               # Bindu agent configuration
├── pyproject.toml                  # Python dependencies
├── Dockerfile                      # Multi-stage Docker build
├── docker-compose.yml              # Docker Compose setup
├── README.md                       # This documentation
├── .env.example                    # Environment template
└── tests/                          # Test suite
```

## 🔌 API Reference

### Health Check

```bash
GET http://localhost:3773/health
```

Response:
```json
{"status": "healthy", "agent": "Travel Agent"}
```

### Chat Endpoint

```bash
POST http://localhost:3773/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Your travel planning query here"}
  ]
}
```

## 🧪 Testing

### Local Testing

```bash
# Install test dependencies
uv sync --group dev

# Run tests
pytest tests/

# Test with coverage
pytest --cov=travel_agent tests/
```

### Integration Test

```bash
# Start agent
python travel_agent/main.py &

# Test API endpoint
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Plan weekend trip to Tokyo"}]}'
```

## 🚨 Troubleshooting

### Common Issues & Solutions

**"EXA_API_KEY required"**
Get your key from: https://exa.ai - This is required for destination research

**"No LLM API key provided"**
Set either `OPENAI_API_KEY` or `OPENROUTER_API_KEY` in your `.env` file

**"Port 3773 already in use"**
Change port in `agent_config.json` or kill the process:
```bash
lsof -ti:3773 | xargs kill -9
```

**Docker build fails**
```bash
docker system prune -a
docker-compose build --no-cache
```

**MCP tool connection issues**
Ensure Node.js/npx is available if using MCP tools, or disable them

## 📊 Dependencies

### Core Packages
*   **bindu** - Agent deployment framework
*   **agno** - AI agent framework
*   **exa-py** - Exa research API
*   **openai** - OpenAI client
*   **python-dotenv** - Environment management
*   **mem0ai** - Memory operations
*   **fastmcp** - MCP tool integration

### Development Packages
*   **pytest** - Testing framework
*   **ruff** - Code formatting/linting
*   **pre-commit** - Git hooks

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  Fork the repository
2.  Create a feature branch: `git checkout -b feature/improvement`
3.  Make your changes following the code style
4.  Add tests for new functionality
5.  Commit with descriptive messages
6.  Push to your fork
7.  Open a Pull Request

**Code Style:**
*   Follow PEP 8 conventions
*   Use type hints where possible
*   Add docstrings for public functions
*   Keep functions focused and small

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Credits & Acknowledgments

*   **Developer:** Paras Chamoli
*   **Framework:** Bindu - Agent deployment platform
*   **Agent Framework:** Agno - AI agent toolkit
*   **Research Engine:** Exa - Destination research API
*   **Memory System:** Mem0 - Conversation memory API

## 🔗 Useful Links
*   🌐 **Bindu Directory:** [bindus.directory](https://bindus.directory)
*   📚 **Bindu Docs:** [docs.getbindu.com](https://docs.getbindu.com)
*   🐙 **GitHub:** [github.com/ParasChamoli/travel-agent](https://github.com/ParasChamoli/travel-agent)
*   💬 **Discord:** Bindu Community

<br/>

<p align="center">
  <strong>Built with ❤️ by Paras Chamoli</strong><br/>
  <em>Making travel planning effortless and comprehensive</em>
</p>

<p align="center">
  <a href="https://github.com/ParasChamoli/travel-agent/stargazers">⭐ Star on GitHub</a> •
  <a href="https://bindus.directory">🌐 Register on Bindu</a> •
  <a href="https://github.com/ParasChamoli/travel-agent/issues">🐛 Report Issues</a>
</p>

---
*Note: This agent provides travel planning and research services. It does not handle actual bookings, payments, or real-time availability. Always verify information with official sources before making travel arrangements. Powered by AI with comprehensive destination research capabilities.*

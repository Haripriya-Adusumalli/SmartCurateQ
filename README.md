# AI Startup Evaluator 🚀

An AI-powered platform that evaluates startups by synthesizing founder materials and public data to generate concise, actionable investment insights.

## Features

### 🤖 Multi-Agent Architecture
- **Data Extraction Agent**: Processes pitch decks, forms, and documents
- **Mapping Agent**: Structures data into standardized startup profiles  
- **Analysis Agent**: Generates investment scores and recommendations
- **Public Data Agent**: Enriches analysis with external market data

### 📊 Comprehensive Analysis
- **Founder Profiles**: Founder-market fit scoring
- **Market Analysis**: Size, growth, competition assessment
- **Business Metrics**: Revenue, traction, KPI evaluation
- **Risk Assessment**: Automated red flag detection
- **Investment Scoring**: Weighted scoring based on investor preferences

### 🎯 Key Capabilities
- Process PDF pitch decks and Google Form submissions
- Benchmark against sector peers and market data
- Flag risk indicators (inconsistent metrics, inflated claims)
- Generate investor-ready deal notes
- Customizable weighting for different investment criteria

## Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Environment Setup
```bash
# Set your Google AI API key
export GEMINI_API_KEY="your_api_key_here"
export GOOGLE_CLOUD_PROJECT="your_project_id"
```

### Run the Application
```bash
streamlit run app.py
```

## Usage

### Single Startup Evaluation
```python
from startup_evaluator import StartupEvaluator
from config import InvestorPreferences

# Initialize evaluator
evaluator = StartupEvaluator()

# Set investor preferences
preferences = InvestorPreferences(
    founder_weight=0.3,
    market_weight=0.25,
    differentiation_weight=0.25,
    traction_weight=0.2
)

# Evaluate startup
memo = evaluator.evaluate_startup(
    pitch_deck_path="path/to/deck.pdf",
    form_data=form_responses,
    investor_preferences=preferences
)

print(f"Investment Score: {memo.investment_score}/10")
print(f"Recommendation: {memo.recommendation}")
```

### Batch Processing
```python
startup_data_list = [
    {"pitch_deck_path": "deck1.pdf"},
    {"form_data": form_data_2},
    # ... more startups
]

results = evaluator.batch_evaluate(startup_data_list, preferences)
```

## Architecture

### Data Flow
1. **Input**: Pitch decks (PDF), Google Forms, public data
2. **Extraction**: AI-powered content extraction and structuring
3. **Enrichment**: Public data integration and claim verification
4. **Analysis**: Multi-factor scoring and risk assessment
5. **Output**: Investment memo with actionable insights

### Scoring Framework
- **Founder Score** (0-10): Experience, domain fit, track record
- **Market Score** (0-10): Size, growth rate, competition level
- **Differentiation Score** (0-10): Uniqueness, defensibility, IP
- **Traction Score** (0-10): Revenue, growth, key metrics

### Risk Detection
- Inconsistent financial metrics
- Inflated market size claims
- High customer churn patterns
- Weak founder-market alignment
- Intense competitive pressure

## Sample Output

```markdown
# Investment Deal Note: AI Analytics Corp

## Executive Summary
**Investment Score:** 7.8/10
**Recommendation:** BUY - Good opportunity with acceptable risk profile
**Risk Level:** MEDIUM

## Team/Founder Summary
- **Sarah Chen**: Former McKinsey consultant with 8 years in data analytics (Founder-Market Fit: 8.2/10)

## Market Analysis
- **Market Size:** $15,000,000,000
- **Growth Rate:** 15.0%
- **Competition Level:** medium
- **Key Players:** Tableau, PowerBI, Looker

## Key Strengths
- Strong founder-market fit
- Large addressable market
- Revenue generating

## Key Concerns
- Competitive market landscape
- Scaling challenges ahead
```

## Configuration

Customize analysis parameters in `config.py`:
- Market size thresholds
- Revenue growth benchmarks
- Risk indicator definitions
- Scoring weights

## Tech Stack

- **AI/ML**: Google Gemini, Vertex AI
- **Data Processing**: PyPDF2, pandas
- **Web Interface**: Streamlit
- **Cloud Services**: Google Cloud Vision, BigQuery
- **Backend**: Python, Pydantic models

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-agent`)
3. Commit changes (`git commit -am 'Add new analysis agent'`)
4. Push to branch (`git push origin feature/new-agent`)
5. Create Pull Request

## License

MIT License - see LICENSE file for details.

---

*Built for the GenAI Exchange Hackathon 2025*
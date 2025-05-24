# 🌤️ Weather Agent

A powerful weather assistant built using OpenAI's Agent SDK that provides detailed weather information for any location worldwide. This agent uses multiple APIs to deliver accurate and comprehensive weather data.

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![OpenAI Agents](https://img.shields.io/badge/OpenAI%20Agents-SDK-orange)](https://github.com/openai/openai-python)

## ✨ Features

- 🔍 Location-based weather information
- 🌡️ Detailed temperature data (current, feels like, min/max)
- 💨 Wind speed and direction
- 💧 Humidity and pressure readings
- ☁️ Cloud coverage information
- 🌅 Sunrise and sunset times
- 🌧️ Rainfall predictions
- 👁️ Visibility information

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- API keys for:
  - [OpenWeather API](https://openweathermap.org/api)
  - [OpenCage Geocoding](https://opencagedata.com/dashboard)
  - [Google Gemini](https://aistudio.google.com/apikey)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Muhammadzainattiq/OpenAI-Agent-SDK-Weather-Agent
cd weather-agent
```

2. Create and configure your environment:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
# OPEN_WEATHER_API_KEY=your_key_here
# OPEN_CAGE_API_KEY=your_key_here
# GEMINI_API_KEY=your_key_here
```

3. Install dependencies:
```bash
uv sync
```

4. Run the agent:
```bash
uv run agent.py
```

## 💡 Usage Examples

The agent can handle various weather-related queries:

```bash
Enter the query: What's the weather like in London?
Enter the query: Will it rain in Tokyo tomorrow?
Enter the query: What's the temperature in New York?
```

## 🔧 Configuration

The agent uses three main APIs:

1. **OpenWeather API**: Provides detailed weather data
2. **OpenCage Geocoding**: Converts location names to coordinates
3. **Google Gemini**: Powers the AI assistant capabilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the Agent SDK
- OpenWeather for weather data
- OpenCage for geocoding services
- Google for Gemini AI capabilities
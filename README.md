## Project Run Commands
Create a .env file in root folder and paste your API keys
```
OPENAI_API_KEY = XXXXXX
GOOGLE_API_KEY = XXXXXX
WEATHER_API_KEY = XXXXXX
AI_MODEL = openai/gpt-4.1-mini
```
<br>

### Goto root folder and run the following commands :

To run backend (fastApi)
```
poetry run uvicorn src.my_vacation.main:app --reload
```

To run frontend (streamlit)
```
poetry run streamlit run src/my_vacation/app.py
```
<br><br>
## Overview
![Demo](assets/demo.gif)

## Notes

<br><br>

## Development Task List
- ✅ Set up project structure
- ✅ Initialize Poetry environment
- ✅ Develop FastApi backend
- ✅ Develop streamlit frontend
- ✅ Add open AI Api connection
- ✅ Add Google Places Api connection
- ✅ Add OpenWeatherMap Api connection

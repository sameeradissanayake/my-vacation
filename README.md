## Project Run Commands
Goto root folder and run the following commands :

To run backend (fastApi)
```
poetry run uvicorn src.my_vacation.main:app --reload
```

To run frontend (streamlit)
```
poetry run streamlit run src/my_vacation/app.py
```
<br><br>

![Demo](assets/demo.gif)

## Notes

Create a .env file in root folder and paste your API keys
```
OPENAI_API_KEY = XXXXXX
GOOGLE_API_KEY = XXXXXX
WEATHER_API_KEY = XXXXXX
AI_MODEL = openai/gpt-4.1-mini
```

## Development Task List
- [x] Set up project structure
- [x] Initialize Poetry environment
- [x] Develop FastApi backend
- [x] Develop streamlit frontend
- [x] Add open AI Api connection
- [x] Add Google Places Api connection
- [x] Add OpenWeatherMap Api connection

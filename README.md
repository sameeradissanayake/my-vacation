## Project Run Commands
Goto root folder and run the command :
```
poetry run uvicorn src.my_vacation.main:app --reload
```

## Notes

Add .env file to root folder and paste your API keys
```
OPENAI_API_KEY = XXXXXX
GOOGLE_API_KEY = XXXXXX
```
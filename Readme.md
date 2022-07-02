# Instructions to Run locally
1. Install [Python](https://www.python.org/downloads/).
2. Clone this repository and open terminal, change directory to the repo.
3. Run `python -m venv venv` to create virtual environment.
4. Run `venv\Scripts\activate` command to activate virtual environment.
5. Run `pip install -r reqirements.txt` command to install dependencies.
6. Run `uvicorn app:app --host 127.0.0.1 --port 8000`
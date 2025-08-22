Project MonteCarloTau - scaffold

Components:
- `cpp/` - example C++ code
- `pythonapi/` - Flask server + pybind11 C++ extension
- `electron-app/` - Electron + TypeScript minimal visualizer

Quick start (high level):

1) Install dependencies

- Python: create venv and install requirements
  - python -m venv .venv
  - source .venv/bin/activate  # or .venv\Scripts\Activate on Windows PowerShell
  - pip install -r pythonapi/requirements.txt

- Build C++ extension (from repo root):
  - cd pythonapi
  - python setup.py build_ext --inplace

- Run Flask server:
  - python pythonapi/src/app.py

- Run Electron app:
  - cd electron-app
  - npm install
  - npm run build
  - npm start
# MonteCarloTau

a tool to visualize the evolution of $\tau$ (https://www.tauday.com/) with Monte Carlo.

A code to practice interfacing C++, Python and TS > Python Backend Dev <3

# Flights-Shiny

This repository contains the coursework for the _Models Deployment_ subject (pl. _Wdrażanie modeli uczenia maszynowego_). It features an interactive web application that showcases flight routes and statistical data on flights across the United States.


https://github.com/piotrulo022/Flights-Shiny/assets/76213314/e270c3c7-7293-4452-a29d-14d3fc981c2b



# Tools and Technologies
This application is built using the Shiny framework, renowned for its high level of customization and dynamic reactivity. Shiny's robust environment allows for the seamless integration of interactive UI components with backend R or Python computations, making it an ideal choice for data-rich web applications.


# Deployment

## App hosted on shinyapps.io
Application is available at: https://pszyszka.shinyapps.io/us-flights/



## Local deployment (requires python== 3.10)

Open your favourite shell in your favourite terminal emulator and :
1. clone the repository
```bash
git clone https://github.com/piotrulo022/US-Flights-webapp.git
cd US-Flights-webapp/ # enter project directory
```

2. prepare virtual environment - use already existing with packages specified in `requirements.txt` or create new virtual environment
with `conda`:


- with `conda`; example of creating venv named *usflights*:
```
# 0) create python virtual environment
conda create -n usflights python==3.10

# 1) activate created environment
conda activate usflights 

# 2) install dependencies
pip install -r requirements.txt
```
 - with built in pythons virtualenvs:
```
# 0) create python virtual environment
python -m ./pyenv

# 1) activate created environment

# Run one of these, depending on shell you use:
source ./pyenv/bin/activate # bash/zsh
source ./pyenv/bin/activate.fish # fish 
source ./pyenv/bin/activate.csv # csh/tcsh

.pyenv\Scripts\activate.bat # Windows cmd.exe
.pyenv\Scripts\Activate.ps1 # Windows PowerShell

# 2) install dependencies
pip install -r requirements.txt
```

3. run the application; example of running on `8000` TCP port:
```bash
shiny run 
shiny run --port 8000 --reload app.py
```

4. open `http://localhost:8000/` in your favourite web browser and enjoy the application :)




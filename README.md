# US Flights webapp

This repository contains the coursework for the _Models Deployment_ subject (pl. _Wdrażanie modeli uczenia maszynowego_). It features an interactive web application that showcases flight routes and statistical data on flights across the United States.

https://github.com/piotrulo022/Flights-Shiny/assets/76213314/e270c3c7-7293-4452-a29d-14d3fc981c2b

# Goals of the project

The primary objective of this project is to develop an intuitive and engaging web application for exploring a dataset of flights across the U.S. The project aims to meet the following specific goals:


- [x] create a responsive and lightweight application -  design a web application that is not only user-friendly and adaptable to various devices but also streamlined to avoid unnecessary bloat,

- [x] maintain code simplicity and efficiency - ensure the application provides valuable features while keeping the codebase simple, efficient, and easy to understand,

- [x] scalability and maintainability -  develop the application with a focus on scalability and ease of maintenance, allowing for future enhancements and updates without major overhauls,

- [x] interactive data visualization -  implement interactive components that allow users to explore and visualize flight data dynamically, enhancing their understanding through visual aids,

- [x] statistical insights - provide insightful statistical analysis and visualizations to highlight trends, patterns, and key metrics within the flight data.


# Tools and Technologies
This application is developed using the Shiny for Python framework, specifically leveraging the Shiny Express module. Known for its exceptional customization capabilities and dynamic reactivity, Shiny provides a robust environment that seamlessly integrates interactive UI components with backend computations, whether in R or Python. This makes it an excellent choice for building data-intensive web applications.

At the heart of this project is the comprehensive dataset detailing airline flight delays and cancellations from 2019 to 2023, provided by the U.S. Department of Transportation's Bureau of Transportation Statistics. This dataset is a rich source of information and can be accessed through the following [link](https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023).


# Deployment

## App hosted on shinyapps.io
Application is available at: https://pszyszka.shinyapps.io/us-flights/


## Local deployment (requires python)

Open your favourite terminal emulator and follow these steps:

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

```bash
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
shiny run --port 8000 --reload app.py
```

4. open `http://localhost:8000/` in web browser and enjoy the application :)


# Conclusions and future plans

Working on this project has significantly enhanced my understanding of building interactive web applications. This skill is invaluable for a data scientist, as it enables the presentation of models and statistical analyses to non-programmers in a user-friendly manner. With the increasing prevalence of web-based applications over desktop solutions, mastering this technology is not only relevant but also advantageous for career development.

Looking ahead, I plan to:

- [x] enchance functionality of the app - add more sophisticated features and data analysis tools,

- [x] expand data sources - extend the application’s scope to include flight data from other continents, making it a global tool rather than one limited to the U.S.

- [x] implement more advanced visualizations -  develop more sophisticated visualization techniques to uncover hidden patterns and present richer, more detailed insights from the data.

- [ ] separate different compontents into seperate files for cleaner code - unfortunately shinyexpress does not support modules and shared reactivity within session yet and this might lead to hard to maintain code when application gets larger


# References

[1] Majerek D., *Wdrażanie modeli uczenia maszynowego*, https://dax44-models-deployment.netlify.app/, Accessed 28.06.2024,

[2] Shiny - easy web apps for data science without the compromises, https://shiny.posit.co/, Accessed 28.06.2024,

[3] Shiny Express API, https://shiny.posit.co/py/api/express/, Accessed 28.06.2024,

[4] U.S. Department of Transportation, Bureau of Transportation Statistics, On-Time : Reporting Carrier On-Time Performance (1987-present), https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFD&Yv0x=D, Accessed 28.06.2024.


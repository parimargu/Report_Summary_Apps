#!/bin/bash

# Project root folder
PROJECT_ROOT="streamlit_ppt_summary"

# Create main project folder
mkdir -p $PROJECT_ROOT

# Navigate into project folder
cd $PROJECT_ROOT || exit

# Create main app file
touch app.py

# Create requirements file
touch requirements.txt

# Create configuration file
touch config.yaml

# Create prompt template file
touch prompt_template.txt

# Create log file (empty initially)
touch app.log

# Create sample pptx file placeholder
touch sample_loan_forecast.pptx

# Create modules folder and module files
mkdir -p modules
touch modules/file_handler.py
touch modules/ppt_parser.py
touch modules/llm_handler.py
touch modules/ui_renderer.py
touch modules/config_manager.py

# Create tests folder and test files
mkdir -p tests
touch tests/test_file_handler.py
touch tests/test_ppt_parser.py
touch tests/test_llm_handler.py
touch tests/test_ui_renderer.py
touch tests/test_config_manager.py

# Print success message
echo "Project structure for '$PROJECT_ROOT' created successfully!"

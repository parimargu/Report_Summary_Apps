#!/bin/bash

# Project root directory
PROJECT_DIR="ppt-summarizer"

# Create main project directory
mkdir -p "$PROJECT_DIR"

# Navigate into project directory
cd "$PROJECT_DIR" || exit

# Create main files
touch app.py config.yaml prompt_template.txt requirements.txt .env.example README.md app.log

# Create modules directory and files
mkdir -p modules
touch modules/__init__.py \
      modules/config_manager.py \
      modules/file_parser.py \
      modules/content_extractor.py \
      modules/llm_service.py \
      modules/ui_renderer.py \
      modules/logger.py

# Create tests directory and files
mkdir -p tests
touch tests/__init__.py \
      tests/test_config_manager.py \
      tests/test_file_parser.py \
      tests/test_content_extractor.py \
      tests/test_llm_service.py \
      tests/conftest.py

# Create sample_data directory and placeholder sample pptx
mkdir -p sample_data
touch sample_data/sample_loan_forecast.pptx

# Print success message
echo "Project structure for '$PROJECT_DIR' created successfully."

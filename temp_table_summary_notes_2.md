Please do spell check and rephrase the below project requirements for the production grade applicarion : ```i want to create highly responsive and rich looking python streamlit application where user upload a .ppt or pptx document, system should read the ppt or pptx document, then iterate the each slide and extract the content table content separately, paragraph text content separately. then split the page into left and right side, show the paragraph text content in the left side of the page and table content in the right side of the page. then create a "Generate Table Summary" button , on click this button, application should take the table content in the right side, then create the summary for this table content using LLM model(use Groq LLM provider, i.e. pyhton SDK groq package) and then show the summary in well formatted bullet points in the bottom of table content section. the .ppt or.pptx document is quarterly loss forecasting/prediction of loans for different bank loan segments like commercial banking. it will have two important values like loan default rate in pencentage and net rate in percentage . the table content summary should be or particulary for negative values or red bold values of default rate and net rate. please highly modularize application code, include python logging for entire application , include python exception handling. include configuration file and read metadata from that configuration file. create production level prompt template file with prompting best practices, prompting best practices should be like use role, system role, few shot prompting technique and other best performing promting techniques, read the prompt template and used it for getting teble content summaring while calling llm. please include sample .ppt or .pptx file for evlauating or testing. Please include unit test cases using pytest for entire application code.```


=============
=============


Here’s a **professionally rephrased and spell-checked** version of your project requirements — rewritten in a clear, structured, and production-grade manner suitable for documentation, specifications, or development handover.

---

# 🧩 **Project Requirements — Streamlit-Based PowerPoint Content Summarization Application**

## **1. Objective**

Develop a **highly responsive, visually rich, and modular Streamlit application** in Python that enables users to upload PowerPoint presentations (`.ppt` or `.pptx`), automatically extract slide content, and generate AI-powered summaries of table data using the **Groq LLM Python SDK** (`groq` package).

The uploaded presentations represent **quarterly loss forecasting or loan prediction reports** for various **banking segments** (e.g., commercial banking).
Each report includes two key financial metrics:

* **Loan Default Rate (%)**
* **Net Rate (%)**

---

## **2. Functional Requirements**

### **2.1 File Upload**

* Users should be able to upload `.ppt` or `.pptx` documents through a Streamlit interface.
* The system must validate the file type before processing.

### **2.2 Content Extraction**

* The application should:

  * Parse the uploaded PowerPoint file.
  * Iterate through each slide.
  * Extract **paragraph text** and **table content** separately.
* Each slide’s extracted content should be processed independently.

### **2.3 User Interface Layout**

* The Streamlit page should be **split into two responsive panels**:

  * **Left Panel:** Display paragraph (text) content.
  * **Right Panel:** Display table data extracted from the same slide.
* The layout should adapt well to different screen sizes and maintain a clean, professional design.

### **2.4 Table Summary Generation**

* Include a **“Generate Table Summary”** button beneath each table view.

* On clicking the button:

  1. The application takes the table data shown on the right panel.
  2. Sends it to the **Groq LLM API** (via the official `groq` Python SDK).
  3. Uses a structured prompt (loaded from a separate prompt template file) to generate a **summary of the table**.
  4. Displays the summary **below the table** in **well-formatted bullet points**.

* The summary must specifically emphasize:

  * **Negative values**
  * **Red or bold entries**
  * **Abnormal Loan Default Rate (%)** and **Net Rate (%)** trends.

---

## **3. Technical Requirements**

### **3.1 Architecture and Modularity**

* The codebase must follow a **modular architecture**, separating concerns across different modules such as:

  * File parsing and slide reading
  * Text and table extraction
  * LLM integration
  * UI rendering
  * Configuration and logging management
* Each module should be independently testable.

### **3.2 Configuration Management**

* Use an external **configuration file** (`config.yaml` or JSON) to store:

  * LLM model configuration (model name, API key, etc.)
  * Application metadata (name, version)
  * Logging preferences
* The application should dynamically read all configuration values at runtime.

### **3.3 Logging and Exception Handling**

* Implement **centralized Python logging** throughout the application:

  * Capture information, warning, and error logs.
  * Write logs to both the console and a log file (e.g., `app.log`).
* Include **robust exception handling**:

  * Catch and handle invalid file formats, missing data, and API errors.
  * Display user-friendly messages in the Streamlit UI.
  * Log detailed stack traces for debugging.

### **3.4 Prompt Template and Prompt Engineering**

* Create a **production-level prompt template file** (`prompt_template.txt`) that follows **prompting best practices**, including:

  * **Role-based prompting** (`system`, `user`)
  * **Few-shot prompting** with example summaries
  * Clear and specific instructions to focus on **negative** or **high-risk** financial indicators
* The application should **read the prompt dynamically** at runtime and pass it to the Groq LLM during summarization.

### **3.5 LLM Integration**

* Use the **Groq Python SDK (`groq` package)** for calling the model.
* Implement:

  * **Retry logic** for rate-limit or transient API errors.
  * **Timeout handling** for slow responses.
  * **Asynchronous support** using `AsyncGroq` for non-blocking API calls.

### **3.6 Testing and Quality Assurance**

* Implement **unit tests using `pytest`** for all modules.
* Test coverage should include:

  * File upload and validation logic
  * PowerPoint parsing and content extraction
  * LLM summarization (mocking Groq SDK calls)
  * Configuration loading
  * Error handling and logging
* Tests should be reproducible and not depend on actual Groq API calls.

### **3.7 Sample Data**

* Include a **sample `.pptx` file** (`sample_loan_forecast.pptx`) for testing and demonstration.

  * The sample file should contain:

    * Text slides describing quarterly loan forecasts.
    * Tables containing “Loan Default Rate (%)” and “Net Rate (%)” data.
    * Some negative or highlighted values for summary testing.

---

## **4. Non-Functional Requirements**

| Category            | Requirement                                                               |
| ------------------- | ------------------------------------------------------------------------- |
| **Performance**     | Process files up to 5 MB and generate summaries in under 10 seconds.      |
| **Scalability**     | Modular code allows adding support for more file types or LLM providers.  |
| **Usability**       | Intuitive, visually appealing, and mobile-friendly Streamlit UI.          |
| **Reliability**     | Gracefully handle failed uploads, timeouts, and API limits.               |
| **Security**        | Use environment variables for API keys; do not store secrets in code.     |
| **Maintainability** | Code should follow PEP 8 and include docstrings for all public functions. |

---

## **5. Deliverables**

1. Complete Streamlit application source code (`.py` modules).
2. Configuration file (`config.yaml`).
3. Prompt template file (`prompt_template.txt`).
4. Centralized logging setup.
5. Unit test suite using `pytest`.
6. Sample `.pptx` file for testing.
7. Setup instructions (`README.md`).
8. Optional: Dockerfile for deployment.

---

## **6. Future Enhancements (Optional)**

* **Concurrent slide summarization** (parallel LLM calls using `asyncio.gather`).
* **Downloadable summary reports** (PDF/Word).
* **Trend visualization** (charts of default rates over time).
* Integration with **vector databases** or **document stores** for historical summaries.

---

Would you like me to convert this version into a **formal Software Requirements Specification (SRS)** format (with numbered sections, deliverables, and acceptance criteria) so it’s ready for project documentation or submission?


================
================

Excellent ✅ — here’s your rewritten project description as a **formal Software Requirements Specification (SRS)**, structured for professional submission or documentation.
It follows standard IEEE-style SRS organization with numbered sections, clear scope, deliverables, and acceptance criteria.

---

# 🧾 **Software Requirements Specification (SRS)**

## **Streamlit Application for PowerPoint Content Extraction and AI-Powered Table Summarization**

---

### **1. Introduction**

#### **1.1 Purpose**

The purpose of this document is to define the requirements for a **production-grade Python Streamlit application** that allows users to upload PowerPoint presentations (`.ppt` or `.pptx`), extract their slide contents, and generate concise AI-powered summaries of table data using the **Groq LLM Python SDK** (`groq` package).

The system is intended to help financial analysts and data professionals quickly identify insights—particularly **negative or abnormal financial values**—from **quarterly loan forecast** presentations.

---

#### **1.2 Scope**

The application will:

* Accept `.ppt` or `.pptx` files uploaded by users.
* Extract and display **paragraph text** and **table data** from each slide.
* Generate AI summaries of tables using the **Groq LLM model** via the `groq` SDK.
* Focus summaries on critical financial indicators such as **Loan Default Rate (%)** and **Net Rate (%)**, with attention to **negative** or **highlighted** (e.g., red or bold) values.

The application will be **highly modular, fault-tolerant, and production-ready**, with integrated logging, configuration management, exception handling, and test coverage using `pytest`.

---

#### **1.3 Definitions, Acronyms, and Abbreviations**

| Term  | Description                                          |
| ----- | ---------------------------------------------------- |
| LLM   | Large Language Model                                 |
| Groq  | AI provider and LLM platform used for summarization  |
| SDK   | Software Development Kit                             |
| UI    | User Interface                                       |
| YAML  | Yet Another Markup Language (used for configuration) |
| Async | Asynchronous (non-blocking) execution model          |

---

#### **1.4 References**

* Groq Python SDK Documentation: [https://console.groq.com/docs](https://console.groq.com/docs)
* Streamlit Documentation: [https://docs.streamlit.io](https://docs.streamlit.io)
* Python PEP 8 – Style Guide for Python Code
* IEEE 830-1998 – Recommended Practice for Software Requirements Specifications

---

#### **1.5 Overview**

This SRS outlines the functional, non-functional, and design requirements of the PowerPoint Summarization Application.
It also defines testing requirements, configuration details, and acceptance criteria for production readiness.

---

### **2. Overall Description**

#### **2.1 Product Perspective**

The system is a standalone Streamlit web application, built on top of Python’s `streamlit`, `python-pptx`, and `groq` libraries.
It will run locally or in a hosted environment (e.g., Streamlit Cloud, Docker, or AWS EC2).

---

#### **2.2 Product Features**

* Upload and parse PowerPoint files.
* Extract slide-by-slide content (text and tables).
* Display extracted content side-by-side (two-panel layout).
* Summarize table content via Groq LLM.
* Log all application events and handle exceptions gracefully.
* Read runtime configurations from external YAML files.
* Include complete unit test coverage with `pytest`.

---

#### **2.3 User Classes and Characteristics**

| User Type         | Description                                                     |
| ----------------- | --------------------------------------------------------------- |
| Financial Analyst | Reviews loan forecasts and uses AI summaries to identify risks. |
| Data Scientist    | Tests and extends the app for new LLM models or datasets.       |
| Developer         | Maintains and deploys the application.                          |

---

#### **2.4 Operating Environment**

* **Backend Language:** Python 3.10+
* **Framework:** Streamlit
* **LLM Provider:** Groq (via `groq` Python SDK)
* **Libraries:** `python-pptx`, `pandas`, `pyyaml`, `pytest`, `groq`, `streamlit`
* **Supported Platforms:** macOS, Windows, Linux
* **Deployment:** Local environment or Docker container

---

#### **2.5 Design and Implementation Constraints**

* Must use the **Groq Python SDK** for all LLM interactions.
* API keys must be securely managed via environment variables.
* The UI must remain responsive during asynchronous API calls.
* Prompt templates must be stored externally and follow best prompt-engineering practices.

---

#### **2.6 User Documentation**

A detailed `README.md` will be provided, including:

* Installation steps
* Configuration setup
* How to run the application
* Example workflow with screenshots

---

#### **2.7 Assumptions and Dependencies**

* Users have a valid **Groq API key** stored as an environment variable.
* The uploaded PowerPoint files are properly formatted (contain readable text and tables).
* Internet access is available for LLM API communication.

---

### **3. System Features**

#### **3.1 File Upload and Validation**

**Description:**
Allow users to upload `.ppt` or `.pptx` files for processing.

**Functional Requirements:**

1. The user shall be able to upload PowerPoint files through the Streamlit file uploader.
2. The system shall validate file types before parsing.
3. Invalid formats shall trigger an error message in the UI and log entry.

---

#### **3.2 Slide Content Extraction**

**Description:**
Extract and segregate content (text and tables) from each slide.

**Functional Requirements:**

1. The system shall iterate through each slide in the uploaded presentation.
2. Paragraph text and table content shall be extracted separately.
3. Extracted content shall be displayed in two responsive panels.

---

#### **3.3 Content Display Layout**

**Description:**
Display extracted content in a visually appealing, two-column layout.

**Functional Requirements:**

1. The left panel shall display paragraph (text) content.
2. The right panel shall display extracted tables in tabular form.
3. The layout shall be responsive for various screen sizes.

---

#### **3.4 Table Summarization**

**Description:**
Generate AI-driven summaries for table content using the Groq LLM.

**Functional Requirements:**

1. A “Generate Table Summary” button shall appear below each table.
2. On click, the system shall:

   * Send the table content to the Groq LLM.
   * Use a predefined prompt template to structure the query.
   * Display the resulting summary below the table in bullet points.
3. The summary shall emphasize negative or abnormal financial values.

---

#### **3.5 Prompt Template and LLM Integration**

**Description:**
Enable flexible, production-level prompting and LLM communication.

**Functional Requirements:**

1. The application shall read the prompt from an external text file.
2. The prompt shall include:

   * Role definitions (`system`, `user`)
   * Few-shot examples
   * Specific instructions for highlighting negative or red values
3. The app shall communicate with the **Groq LLM API** using the `groq` Python SDK.
4. The app shall handle:

   * Timeouts (default 20s)
   * API rate limits (retry with exponential backoff)
   * Asynchronous execution (`AsyncGroq`)

---

#### **3.6 Logging and Exception Handling**

**Description:**
Provide full visibility into system operations and handle errors gracefully.

**Functional Requirements:**

1. All modules shall use centralized Python logging.
2. Logs shall be written to both console and file (`app.log`).
3. Errors shall be caught, logged, and shown in a user-friendly format within the UI.

---

#### **3.7 Configuration Management**

**Description:**
Use external configuration to simplify deployment and customization.

**Functional Requirements:**

1. Configuration shall be stored in `config.yaml`.
2. It shall include:

   * LLM model name
   * Timeout and retry settings
   * Application metadata
3. The app shall dynamically read configurations at startup.

---

#### **3.8 Testing and Quality Assurance**

**Description:**
Ensure code quality and reliability through automated testing.

**Functional Requirements:**

1. Unit tests shall be implemented using `pytest`.
2. Tests shall cover:

   * File upload and parsing
   * Content extraction
   * LLM interaction (mocked Groq client)
   * Logging and exception handling
3. Test results shall report at least **90% code coverage**.

---

### **4. External Interface Requirements**

#### **4.1 User Interface**

* Implemented using Streamlit’s component-based layout system.
* Minimalist design with responsive columns and collapsible sections.
* Real-time feedback for long-running operations using `st.spinner`.

---

#### **4.2 Hardware Interfaces**

No specific hardware requirements; runs on standard computing environments.

---

#### **4.3 Software Interfaces**

| Interface     | Description                        |
| ------------- | ---------------------------------- |
| `groq` SDK    | Connects to Groq LLM API           |
| `python-pptx` | Reads and parses PowerPoint slides |
| `pandas`      | Displays and structures table data |
| `pytest`      | Handles automated testing          |

---

### **5. Non-Functional Requirements**

| Category            | Requirement                                                          |
| ------------------- | -------------------------------------------------------------------- |
| **Performance**     | Process files up to 5 MB and generate summaries in under 10 seconds. |
| **Scalability**     | Support adding new LLM providers or file types.                      |
| **Usability**       | Intuitive, mobile-friendly Streamlit UI.                             |
| **Maintainability** | Modular structure; follows PEP 8 standards.                          |
| **Security**        | Store API keys in environment variables only.                        |
| **Reliability**     | Retry failed LLM calls up to three times with exponential backoff.   |

---

### **6. Deliverables**

1. Streamlit application source code.
2. Configuration file (`config.yaml`).
3. Prompt template (`prompt_template.txt`).
4. Centralized logging module.
5. Unit tests (`pytest`).
6. Sample `.pptx` file for testing.
7. README file with setup and usage instructions.
8. Optional Dockerfile for deployment.

---

### **7. Acceptance Criteria**

| ID  | Criterion                                                   | Status |
| --- | ----------------------------------------------------------- | ------ |
| AC1 | Application uploads and parses `.pptx` files without error. | ☐      |
| AC2 | Extracted text and tables display correctly side by side.   | ☐      |
| AC3 | LLM-generated summaries focus on negative/abnormal values.  | ☐      |
| AC4 | Errors are logged and displayed gracefully in the UI.       | ☐      |
| AC5 | Unit tests run successfully with > 90% code coverage.       | ☐      |
| AC6 | Configuration and prompt templates load dynamically.        | ☐      |
| AC7 | Groq API calls handle rate limits and timeouts correctly.   | ☐      |

---

### **8. Future Enhancements**

* Parallel summarization of multiple slides using `asyncio.gather`.
* Downloadable summary reports in PDF or DOCX format.
* Visualization of trends (e.g., graphs for default rates).
* Integration with databases for storing historical summaries.

---

Would you like me to include this as a **formatted Markdown/Word export template** (ready for client submission with table of contents and cover page)?



================
================

Excellent ✅ — below is your **finalized Software Requirements Specification (SRS)** formatted in **professional Markdown**, ready for submission, client documentation, or export to Word/PDF.

It includes:

* A **cover page section**
* A **clickable Table of Contents** (when exported from Markdown to PDF or DOCX)
* Proper headers, formatting, and structure following **IEEE-style SRS best practices**

---

# 📘 **Software Requirements Specification (SRS)**

## **Streamlit Application for PowerPoint Content Extraction and AI-Powered Table Summarization**

---

### **Document Control**

| Version | Date       | Author                  | Description           |
| ------- | ---------- | ----------------------- | --------------------- |
| 1.0     | 2025-11-05 | [Your Name / Team Name] | Initial Draft of SRS  |
| 1.1     | TBD        | —                       | Reviewed and Approved |

---

### **Approval Signatures**

| Role           | Name | Signature | Date |
| -------------- | ---- | --------- | ---- |
| Project Owner  |      |           |      |
| Technical Lead |      |           |      |
| QA Lead        |      |           |      |

---

## 🧭 **Table of Contents**

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features](#3-system-features)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Deliverables](#6-deliverables)
7. [Acceptance Criteria](#7-acceptance-criteria)
8. [Future Enhancements](#8-future-enhancements)

---

## **1. Introduction**

### **1.1 Purpose**

This document defines the requirements for a **production-grade Python Streamlit application** that enables users to upload PowerPoint presentations (`.ppt` or `.pptx`), extract slide content, and generate concise AI-based summaries of table data using the **Groq LLM Python SDK** (`groq` package).

The system will support financial analysts and banking professionals in analyzing **quarterly loan forecast presentations** with a focus on highlighting **negative or abnormal financial indicators**.

---

### **1.2 Scope**

The application will:

* Accept and parse PowerPoint files (`.ppt`, `.pptx`).
* Extract text and table data from each slide.
* Display extracted content in a two-panel Streamlit interface.
* Generate AI summaries of table data using Groq’s LLM via the `groq` SDK.
* Emphasize **negative**, **red**, or **bold** financial values such as:

  * Loan Default Rate (%)
  * Net Rate (%)

The system will feature **modular architecture**, **robust error handling**, **asynchronous LLM integration**, and **pytest-based test coverage**.

---

### **1.3 Definitions, Acronyms, and Abbreviations**

| Term  | Definition                                              |
| ----- | ------------------------------------------------------- |
| LLM   | Large Language Model                                    |
| SDK   | Software Development Kit                                |
| Groq  | AI platform providing LLM inference services            |
| UI    | User Interface                                          |
| YAML  | Configuration file format (Yet Another Markup Language) |
| Async | Asynchronous execution (non-blocking)                   |
| API   | Application Programming Interface                       |

---

### **1.4 References**

* [Groq Python SDK Documentation](https://console.groq.com/docs)
* [Streamlit Documentation](https://docs.streamlit.io)
* [Python PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
* IEEE 830-1998 – Recommended Practice for Software Requirements Specifications

---

### **1.5 Overview**

This SRS specifies functional and non-functional requirements, external interface requirements, test expectations, and acceptance criteria for the PowerPoint Summarization Application.

---

## **2. Overall Description**

### **2.1 Product Perspective**

The application will be a **standalone Streamlit web app** running locally or on the cloud.
It will combine document parsing, text extraction, and LLM summarization into an interactive, responsive, and modular workflow.

---

### **2.2 Product Features**

* Upload `.ppt`/`.pptx` files.
* Extract and display text and tables from slides.
* Generate AI-driven summaries via Groq’s LLM API.
* Log operations and handle exceptions gracefully.
* Use YAML configuration and prompt templates.
* Include comprehensive pytest unit tests.

---

### **2.3 User Classes and Characteristics**

| User Type         | Description                                          |
| ----------------- | ---------------------------------------------------- |
| Financial Analyst | Uses the tool to analyze loan performance summaries. |
| Data Scientist    | Tests and integrates alternate LLM models.           |
| Developer         | Extends or deploys the system.                       |

---

### **2.4 Operating Environment**

| Component    | Requirement                                         |
| ------------ | --------------------------------------------------- |
| Language     | Python 3.10+                                        |
| Framework    | Streamlit                                           |
| LLM Provider | Groq                                                |
| Libraries    | `python-pptx`, `pandas`, `groq`, `pyyaml`, `pytest` |
| Platforms    | Windows, macOS, Linux                               |
| Deployment   | Local machine or Docker container                   |

---

### **2.5 Design and Implementation Constraints**

* Must use **Groq Python SDK** (`groq`) for LLM calls.
* Secrets (API keys) stored only in environment variables.
* Use `AsyncGroq` for non-blocking API calls.
* Prompt templates must be external and configurable.

---

### **2.6 User Documentation**

The `README.md` file will include:

* Installation and setup instructions
* Configuration and environment variable setup
* Step-by-step usage guide with screenshots
* Example PowerPoint file for testing

---

### **2.7 Assumptions and Dependencies**

* Users have valid **Groq API credentials**.
* The uploaded file follows proper PowerPoint structure.
* Stable internet connection is available for API access.

---

## **3. System Features**

### **3.1 File Upload and Validation**

**Description:**
Allows the user to upload `.ppt` or `.pptx` files for processing.

**Functional Requirements:**

1. Validate file extension before processing.
2. Display error messages for invalid or unreadable files.
3. Log file upload events and errors.

---

### **3.2 Slide Content Extraction**

**Description:**
Extract text and tables from each slide using `python-pptx`.

**Functional Requirements:**

1. Iterate through all slides.
2. Extract text (paragraphs, titles).
3. Extract and structure table data in pandas DataFrames.
4. Display extracted content slide-by-slide.

---

### **3.3 UI Layout and Display**

**Description:**
Render content using a **two-panel Streamlit layout**.

**Functional Requirements:**

1. Left panel: Paragraph text.
2. Right panel: Table data.
3. Include a “Generate Table Summary” button for each table.
4. Maintain responsive layout across devices.

---

### **3.4 Table Summarization**

**Description:**
Generate summaries for extracted table data using **Groq LLM**.

**Functional Requirements:**

1. Send table content as input to Groq LLM.
2. Read prompt template from external file.
3. Highlight abnormal, negative, or red/bold values.
4. Display summary as well-formatted bullet points under the table.

---

### **3.5 Prompt Template and LLM Integration**

**Description:**
Ensure structured and configurable communication with the Groq model.

**Functional Requirements:**

1. Read the prompt from an external `.txt` file.
2. Include:

   * Role-based prompting (`system`, `user`)
   * Few-shot examples
   * Clear financial analysis instructions
3. Support retries for rate limits and connection issues.
4. Timeout gracefully with error messages in the UI.
5. Implement asynchronous requests via `AsyncGroq`.

---

### **3.6 Logging and Exception Handling**

**Functional Requirements:**

1. Log all activities to both console and `app.log`.
2. Log levels: INFO, WARNING, ERROR, DEBUG.
3. Use centralized logger via `logging` module.
4. Display concise, user-friendly error messages in Streamlit.
5. Record full exception tracebacks in logs.

---

### **3.7 Configuration Management**

**Functional Requirements:**

1. Load settings from `config.yaml`.
2. Support:

   * Model name and version
   * Retry and timeout configuration
   * API key environment variable name
3. Read configurations dynamically at runtime.

---

### **3.8 Testing and Quality Assurance**

**Functional Requirements:**

1. Use `pytest` for automated unit testing.
2. Include mock tests for Groq API interactions.
3. Ensure 90%+ code coverage.
4. Test file upload, extraction, and summarization workflows.
5. Use sample PowerPoint files for reproducible tests.

---

## **4. External Interface Requirements**

### **4.1 User Interface**

* Implemented with Streamlit components (`st.file_uploader`, `st.columns`, `st.button`, etc.).
* Include progress spinners during LLM processing.
* Support dark/light theme modes.

---

### **4.2 Software Interfaces**

| Interface     | Purpose               |
| ------------- | --------------------- |
| `groq` SDK    | AI summarization API  |
| `python-pptx` | PowerPoint parsing    |
| `pandas`      | Table data processing |
| `pytest`      | Testing framework     |
| `pyyaml`      | Config management     |

---

### **4.3 Hardware Interfaces**

* Runs on any modern laptop or server.
* No specific hardware dependency.

---

## **5. Non-Functional Requirements**

| Category            | Requirement                                         |
| ------------------- | --------------------------------------------------- |
| **Performance**     | Process `.pptx` ≤ 5MB in <10 seconds.               |
| **Scalability**     | Support additional LLM providers in future.         |
| **Usability**       | Responsive and intuitive Streamlit layout.          |
| **Reliability**     | Retry failed Groq calls with exponential backoff.   |
| **Maintainability** | Modular structure following PEP 8.                  |
| **Security**        | API keys via environment variables only.            |
| **Logging**         | Centralized structured logging to file and console. |

---

## **6. Deliverables**

1. Complete Streamlit app source code.
2. Configuration file (`config.yaml`).
3. Prompt template (`prompt_template.txt`).
4. Logging and exception handling modules.
5. Unit tests using `pytest`.
6. Sample PowerPoint file (`sample_loan_forecast.pptx`).
7. `README.md` for setup and usage.
8. Optional: Dockerfile for deployment.

---

## **7. Acceptance Criteria**

| ID  | Criterion                                           | Status |
| --- | --------------------------------------------------- | ------ |
| AC1 | `.pptx` upload and parsing works reliably.          | ☐      |
| AC2 | Text and table content extracted per slide.         | ☐      |
| AC3 | AI summary focuses on negative and red/bold values. | ☐      |
| AC4 | All logs recorded with timestamps.                  | ☐      |
| AC5 | 90%+ unit test coverage achieved.                   | ☐      |
| AC6 | Configurations loaded dynamically.                  | ☐      |
| AC7 | API timeouts and retries handled gracefully.        | ☐      |

---

## **8. Future Enhancements**

* Parallel summarization for multiple slides using `asyncio.gather`.
* Option to export summarized results to PDF or Word.
* Visualization dashboards (charts of default rates).
* Integration with databases or vector stores for trend analysis.

---

### ✅ **End of Document**

---

Would you like me to generate a **Word (.docx) version** of this Markdown file (fully formatted with cover page, logo placeholder, and styled headings)? I can produce that instantly for download.



================
================

Code generation prompt:


Please generate complete code for this project requirements: ```🧩 Project Requirements — Streamlit-Based PowerPoint Content Summarization Application
1. Objective

Develop a highly responsive, visually rich, and modular Streamlit application in Python that enables users to upload PowerPoint presentations (.ppt or .pptx), automatically extract slide content, and generate AI-powered summaries of table data using the Groq LLM Python SDK (groq package).

The uploaded presentations represent quarterly loss forecasting or loan prediction reports for various banking segments (e.g., commercial banking).
Each report includes two key financial metrics:

Loan Default Rate (%)

Net Rate (%)

2. Functional Requirements
2.1 File Upload

Users should be able to upload .ppt or .pptx documents through a Streamlit interface.

The system must validate the file type before processing.

2.2 Content Extraction

The application should:

Parse the uploaded PowerPoint file.

Iterate through each slide.

Extract paragraph text and table content separately.

Each slide’s extracted content should be processed independently.

2.3 User Interface Layout

The Streamlit page should be split into two responsive panels:

Left Panel: Display paragraph (text) content.

Right Panel: Display table data extracted from the same slide.

The layout should adapt well to different screen sizes and maintain a clean, professional design.

2.4 Table Summary Generation

Include a “Generate Table Summary” button beneath each table view.

On clicking the button:

The application takes the table data shown on the right panel.

Sends it to the Groq LLM API (via the official groq Python SDK).

Uses a structured prompt (loaded from a separate prompt template file) to generate a summary of the table.

Displays the summary below the table in well-formatted bullet points.

The summary must specifically emphasize:

Negative values

Red or bold entries

Abnormal Loan Default Rate (%) and Net Rate (%) trends.

3. Technical Requirements
3.1 Architecture and Modularity

The codebase must follow a modular architecture, separating concerns across different modules such as:

File parsing and slide reading

Text and table extraction

LLM integration

UI rendering

Configuration and logging management

Each module should be independently testable.

3.2 Configuration Management

Use an external configuration file (config.yaml or JSON) to store:

LLM model configuration (model name, API key, etc.)

Application metadata (name, version)

Logging preferences

The application should dynamically read all configuration values at runtime.

3.3 Logging and Exception Handling

Implement centralized Python logging throughout the application:

Capture information, warning, and error logs.

Write logs to both the console and a log file (e.g., app.log).

Include robust exception handling:

Catch and handle invalid file formats, missing data, and API errors.

Display user-friendly messages in the Streamlit UI.

Log detailed stack traces for debugging.

3.4 Prompt Template and Prompt Engineering

Create a production-level prompt template file (prompt_template.txt) that follows prompting best practices, including:

Role-based prompting (system, user)

Few-shot prompting with example summaries

Clear and specific instructions to focus on negative or high-risk financial indicators

The application should read the prompt dynamically at runtime and pass it to the Groq LLM during summarization.

3.5 LLM Integration

Use the Groq Python SDK (groq package) for calling the model.

Implement:

Retry logic for rate-limit or transient API errors.

Timeout handling for slow responses.

Asynchronous support using AsyncGroq for non-blocking API calls.

3.6 Testing and Quality Assurance

Implement unit tests using pytest for all modules.

Test coverage should include:

File upload and validation logic

PowerPoint parsing and content extraction

LLM summarization (mocking Groq SDK calls)

Configuration loading

Error handling and logging

Tests should be reproducible and not depend on actual Groq API calls.

3.7 Sample Data

Include a sample .pptx file (sample_loan_forecast.pptx) for testing and demonstration.

The sample file should contain:

Text slides describing quarterly loan forecasts.

Tables containing “Loan Default Rate (%)” and “Net Rate (%)” data.

Some negative or highlighted values for summary testing.

4. Non-Functional Requirements
Category	Requirement
Performance	Process files up to 5 MB and generate summaries in under 10 seconds.
Scalability	Modular code allows adding support for more file types or LLM providers.
Usability	Intuitive, visually appealing, and mobile-friendly Streamlit UI.
Reliability	Gracefully handle failed uploads, timeouts, and API limits.
Security	Use environment variables for API keys; do not store secrets in code.
Maintainability	Code should follow PEP 8 and include docstrings for all public functions.```



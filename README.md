# Tourism Dashboard - Rio de Janeiro

This is an interactive tourism dashboard built with **Streamlit**. The application enables users to upload datasets, visualize data, perform basic analytics, and create various types of charts. The tool is designed to simplify data exploration and visualization for tourism data.

## Features

### File Upload and Data Loading
- Upload files in **CSV**, **XLS**, or **XLSX** format.
- Uses caching to optimize data loading performance.
- Displays an interactive table with selectable columns and rows.

### Customization
- Customizable background and font colors using a **Color Picker**.

### Data Visualization
- Create basic and advanced charts:
  - Bar, Line, and Pie Charts.
  - Histogram and Scatter Plots.
- Interactive selection of chart type and data.

### Data Filtering and Metrics
- Filter rows and columns based on user input.
- Display summary metrics like mean and sum for numeric columns.
- Option to filter data based on specific columns (e.g., year).

### Data Download
- Download filtered data as a **CSV** file.

### User-Friendly Design
- Dynamic progress bars and loading spinners.
- Handles data format errors gracefully with meaningful error messages.

## Technologies Used

- **Streamlit**: Interactive front-end for the dashboard.
- **Pandas**: Data manipulation and analysis.
- **Plotly Express**: Interactive and customizable data visualizations.

## Installation and Usage

1. Clone the Repository
- git clone https://github.com/your-username/tourism-dashboard.git
- cd tourism-dashboard
2. Set Up a Virtual Environment
Create and activate a virtual environment:
- python -m venv venv
- Windows: venv\Scripts\activate
- Mac/Linux: source venv/bin/activate
3. Install Dependencies
- pip install -r requirements.txt
4. Run the Application
- streamlit run app.py
*The application will be accessible at: http://localhost:8501

### Usage Instructions
Upload a CSV, XLS, or XLSX file using the file uploader.
Use the color picker to customize the dashboard appearance.
Select columns and rows to display in the interactive table.
Explore data using the provided charts and metrics.
Filter data based on specific criteria and download the filtered dataset.

Example Visualizations
Bar Chart
A basic bar chart showing the relationship between two selected columns.

Scatter Plot
An advanced scatter plot illustrating correlations between numeric columns.

Notes
Ensure that uploaded files are in the correct format.
For XLSX files, the openpyxl engine is required, while for XLS files, the xlrd engine is used.
Use the Download CSV button to export filtered data for further analysis.


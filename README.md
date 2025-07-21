# Product Description Generator

This project fetches product data from the DummyJSON API and uses Cohere's AI model to generate friendly, human-like product descriptions.

## Project Structure

```
product-description-generator/
├── ingest_products.py      # Fetches products from DummyJSON API
├── describer.py           # Generates descriptions using Cohere
├── pipeline.py            # Orchestrates the complete workflow
├── data/
│   ├── raw/              # Raw product data (JSON and TXT)
│   └── descriptions/     # Generated descriptions (JSON, TXT, HTML)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```
## Members of project 
 AJDIR Abdelali



## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Cohere API key:

```
COHERE_API_KEY=your_cohere_api_key_here
```

### 3. Create Required Directories

```bash
mkdir -p data/raw data/descriptions
```

## Usage Instructions

### Basic Usage

Run the complete pipeline with simulated responses:

```bash
python pipeline.py
```

### Using Real AI Model

To use the actual Cohere model (requires API key):

```bash
python pipeline.py --real-model
```

### Skip Data Ingestion

To reuse existing data and only regenerate descriptions:

```bash
python pipeline.py --skip-ingest --real-model
```

### Filter by Category

Generate descriptions only for specific product categories:

```bash
python pipeline.py --category laptops --real-model
```

### Different Modes

Customize the prompt mode:

```bash
python pipeline.py --mode summarize --real-model
python pipeline.py --mode "create marketing copy for" --real-model
```

## Individual Components

### Ingest Products

Fetch fresh product data:

```bash
python ingest_products.py
```

### Generate Descriptions

Process existing product data:

```bash
python describer.py --real-model
python describer.py --category smartphones --real-model
```

## Output Files

The pipeline generates three types of output files:

1. **JSON Format**: `pipeline_results_describe_YYYY-MM-DD_HH-MM.json`
2. **Text Format**: `pipeline_results_describe_YYYY-MM-DD_HH-MM.txt`
3. **HTML Format**: `pipeline_results_describe_YYYY-MM-DD_HH-MM.html` (styled webpage)

## Command Line Arguments

### pipeline.py

- `--skip-ingest`: Skip downloading new data, reuse existing files
- `--mode MODE`: Customize prompt mode (default: "describe")
- `--real-model`: Use actual Cohere model instead of simulation
- `--category CATEGORY`: Filter products by category

### describer.py

- `--real-model`: Use actual Cohere model instead of simulation
- `--category CATEGORY`: Filter products by category

## Team Member Contributions

- **Data Ingestion**: Fetches products from DummyJSON API with error handling
- **AI Integration**: Seamless Cohere API integration with fallback simulation
- **Pipeline Architecture**: Modular design with reusable components
- **Output Formatting**: Multiple output formats including styled HTML
- **CLI Interface**: Comprehensive command-line arguments for flexibility
- **Error Handling**: Robust error handling throughout the pipeline
- **Documentation**: Complete setup and usage instructions

## Example Output

### Sample Product Description

**Original**: "The iPhone 9 is a sleek and powerful smartphone from Apple..."

**AI-Generated**: "Experience premium mobile technology with the iPhone 9, Apple's sophisticated smartphone that combines sleek design with powerful performance. At $549, this highly-rated device (4.69★) delivers exceptional value for users seeking reliability and cutting-edge features in their daily mobile companion."

## Features

- ✅ Fetches real product data from DummyJSON API
- ✅ AI-powered description generation using Cohere
- ✅ Multiple output formats (JSON, TXT, HTML)
- ✅ Category filtering capability
- ✅ Simulation mode for testing without API costs
- ✅ Styled HTML output with product grouping
- ✅ Comprehensive error handling
- ✅ CLI argument support
- ✅ Modular, extensible architecture

## API Requirements

- **DummyJSON API**: Free, no authentication required
- **Cohere API**: Requires free account and API key from [cohere.ai](https://cohere.ai)

## Troubleshooting

1. **No COHERE_API_KEY found**: Ensure your `.env` file contains the API key
2. **No products found**: Run without `--skip-ingest` to fetch fresh data
3. **Category not found**: Check available categories in the raw data files
4. **API errors**: Check your internet connection and API key validity
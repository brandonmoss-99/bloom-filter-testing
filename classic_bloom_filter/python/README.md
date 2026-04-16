# Python classic bloom filter

A classic bloom filter implementation, using MurmurHash3 hash functions

`main_parallel.py` is used to 'benchmark' the BloomFilter class in `bloom_filter.py`, by running many rounds of creating a bloom filter, inserting a number of items, and then running searches for new not-inserted items, checking the number of false positives and timing data

It runs over as many CPU cores as are available for a faster execution

## Running
From inside this directory, with Python's virtual environment venv:

MacOS/Linux:
```bash
# Make the Python virtual environment
python -m venv ./venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Python code
python main_parallel.py

# Deactivate the virtual environment once done
deactivate
```

Windows:
```powershell
# Create the virtual environment with venv
python -m venv ./venv

# Activate the virtual environment
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run Python code
python main_parallel.py

# Deactivate the virtual environment once done
venv\Scripts\deactivate.bat
```

# Python Generators Project

This project demonstrates the use of Python generators for efficient data processing, streaming, and pagination. It contains several scripts that showcase different generator-based techniques for handling large datasets in a memory-efficient way.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [File Descriptions](#file-descriptions)
- [Setup & Requirements](#setup--requirements)


## Project Overview

Generators are a powerful feature in Python that allow you to iterate over data without loading everything into memory at once. This project provides practical examples of how to use generators for streaming users, batch processing, lazy pagination, and more.

## Features

- Stream data efficiently using generators
- Batch process large datasets
- Implement lazy pagination
- Example scripts for real-world scenarios

## Directory Structure

```
python-generators-0x00/
├── 0-stream_users.py
├── 1-batch_processing.py
├── 2-lazy_paginate.py
├── 4-stream_ages.py
├── seed.py
```

## File Descriptions

- **0-stream_users.py**: Streams user data using a generator.
- **1-batch_processing.py**: Processes data in batches using generators.
- **2-lazy_paginate.py**: Implements lazy pagination for large datasets.
- **4-stream_ages.py**: Streams user ages using a generator.
- **seed.py**: Seeds the dataset with sample data for testing.

## Setup & Requirements

1. **Python 3.6+** is required.
2. (Optional) Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install any required packages (if needed):
   ```powershell
   pip install -r requirements.txt
   ```
   _(Note: If there is no requirements.txt, the scripts may not require external packages.)_

## Usage

1. **Seed the data** (if applicable):
   ```powershell
   python python-generators-0x00/seed.py
   ```
2. **Run any of the example scripts:**
   ```powershell
   python python-generators-0x00/0-stream_users.py
   python python-generators-0x00/1-batch_processing.py
   python python-generators-0x00/2-lazy_paginate.py
   python python-generators-0x00/4-stream_ages.py
   ```
   Each script will demonstrate a different generator-based technique.



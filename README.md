# Python Generators Project

This project demonstrates the use of Python generators for efficient data processing, streaming, and pagination. It contains several scripts that showcase different generator-based techniques for handling large datasets in a memory-efficient way.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [File Descriptions](#file-descriptions)
- [Setup & Requirements](#setup--requirements)
- [Usage](#usage)

---

## Project Overview

Generators are a powerful feature in Python that allow you to iterate over data without loading everything into memory at once. This project provides practical examples of how to use generators for streaming users, batch processing, lazy pagination, and more.

---

## Features

- Stream data efficiently using generators
- Batch process large datasets

---

# Python Backend Utilities Project

This repository contains two main Python subprojects, each demonstrating advanced Python programming concepts:

- **python-generators-0x00**: Efficient data processing using Python generators.
- **python-decorators-0x01**: Practical use of Python decorators for database operations.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Subprojects](#subprojects)
- [Directory Structure](#directory-structure)
- [Setup & Requirements](#setup--requirements)
- [Usage](#usage)
- [License](#license)

---

## Project Overview

This project demonstrates efficient and Pythonic approaches to data processing and database management. It is split into two folders:

- **python-generators-0x00**: Shows how to use generators for streaming, batching, and paginating large datasets.
- **python-decorators-0x01**: Provides reusable decorators for logging, connection management, transactions, retries, and caching in database operations.

---

## Subprojects

### python-generators-0x00

Scripts for memory-efficient data handling:

- `0-stream_users.py`: Streams user data using a generator.
- `1-batch_processing.py`: Processes data in batches using generators.
- `2-lazy_paginate.py`: Implements lazy pagination for large datasets.
- `4-stream_ages.py`: Streams user ages using a generator.
- `seed.py`: Seeds the dataset with sample data for testing.

### python-decorators-0x01

Reusable decorators for database operations:

- `0-log_queries.py`: Logs SQL queries before execution.
- `1-with_db_connection.py`: Manages database connection context for functions.
- `2-transactional.py`: Ensures database operations are transactional.
- `3-retry_on_failure.py`: Retries failed database operations automatically.
- `4-cache_query.py`: Caches query results in memory for performance.

---

## Directory Structure

```
alx-backend-python/
├── python-generators-0x00/
│   ├── 0-stream_users.py
│   ├── 1-batch_processing.py
│   ├── 2-lazy_paginate.py
│   ├── 4-stream_ages.py
│   ├── seed.py
│   └── README.md
├── python-decorators-0x01/
│   ├── 0-log_queries.py
│   ├── 1-with_db_connection.py
│   ├── 2-transactional.py
│   ├── 3-retry_on_failure.py
│   ├── 4-cache_query.py
│   └── README.md (optional)
└── README.md
```

---

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

---

## Usage

### For Generators Project

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

### For Decorators Project

Run any of the scripts in `python-decorators-0x01/` to see the effect of the decorators. Each script is self-contained and demonstrates a specific decorator's use.

---



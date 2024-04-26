# Penpot SVG Interaction Extractor

## Overview
The "Penpot SVG Interaction Extractor" is a Python tool developed to parse SVG files exported from Penpot. It extracts on a per view basis forms (groups) their fields and resolves simple connections between boards. The output is JSON.

## Features
- Extract elements and their attributes from SVG files.
- Analyze the structure and styles of elements.
- Detect simple interaction patterns based on SVG structure.

## Installation
To set up the Penpot SVG Interaction Extractor, follow these steps:

### Usage

To use the extractor, run the extractor.py script with an SVG file as input:

```bash
python src/extractor.py --file path/to/your/file.svg
```

#### Example

An example SVG file is provided in the /examples directory. You can test the extractor with this file to see how it processes and outputs data.
Contributing

Contributions to improve the Penpot SVG Interaction Extractor are welcome. Please feel free to fork the repository, make changes, and submit a pull request.

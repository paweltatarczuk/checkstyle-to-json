# Checkstyle to JSON converter

Motivation: There is a number of tools for static-analysis of code supporting
xml format similar to checkstyle. I needed some simple CLI tool allowing to
convert Checkstyle XML to a JSON which includes context for every error.

## Note

This was only tested with PHPCS report in checkstyle format.

## Usage

To convert 'report.checkstyle.xml' file to JSON and store the result in 'report.json' file:

`python checkstyle-to-json.py <source> <dest>`

**Arguments:**

- source - Path to checkstyle XML file, this file will be converted
- dest   - Path to JSON file, this file will be created in JSON format

**Options:**

- `-B, --before BEFORE`  Amount of lines before used for file context fetch (default: 3)
- `-A, --after AFTER`    Amount of lines after used for file context fetch (default: 3)

## JSON format

```
{
    "path/to/file": [
        {
            "severity": "severity of error",
            "source": "rule which triggered the error",
            "line": "line in file",
            "column": "column in line",
            "message": "rule message",
            "context": ["array of of lines from file around the error..."],
        }
    ]
}
```

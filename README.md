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
- `-G, --gitlab`         Create a file suitable for the CI/CD-pipeline upload to gitlab.com

## JSON format

### Standard

```
{
    "path/to/file": [
        {
            "severity": "severity of error",
            "source": "rule which triggered the error",
            "line": "line in file",
            "column": "column in line",
            "message": "rule message",
            "context": {
                "line-no": "array of of lines from file around the error..."
            }
        }
    ]
}
```

### GitLab format

see https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html#implementing-a-custom-tool

[
  {
    "description": "a description",
    "fingerprint": "a checksum to (re-)identify issues",
    "severity": "severity: info, minor, major, critical, or blocker",
    "location": {
      "path": "file/with_issue.R",
      "lines": {
        "begin": 42
      }
    }
  }
]

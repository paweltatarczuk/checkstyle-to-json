# Grassy-CI Reporting

Motivation: There is a number of tools for static-analysis of code supporting
xml format. Each tool has its own unique XML format which differs slightly from
others. I needed some simple CLI tool allowing to convert XML report of popular
linters to an unified XML format.

## Note

This tool supports two types of linters:

- violation   Linters which report violations of some code standards
- duplicity   Linters which report duplicates

For these two types were introduced two separate formats.

## Supported linters

### Violation

- PHP Code Sniffer
- PHP Mess Detector

### Duplicity

- PHP Copy-Paste Detector

## Usage

There are two main scenarios of this tool:

### 1. Transform a report to the unified format

To transform a report in one format to the unified format you are going to
need some *XSLT processor*.

All `.xslt` files are placed in `resources` directories and you can use them
with a preferred tool for *XSLT* processing.

Example transforming `phpcs` report with `xsltproc`:

```
$ xsltproc -o path/to/new/report.xml resources/phpcs.xslt path/to/a/report.xml
```

### 2. Add source code context to a report (violations only)

`python contexter.py <report>`

**Arguments:**

- `report`   Path to a XML report

**Options:**

- `-B, --before BEFORE`  Amount of lines before used for file context fetch (default: 3)
- `-A, --after AFTER`    Amount of lines after used for file context fetch (default: 3)

## Formats

### Violation

```
<violation
  file="path/to/file/violating/a/rule"
  line="10"
  message="Message describing the violation"
  rule="Rule name which was violated"
  severity="warning">
  <context begin="7" end="13">
    ...
  </context>
</violation>
```

### Duplicity

```
<duplicate>
  <file path="path/to/file/having/duplicate">
    <context begin="10" end="30">
      ...
    </context>
  </file>
  <file path="path/to/another/file/having/duplicate">
    <context begin="20" end="40">
      ...
    </context>
  </file>
  <file ... />
  <context
</duplicate>
```

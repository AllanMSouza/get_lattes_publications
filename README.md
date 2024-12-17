# get_publication.py

This script processes XML files containing bibliographic production data and extracts information about conference and journal papers. It provides functions to parse the XML files, extract relevant data, and print the formatted output.

## Dependencies

- `bs4` (BeautifulSoup)
- `xml.etree.ElementTree`
- `sys`
- `os`
- `optparse`

## Functions

### `get_conference_papers(filename, until_year=2019)`

Extracts conference papers from the specified XML file.

- **Parameters:**
  - `filename` (str): The name of the XML file (without the `.xml` extension) located in the `data` directory.
  - `until_year` (int, optional): The cutoff year for including papers. Papers published before this year will be excluded. Default is 2019.

- **Returns:**
  - `papers` (list): A list of dictionaries, each containing information about a conference paper.

### `get_journal_papers(filename, until_year)`

Extracts journal papers from the specified XML file.

- **Parameters:**
  - `filename` (str): The name of the XML file (without the `.xml` extension) located in the `data` directory.
  - `until_year` (int): The cutoff year for including papers. Papers published before this year will be excluded.

- **Returns:**
  - `papers` (list): A list of dictionaries, each containing information about a journal paper.

### `print_papers(papers)`

Prints the formatted information of the given papers.

- **Parameters:**
  - `papers` (list): A list of dictionaries, each containing information about a paper.

### `main()`

Main function that parses command-line options, generates the XML file using an external command, and prints the extracted conference and journal papers.

- **Command-line Options:**
  - `--cpf` (str): The CPF (Cadastro de Pessoas Físicas) number used to generate the XML file.
  - `--from` (int): The cutoff year for including papers.

## Usage

To run the script, use the following command:

```sh
python get_publication.py --cpf <CPF_NUMBER> --from <YEAR>
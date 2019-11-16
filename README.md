# Accio-bib

Read a list of paper titles and save their DBLP bibtex entries in a file.

## Usage
```
pip install -r requirements.txt

python accio.py <input_file> <output_file>
```

## Example
Run
```
python accio.py test.txt test.bib
```
You should see the following in the standard output
```
Accio article "Dynamic Routing Between Capsules"
Success!
Accio article "Non-Autoregressive Neural Machine Translation"
Success!
Accio article "NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System"
Success!
*** Completed ***
3 Succeeded, 0 Failed
Bibtex saved to test.bib
```

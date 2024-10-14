# SAT Black Lists

Process black lists from the SAT from all the published CSV files.

## Run

Run 

```bash
python main.py
```

## Output

You'll get a CSV file with all the data appended in a single CSV file to find
taxpayers in the black lists.

## Instructions

1. Visit [SAT website](http://omawww.sat.gob.mx/cifras_sat/Paginas/datos/vinculo.html?page=ListCompleta69.html)
2. Create a new folder in `data/sat/black_lists/{update date in YYYYMMMDD format}`
3. Download each file into the folder above.
4. Create the `data/processed/` if it doesn't exist
5. Run script

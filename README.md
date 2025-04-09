# PastReader2025

⚠️**Update (07/04/2025)**: Test set release. You can download it [here](https://zenodo.org/records/15166903).

⚠️**Update (03/04/2025)**: The dataset has been moved to [Zenodo](https://zenodo.org/records/15084265).

---

Repository for the [PastReader](https://sites.google.com/view/pastreader2025) workshop at IberLEF 2025.

## Evaluation script usage

```bash
python evaluation_script.py [-h] --predictions_dir PREDICTIONS_DIR --references_dir REFERENCES_DIR [--output_file OUTPUT_FILE]
```

Argument description:

| Argument | Value | Description |
|----------|-------|-------------|
| -h, --help | None| Show help message and exit. |
| --predictions_dir | PREDICTIONS_DIR | Directory containing predictions. |
| --references_dir | REFERENCES_DIR | Directory containing references. |
| --output_file | OUTPUT_FILE | Output JSON file to save the evaluation results. If not provided, results will be printed to console. |

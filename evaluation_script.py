import os
import json
import argparse

from tqdm import tqdm
from evaluate import load

class PastReaderEval():
    def __init__(self):
        self.edit_distance = None

    def format_input(self, predictions_dir, references_dir):
        """Format the predictions and references files for evaluation."""
        predictions = []
        references = []

        # Check if directories exist
        if not os.path.exists(predictions_dir):
            raise FileNotFoundError(f"Predictions directory {predictions_dir} does not exist.")
        if not os.path.exists(references_dir):
            raise FileNotFoundError(f"References directory {references_dir} does not exist.")

        # Load reference and predictions
        for file in os.listdir(predictions_dir):
            with open(os.path.join(predictions_dir, file), "r", encoding="utf-8") as f:
                predictions.append(f.read())

        for file in os.listdir(references_dir):
            with open(os.path.join(references_dir, file), "r", encoding="utf-8") as f:
                references.append(f.read())

        # Check if predictions and references have the same length
        if len(predictions) != len(references):
            raise ValueError("Number of predictions and references do not match.")
        
        # Check if predictions and references are not empty
        if not predictions or not references:
            raise ValueError("Predictions and references are empty.")
        
        # Remove empty strings from references and the same row from predictions
        predictions = [pred for pred, ref in zip(predictions, references) if ref.strip()]
        references = [ref for ref in references if ref.strip()]

        # Check if predictions and references are not empty strings
        if any(not pred.strip() for pred in predictions):
            raise ValueError("Predictions contain empty strings.")
        if any(not ref.strip() for ref in references):
            raise ValueError("References contain empty strings.")
        
        return predictions, references

    def generate_output(self, results, output_file):
        """Generate the output results."""
        if output_file:
            output_dir = os.path.dirname(output_file)

            if not output_dir:
                output_dir = os.getcwd()
            
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            if output_file.endswith(".json"):
                filename = os.path.basename(output_file)
            else:
                filename = os.path.basename(output_file) + ".json"

            with open(os.path.join(output_dir, filename), "w") as f:
                # Save results to a JSON file
                json.dump(results, f, indent=4)
            print(f"Evaluation results saved to {filename}")

        # Print results to console
        print(json.dumps(results, indent=4))

    def levenshtein_distance(self, predictions, references):
        """Compute the Levenshtein distance between predictions and references."""

        from Levenshtein import distance as levenshtein
        scores = [
            levenshtein(pred, ref) for pred, ref in tqdm(zip(predictions, references), total=len(references))
        ]
        self.edit_distance = sum(scores) / len(scores)
        return self.edit_distance

    def sentence_error_rate(self, predictions, references):
        """Compute the sentence error rate (SER) between predictions and references."""

        return None

    def normalized_edit_distance(self, predictions, references):
        """Compute the normalized edit distance between predictions and references."""

        if not self.edit_distance:
            self.levenshtein_distance(predictions, references)

        return self.edit_distance / len(references)

    def compute_metrics(self, predictions, references):
        """Compute various metrics for the predictions and references."""

        wer = load("wer")
        rouge = load("rouge")
        bleu = load("bleu")

        results = {
            "Word Error Rate": wer.compute(predictions=predictions, references=references),
            "Sentence Error Rate": self.sentence_error_rate(predictions, references),
            "Levenshtein Distance": self.levenshtein_distance(predictions, references),
            "Normalized Edit Distance": self.normalized_edit_distance(predictions, references),
            "BLEU Score": bleu.compute(predictions=predictions, references=references)["bleu"],
            "ROUGE Score": rouge.compute(predictions=predictions, references=references)
        }
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PastReader Evaluation Script")
    parser.add_argument(
        "--predictions_dir", 
        type=str, 
        help="Directory containing predictions.",
        required=True
    )

    parser.add_argument(
        "--references_dir", 
        type=str, 
        help="Directory containing references.",
        required=True
    )

    parser.add_argument(
        "--output_file", 
        type=str, 
        help="Output file to save the evaluation results. If not provided, results will be printed to console.",
        required=False
    )

    args = parser.parse_args()

    # Initialize evaluation class
    eval = PastReaderEval()

    # Format files
    predictions, references = eval.format_input(args.predictions_dir, args.references_dir)

    # Compute metrics
    results = eval.compute_metrics(predictions, references)

    # Generate output
    eval.generate_output(results, args.output_file)
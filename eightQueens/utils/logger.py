import pandas as pd
import os

class Logger:
    """
    Handles logging of GA progress to a list and saving to a CSV file.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.log_data = []
        self._prepare_directory()

    def _prepare_directory(self):
        """Ensures the directory for the log file exists."""
        dir_name = os.path.dirname(self.filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

    def log_generation(self, generation: int, best_fitness: float, avg_fitness: float, worst_fitness: float):
        """Logs the metrics for a single generation."""
        self.log_data.append({
            'generation': generation,
            'best_fitness': best_fitness,
            'avg_fitness': avg_fitness,
            'worst_fitness': worst_fitness
        })

    def save(self):
        """Saves the logged data to a CSV file."""
        if not self.log_data:
            return # Nothing to save
        df = pd.DataFrame(self.log_data)
        df.to_csv(self.filepath, index=False)
        # print(f"Log saved to {self.filepath}")

    def clear(self):
        """Clears the internal log data."""
        self.log_data = []
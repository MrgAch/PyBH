# PyBH

**PyBH** is a Python package designed for petroleum geology, it provides functionality for 1D basin modeling.

## Features

- **Preliminary version:**  
  - Plotting burial history curves from well data.  

- **Planned features in future versions:**  
  - Thermal history modeling.  
  - Source rock maturation modeling.  

## Requirements

To use **PyBH**, you need **Python 3.10 or higher**.  

The package relies on the following libraries:  
- [Matplotlib](https://matplotlib.org/)  
- [Pandas](https://pandas.pydata.org/)  
- [NumPy](https://numpy.org/)  

These dependencies will be installed automatically when you install **PyBH**.

## Installation

To install **PyBH**, simply run the following command in your terminal:
```sh
pip install PyBH
```

# PyBH Package Usage Guide

## 1. Preparing the CSV File

Create a CSV file containing the **1D well model** (real or virtual) with the following columns:

- **Name**: Event name
- **Type**: Event type (N = Normal Layer, H = Hiatus, E = Erosion, D = Deposition, B = Base)
- **Top**: Depth at the top of the layer
- **Thickness**: Layer thickness
- **Deposed**: Deposited thickness
- **Eroded**: Eroded thickness
- **Age at top**: Age at the top of the layer

### Example of `model1.csv`
```csv
| Name | Type | Top | Thickness | Deposed | Eroded | Age at top |
|------|------|-----|-----------|---------|--------|------------|
| L1   | N    | 0   | 15        | 15      | 0      | 0          |
| L2   | H    | 15  | 0         | 0       | 0      | 8          |
| L3   | N    | 15  | 76        | 76      | 0      | 20         |
| L4   | N    | 91  | 15        | 15      | 0      | 40         |
| L5   | N    | 106 | 31        | 31      | 0      | 60         |
| L6   | H    | 137 | 0         | 0       | 0      | 75         |
| L7   | E    | 137 | 0         | 0       | 30     | 76         |
| L8   | D    | 137 | 0         | 30      | 0      | 80         |
| L9   | N    | 137 | 61        | 61      | 0      | 83         |
| L10  | N    | 198 | 30        | 30      | 0      | 90         |
| L11  | N    | 228 | 61        | 61      | 0      | 100        |
| L12  | N    | 289 | 31        | 31      | 0      | 110        |
| Bas  | B    | 320 | 0         | 0       | 0      | 125        |
```

**➡ Save this file as `model1.csv` in the same directory as your script.**

---

## 2. Using the PyBH Package

Create a **Python file** (`script.py`) or a **Jupyter notebook** (`notebook.ipynb`) in the same directory as `model1.csv`, then add the following code:

```python
# Import the package
import PyBH as bh  

# Load the model data
data = bh.import_data('model1.csv')

# Plot the model
bh.plot(data)
```

---

## 3. Code Explanation
✅ **Import the `PyBH` package**  
✅ **Load data from `model1.csv`** using `bh.import_data()`  
✅ **Visualize the model as a plot** using `bh.plot(data)`  
```

---

## 4. Support and Contact
If you encounter any issues, open an **issue** on the GitHub repository or contact me.

---

🚀 **Enjoy working with PyBH!**
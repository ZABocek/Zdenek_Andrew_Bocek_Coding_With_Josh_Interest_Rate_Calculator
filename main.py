import os
import csv
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QTreeView, QLineEdit, 
    QMessageBox, QMainWindow, QFileDialog)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FinanceApp(QMainWindow):
    def __init__(self):
        super(FinanceApp, self).__init__()
        self.setWindowTitle("InterestMe 2.0")
        self.resize(800, 600)
        
        main_window = QWidget()
        
        self.rate_text = QLabel("Interest Rate (%):")
        self.rate_input = QLineEdit()
        
        self.initial_text = QLabel("Initial Investment:")
        self.initial_input = QLineEdit()
        
        self.years_text = QLabel("Years to Invest:")
        self.years_input = QLineEdit()
        
        # Creation of Treeview
        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        
        self.calc_button = QPushButton("Calculate")
        self.clear_button = QPushButton("Clear")
        self.save_button = QPushButton("Save")  # New save button
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()
        
        self.row1.addWidget(self.rate_text)
        self.row1.addWidget(self.rate_input)
        self.row1.addWidget(self.initial_text)
        self.row1.addWidget(self.initial_input)
        self.row1.addWidget(self.years_text)
        self.row1.addWidget(self.years_input)    
        
        self.col1.addWidget(self.tree_view)
        self.col1.addWidget(self.calc_button)
        self.col1.addWidget(self.clear_button)
        self.col1.addWidget(self.save_button)  # Add the save button to the layout
        
        self.col2.addWidget(self.canvas)
        
        self.row2.addLayout(self.col1, 30)
        self.row2.addLayout(self.col2, 70)
        
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        
        main_window.setLayout(self.master_layout)
        self.setCentralWidget(main_window)
        
        self.calc_button.clicked.connect(self.calc_interest)
        self.clear_button.clicked.connect(self.reset)
        self.save_button.clicked.connect(self.save_results)  # Connect the save button
        
    def calc_interest(self):
        initial_investment = None
        try:
            interest_rate = float(self.rate_input.text())
            initial_investment = float(self.initial_input.text())
            num_years = int(self.years_input.text())
        
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input, enter a number!")
            return
        
        total = initial_investment
        self.model.clear()  # Clear the tree view before calculation
        for year in range(1, num_years + 1):
            total += total * (interest_rate / 100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([item_year, item_total])
            
        # Update my chart with the data
        self.figure.clear()
        ax = self.figure.subplots()
        years = list(range(1, num_years + 1))
        totals = [initial_investment * (1 + interest_rate / 100) ** year for year in years]
        
        ax.plot(years, totals)
        ax.set_title("Interest Chart")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total")
        self.canvas.draw()
        
        # Store values for saving
        self.years = years
        self.totals = totals
            
    def reset(self):
        # Clear all input fields and the QTreeView model
        self.rate_input.clear()
        self.initial_input.clear()
        self.years_input.clear()
        self.model.clear()

        # Clear the figure and refresh the canvas
        self.figure.clear()
        self.canvas.draw()
    
    def save_results(self):
        # Open a directory selection dialog
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        
        if dir_path:
            num = 0
            # Create the "Saved" folder inside the selected directory
            folder_path = os.path.join(dir_path, "Saved{num}")
            num += 1
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                
            # Save the CSV file
            csv_file_path = os.path.join(folder_path, "interest_results.csv")
            with open(csv_file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Year", "Total"])  # Header row
                
                for year, total in zip(self.years, self.totals):
                    writer.writerow([year, "{:.2f}".format(total)])
                    
            # Save the graph as a PNG image
            image_file_path = os.path.join(folder_path, "interest_chart.png")
            self.figure.savefig(image_file_path)
            
            QMessageBox.information(self, "Save", f"Results saved to {folder_path}")
            
if __name__ == "__main__":
    app = QApplication([])
    my_app = FinanceApp()
    my_app.show()
    app.exec_()

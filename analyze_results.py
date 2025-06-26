import pandas as pd
from tkinter import filedialog
def main():
    try:
        csv_path = filedialog.askopenfilename(title="select a csv file", filetypes=(("csv files", "*.csv"), ("All files", "*.*")))
        # df = pd.read_csv("result.csv")
        df = pd.read_csv(csv_path)

        print("Total records:", len(df))
        print("Path:",csv_path)
        print("Performance Statistics (in milliseconds/compare):\n")
        for col in df.columns:
            print(f"{col}:")
            print(f"  Min:  {df[col].min():.6f} ms")
            print(f"  Max:  {df[col].max():.6f} ms")
            print(f"  Avg:  {df[col].mean():.6f} ms")
            print()
    except:
        option = input("are you still there?[y/n]").upper()
        if option == "Y":
            main()
        else:
            print("see yaa!")

main()
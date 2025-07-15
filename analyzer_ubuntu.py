import pandas as pd
import os
import sys
import glob

def select_csv_file():
    """ให้ผู้ใช้เลือกไฟล์ CSV โดยไม่ใช้ tkinter"""
    
    # วิธีที่ 1: ใช้ command line argument
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
        if os.path.exists(csv_path) and csv_path.endswith('.csv'):
            return csv_path
        else:
            print(f"Error: File '{csv_path}' not found or not a CSV file")
    
    # วิธีที่ 2: ค้นหาไฟล์ CSV ใน directory ปัจจุบัน
    csv_files = glob.glob("*.csv")
    
    if csv_files:
        print("Found CSV files in current directory:")
        for i, file in enumerate(csv_files, 1):
            print(f"{i}. {file}")
        
        while True:
            try:
                choice = input(f"\nSelect file (1-{len(csv_files)}) or enter full path: ").strip()
                
                # ถ้าผู้ใช้ใส่ตัวเลข
                if choice.isdigit():
                    choice = int(choice)
                    if 1 <= choice <= len(csv_files):
                        return csv_files[choice - 1]
                    else:
                        print(f"Please enter a number between 1 and {len(csv_files)}")
                        continue
                
                # ถ้าผู้ใช้ใส่ path
                elif os.path.exists(choice) and choice.endswith('.csv'):
                    return choice
                
                else:
                    print("Invalid choice or file not found. Please try again.")
                    
            except (ValueError, KeyboardInterrupt):
                print("\nOperation cancelled.")
                return None
    
    # วิธีที่ 3: ให้ผู้ใช้ใส่ path เอง
    while True:
        try:
            csv_path = input("Enter CSV file path (or 'q' to quit): ").strip()
            
            if csv_path.lower() == 'q':
                return None
                
            if os.path.exists(csv_path) and csv_path.endswith('.csv'):
                return csv_path
            else:
                print("File not found or not a CSV file. Please try again.")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None

def analyze_csv(csv_path):
    """วิเคราะห์ข้อมูล CSV"""
    try:
        print(f"Loading: {csv_path}")
        df = pd.read_csv(csv_path)
        
        print("=" * 60)
        print(f"CSV Analysis Results")
        print("=" * 60)
        print(f"File: {os.path.basename(csv_path)}")
        print(f"Full Path: {os.path.abspath(csv_path)}")
        print(f"Total records: {len(df)}")
        print(f"Total columns: {len(df.columns)}")
        print("=" * 60)
        
        # แสดงข้อมูลทั่วไป
        print("\nColumn Information:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col} (dtype: {df[col].dtype})")
        
        print("\n" + "=" * 60)
        print("Performance Statistics (in milliseconds/compare):")
        print("=" * 60)
        
        # วิเคราะห์เฉพาะคอลัมน์ที่เป็นตัวเลข
        numeric_columns = df.select_dtypes(include=['number']).columns
        
        if len(numeric_columns) == 0:
            print("No numeric columns found for analysis.")
            return
        
        for col in numeric_columns:
            print(f"\n{col}:")
            print(f"  Count: {df[col].count()}")
            print(f"  Min:   {df[col].min():.6f} ms")
            print(f"  Max:   {df[col].max():.6f} ms")
            print(f"  Mean:  {df[col].mean():.6f} ms")
            print(f"  Median:{df[col].median():.6f} ms")
            print(f"  Std:   {df[col].std():.6f} ms")
        
        # แสดงตัวอย่างข้อมูล
        print("\n" + "=" * 60)
        print("Sample Data (first 5 rows):")
        print("=" * 60)
        print(df.head())
        
        # สถิติเพิ่มเติม
        if len(numeric_columns) > 0:
            print("\n" + "=" * 60)
            print("Summary Statistics:")
            print("=" * 60)
            print(df[numeric_columns].describe())
            
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")

def main():
    print("CSV Performance Analyzer - Ubuntu Version")
    print("=" * 50)
    
    try:
        csv_path = select_csv_file()
        
        if csv_path:
            analyze_csv(csv_path)
        else:
            print("No file selected. Exiting.")
            return
            
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # ถาม user ว่าต้องการทำต่อหรือไม่
    try:
        option = input("\nDo you want to analyze another file? [y/n]: ").strip().upper()
        if option == "Y":
            main()
        else:
            print("Thanks for using CSV Analyzer!")
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
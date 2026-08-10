import pandas as pd
import mysql.connector

# STEP 1: Load Excel File
file_path = r"E:/Aftership Project/Phase 4/USA_Logistics_ERP_3500_Records-3.xlsx"
df = pd.read_excel(file_path)

# STEP 2: Clean Column Names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[()/\-]", "_", regex=True)
)

# 🔥 FIX COLUMN NAME MISMATCH (VERY IMPORTANT)
df = df.rename(columns={
    'tax_id__ein_': 'tax_id',
    'dangerous_goods__y_n_': 'dangerous_goods'
})

print("Columns:", df.columns)
print("Total Columns:", len(df.columns))

# STEP 3: Handle NULL values
df = df.where(pd.notnull(df), None)

# 🔥 STEP 4: FIX STRING COLUMNS
string_cols = [
    'postal_code', 'tax_id', 'hs_code',
    'barcode', 'tracking_number'
]

for col in string_cols:
    if col in df.columns:
        df[col] = df[col].astype(str)

# 🔥 STEP 5: FIX NUMERIC COLUMNS
numeric_cols = [
    'opening_qty','received_qty','order_qty','picked_qty','packed_qty',
    'issued_qty','adjustment_qty','closing_qty'
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# 🔥 STEP 6: FIX DECIMAL COLUMNS
decimal_cols = [
    'credit_limit','unit_price','unit_cost','order_value','opening_value',
    'length','width','height','weight','cbm'
]

for col in decimal_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# 🔥 STEP 7: FIX DATE COLUMNS
date_cols = [
    'opening_date','expiry_date','order_date','packed_date',
    'dispatch_date','expected_delivery','delivered_date'
]

for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
        df[col] = df[col].dt.strftime('%Y-%m-%d')

# 🔥 STEP 8: Replace NaT with None
df = df.replace({pd.NaT: None})

# STEP 9: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vi@5930singh",
    database="logistics_db"
)

cursor = conn.cursor()

# STEP 10: AUTO QUERY
columns = ", ".join(df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))

insert_query = f"""
INSERT INTO logistics_erp ({columns})
VALUES ({placeholders})
"""

print("Placeholders Count:", insert_query.count("%s"))

# STEP 11: Convert DataFrame to List
data = df.values.tolist()

print("Sample Row:", data[0])
print("Row Length:", len(data[0]))

# STEP 12: Insert Data
try:
    cursor.executemany(insert_query, data)
    conn.commit()
    print("✅ Data inserted successfully!")

except Exception as e:
    print("❌ Error:", e)
    conn.rollback()

# STEP 13: Close
cursor.close()
conn.close()
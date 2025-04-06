import pandas as pd
import os
from datetime import datetime

# Define the table structure and mapping
table_name = "product_price_tracking"
columns_mapping = {
    "月份": "month",
    "日期": "date",
    "Buybox价格($)": "buybox_price",
    "价格($)": "price",
    "Prime价格($)": "prime_price",
    "Coupon价格($)": "coupon_price",
    "Coupon折扣": "coupon_discount",
    "Deal价格($)": "deal_price",
    "Deal价格信息": "deal_price_info",
    "FBA价格($)": "fba_price",
    "FBM价格($)": "fbm_price",
    "划线价格($)": "strikethrough_price",
    "子体销量($)": "subitem_sales",
    "BSR排名": "bsr_rank",
    "BSR[Area Rugs]": "bsr_area_rugs",
    "BSR[Area Rug Sets]": "bsr_area_rug_sets",
    "评分": "rating",
    "评分数": "review_count",
    "卖家数": "seller_count"
}

# Required fields that need to be added
required_fields = {
    "parent_asin": None,
    "asin": None,
    "create_time": "CURRENT_TIMESTAMP",
    "update_time": "CURRENT_TIMESTAMP",
    "batch": None
}

def clean_value(value):
    """Clean and format values for SQL insertion"""
    if pd.isna(value) or value in [' ', '']:
        return 'NULL'
    elif isinstance(value, str):
        return value
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        return f"'{str(value)}'"

def generate_insert_statements(df, excel_filename):
    """Generate INSERT statements from DataFrame"""
    insert_statements = []
    batch_id = datetime.now().strftime("%Y%m%d%H%M%S")  # Generate batch ID
    
    for _, row in df.iterrows():
        columns = []
        values = []
        
        # Add required fields
        required_fields['batch'] = batch_id
        for field, default_value in required_fields.items():
            columns.append(field)
            values.append(default_value if default_value else 'NULL')
        
        # Map and add data columns
        for excel_col, db_col in columns_mapping.items():
            if excel_col in df.columns:
                columns.append(db_col)
                value = row[excel_col]
                values.append(clean_value(value))
        
        # Build the INSERT statement
        columns_str = ", ".join(columns)
        values_str = ", ".join(values)
        insert_stmt = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
        insert_statements.append(insert_stmt)
    
    return insert_statements

def process_excel_files(excel_dir):
    """Process all Excel files in the directory"""
    for excel_file in os.listdir(excel_dir):
        if excel_file.endswith(('.xlsx', '.xls')):
            file_path = os.path.join(excel_dir, excel_file)
            print(f"Processing file: {file_path}")
            
            try:
                df = pd.read_excel(file_path)
                insert_statements = generate_insert_statements(df, excel_file)
                
                # Save to SQL file
                sql_filename = f"{os.path.splitext(excel_file)[0]}.sql"
                with open(sql_filename, 'w', encoding='utf-8') as sql_file:
                    sql_file.write("\n".join(insert_statements))
                
                print(f"Generated SQL file: {sql_filename} with {len(insert_statements)} INSERT statements")
                
            except Exception as e:
                print(f"Error processing {excel_file}: {str(e)}")

if __name__ == "__main__":
    excel_file_path = "D:\\rpa_tools\\mysql_connect\\2月模型取数\\Keepa\\"
    process_excel_files(excel_file_path)
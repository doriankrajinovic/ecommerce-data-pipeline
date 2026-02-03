"""
Parquet exporter - sprema generirane podatke u Parguet format. 
"""

from pathlib import Path 
import pandas as pd 

from models import Customer, Order, OrderItem, Product 



def customers_to_dataframe(customers):
    """Pretvara listu Customer objekata u DataFrame"""

    data_list = []

    for customer in customers:
        customer_dict = customer.model_dump() 
        data_list.append(customer_dict)

    df = pd.DataFrame(data_list)
    return df 

def products_to_dataframe(products):
    """Pretvara listu Product objekata u DataFrame."""

    data_list = []

    for product in products: 
        product_dict = product.model_dump()
        data_list.append(product_dict)

    df = pd.DataFrame(data_list)

    # Enum -> string 
    for i in range(len(df)): 
        category_value = df.loc[i, 'category']
        if hasattr(category_value, 'value'): 
            df.loc[i, 'category'] = category_value.value
    
    return df 


def orders_to_dataframe(orders):
    """Pretvara listu Order objekata u DataFrame."""
    data_list = []
    
    for order in orders:
        order_dict = order.model_dump()
        data_list.append(order_dict)
    
    df = pd.DataFrame(data_list)
    
    # Enum -> string
    for i in range(len(df)):
        status_value = df.loc[i, 'status']
        if hasattr(status_value, 'value'):
            df.loc[i, 'status'] = status_value.value
    
    return df


def order_items_to_dataframe(order_items):
    """Pretvara listu OrderItem objekata u DataFrame."""
    data_list = []
    
    for item in order_items:
        item_dict = item.model_dump()
        data_list.append(item_dict)
    
    df = pd.DataFrame(data_list)
    return df


def export_to_parquet(data, output_dir="data/raw"): 
    """Sprema DataFrame u Parquet datoteku. """
    output_path = Path(output_dir) 
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files = {}

    print("Saving customers...")
    customers_df = customers_to_dataframe(data["customers"])
    customers_file = output_path / "customers.parquet"
    customers_df.to_parquet(customers_file, index=False)
    saved_files["customers"] = str(customers_file)
    print(f"  Saved {len(customers_df)} rows")
    
    # Products
    print("Saving products...")
    products_df = products_to_dataframe(data["products"])
    products_file = output_path / "products.parquet"
    products_df.to_parquet(products_file, index=False)
    saved_files["products"] = str(products_file)
    print(f"  Saved {len(products_df)} rows")
    
    # Orders
    print("Saving orders...")
    orders_df = orders_to_dataframe(data["orders"])
    orders_file = output_path / "orders.parquet"
    orders_df.to_parquet(orders_file, index=False)
    saved_files["orders"] = str(orders_file)
    print(f"  Saved {len(orders_df)} rows")
    
    # Order Items
    print("Saving order_items...")
    order_items_df = order_items_to_dataframe(data["order_items"])
    order_items_file = output_path / "order_items.parquet"
    order_items_df.to_parquet(order_items_file, index=False)
    saved_files["order_items"] = str(order_items_file)
    print(f"  Saved {len(order_items_df)} rows")
    
    return saved_files


if __name__ == "__main__":
    from generator import generate_all_data
    
    print("=== Generating data ===")
    data = generate_all_data(num_customers=100, num_products=50, num_orders=200)
    
    print("\n=== Exporting to Parquet ===")
    saved_files = export_to_parquet(data)
    
    print("\n=== Done! ===")
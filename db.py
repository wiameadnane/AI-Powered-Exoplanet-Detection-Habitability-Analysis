import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseManager:
    def __init__(self, table_name: str = 'tess_dataset'):
        self.table_name = table_name
        
        # Try to get DATABASE_URL first (for cloud databases like Neon)
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Use DATABASE_URL if available (Neon, Heroku, etc.)
            self.connection_string = database_url
            self.use_url = True
        else:
            # Fall back to individual parameters
            self.connection_params = {
                'host': os.getenv('DB_HOST'),
                'port': os.getenv('DB_PORT'),
                'database': os.getenv('DB_NAME'),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD')
            }
            self.use_url = False

    def get_connection(self):
        """Create and return a database connection"""
        if self.use_url:
            return psycopg2.connect(self.connection_string)
        else:
            return psycopg2.connect(**self.connection_params)

    def add_csv_to_database(self, csv_path: str) -> dict:
        """
        Add CSV data as new entries into the database

        Args:
            csv_path: Path to the CSV file

        Returns:
            dict: Status information about the operation
        """
        try:
            df = pd.read_csv(csv_path)
            conn = self.get_connection()
            cur = conn.cursor()

            # Create table if it doesn't exist
            type_mapping = {'int64': 'INTEGER', 'float64': 'REAL', 'object': 'TEXT', 'bool': 'BOOLEAN'}
            columns = [f"{col} {type_mapping.get(str(dtype), 'TEXT')}" for col, dtype in df.dtypes.items()]
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({', '.join(columns)})")

            # Insert data
            cols = df.columns.tolist()
            insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(self.table_name),
                sql.SQL(', ').join(map(sql.Identifier, cols)),
                sql.SQL(', '.join(['%s'] * len(cols)))
            )

            for _, row in df.iterrows():
                cur.execute(insert_query, tuple(row))

            conn.commit()
            return {'success': True, 'rows_inserted': len(df)}

        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()

    def export_to_csv(self, output_path: str) -> dict:
        """
        Export entire database table to CSV for model retraining

        Args:
            output_path: Path where CSV file will be saved

        Returns:
            dict: Status information about the operation
        """
        try:
            conn = self.get_connection()
            df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", conn)
            df.to_csv(output_path, index=False)

            return {'success': True, 'rows_exported': len(df), 'output_path': output_path}

        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            if 'conn' in locals():
                conn.close()


    def get_row_count(self) -> dict:
        """
        Get the total number of rows in the database table
        
        Returns:
            dict: Count information
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            count = cur.fetchone()[0]
            return {'success': True, 'count': count}
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()


# Example usage
if __name__ == "__main__":
    db = DatabaseManager(table_name='tess_dataset')

    # Add CSV to database
    result = db.add_csv_to_database('cleaned_data.csv')
    print(result)

    # Export database to CSV for retraining
    result = db.export_to_csv('whole_dataset.csv')
    print(result)

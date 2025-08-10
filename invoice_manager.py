import sqlite3
import json
from datetime import datetime
from typing import List, Dict
import os

class InvoiceManager:
    def __init__(self, db_name: str = "invoices.db"):
        """Initialize the SQLite database for invoice management."""
        self.db_name = db_name
        self._init_database()

    def _init_database(self):
        """Create the invoices and invoice_customers tables if they don't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_number INTEGER PRIMARY KEY,
                    creation_date TEXT NOT NULL,
                    company_name TEXT,
                    total_amount REAL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS invoice_customers (
                    invoice_number INTEGER,
                    customer_name TEXT,
                    customer_address TEXT,
                    customer_email TEXT,
                    items TEXT,  -- JSON serialized list of items
                    FOREIGN KEY (invoice_number) REFERENCES invoices (invoice_number)
                )
            """)
            conn.commit()

    def store_invoice(self, invoice_number: int, invoice_date: str, company: Dict, customers: List[Dict]):
        """Store an invoice and its customers with their items in the database."""
        total_amount = sum(sum(item["quantity"] * item["unit_price"] for item in customer["items"]) for customer in customers)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Store invoice
            cursor.execute("""
                INSERT INTO invoices (invoice_number, creation_date, company_name, total_amount)
                VALUES (?, ?, ?, ?)
            """, (invoice_number, invoice_date, company["name"], total_amount))
            # Store customers and their items
            for customer in customers:
                items_json = json.dumps(customer["items"])
                cursor.execute("""
                    INSERT INTO invoice_customers (invoice_number, customer_name, customer_address, customer_email, items)
                    VALUES (?, ?, ?, ?, ?)
                """, (invoice_number, customer["name"], customer["address"], customer["email"], items_json))
            conn.commit()

    def retrieve_invoice(self, invoice_number: int) -> Dict:
        """Retrieve an invoice and its customers with their items by number."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Retrieve invoice
            cursor.execute("""
                SELECT invoice_number, creation_date, company_name, total_amount
                FROM invoices WHERE invoice_number = ?
            """, (invoice_number,))
            invoice_result = cursor.fetchone()
            if not invoice_result:
                return {}
            # Retrieve customers and their items
            cursor.execute("""
                SELECT customer_name, customer_address, customer_email, items
                FROM invoice_customers WHERE invoice_number = ?
            """, (invoice_number,))
            customers = [
                {
                    "name": row[0],
                    "address": row[1],
                    "email": row[2],
                    "items": json.loads(row[3]) if row[3] else []
                } for row in cursor.fetchall()
            ]
            return {
                "invoice_number": invoice_result[0],
                "creation_date": invoice_result[1],
                "company_name": invoice_result[2],
                "total_amount": invoice_result[3],
                "customers": customers
            }

    def retrieve_all_invoices(self) -> List[Dict]:
        """Retrieve all invoices with their customers and items."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Retrieve all invoices
            cursor.execute("""
                SELECT invoice_number, creation_date, company_name, total_amount
                FROM invoices
            """)
            invoices = cursor.fetchall()
            result = []
            for invoice in invoices:
                invoice_number = invoice[0]
                # Retrieve customers and their items for this invoice
                cursor.execute("""
                    SELECT customer_name, customer_address, customer_email, items
                    FROM invoice_customers WHERE invoice_number = ?
                """, (invoice_number,))
                customers = [
                    {
                        "name": row[0],
                        "address": row[1],
                        "email": row[2],
                        "items": json.loads(row[3]) if row[3] else []
                    } for row in cursor.fetchall()
                ]
                result.append({
                    "invoice_number": invoice[0],
                    "creation_date": invoice[1],
                    "company_name": invoice[2],
                    "total_amount": invoice[3],
                    "customers": customers
                })
            return result

    def categorize_invoices_by_date(self, period: str = "month") -> Dict:
        """Categorize invoices by year, month, or day."""
        invoices = self.retrieve_all_invoices()
        categorized = {}
        for invoice in invoices:
            date = datetime.strptime(invoice["creation_date"], "%Y-%m-%d")
            if period == "year":
                key = str(date.year)
            elif period == "month":
                key = f"{date.year}-{date.month:02d}"
            else:  # day
                key = invoice["creation_date"]
            if key not in categorized:
                categorized[key] = []
            categorized[key].append(invoice)
        return categorized

    def delete_invoice(self, invoice_number: int) -> bool:
        """Delete an invoice and its associated customers by number."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Delete customers
            cursor.execute("DELETE FROM invoice_customers WHERE invoice_number = ?", (invoice_number,))
            # Delete invoice
            cursor.execute("DELETE FROM invoices WHERE invoice_number = ?", (invoice_number,))
            conn.commit()
            return cursor.rowcount > 0
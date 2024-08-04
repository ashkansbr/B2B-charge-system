Django Project

This project is a B2B software system designed to manage and sell credit for vendors.
The system allows vendors to request an increase in their credit, and an API will be used to manage the credit allocation for vendors based on their phone numbers.
The system ensures that the credit allocation is precise and aligns with the accounting system.

Features

Vendor Credit Management: Vendors can request an increase in their credit.
Credit Allocation: The API allocates a specific amount of credit to a vendor based on their phone number.
Real-Time Updates: Ensures that the vendor's credit is updated in real-time and prevents negative credit balance.
Accounting Integration: Ensures that the credit system aligns with the accounting system and accurately records transactions.
Concurrency Handling: Handles potential race conditions and double spending issues.
Logging: Creates appropriate logs for credit sales and updates.
Testing: Includes test cases for credit increase and sales transactions, and ensures the system works correctly under high load and concurrent access.
Project Structure

Models: Defines the models and architecture of the system.
Views: Handles API requests and responses.
Serializers: Manages the serialization and deserialization of data.
Tests: Includes test cases for ensuring the correctness and robustness of the system.

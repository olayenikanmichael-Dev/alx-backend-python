# Python Generators Project — Task 0: Getting Started with Python Generators

## 📘 About the Project
This project introduces the foundational step in working with **Python generators** and efficient data handling using **MySQL databases**.  
The first task focuses on creating and populating a database that will later be used for generator-based data streaming and memory-efficient data processing.

---

## 🎯 Objective
Create a Python script `seed.py` that:
1. Connects to a MySQL server.
2. Creates a database named **`ALX_prodev`** (if it doesn’t exist).
3. Creates a table **`user_data`** with appropriate fields.
4. Inserts sample user records from a CSV file (`user_data.csv`).

---

## 🧠 Learning Objectives
By completing this task, you will:
- Understand how to connect Python with MySQL databases.
- Learn how to create databases and tables programmatically.
- Practice reading and inserting CSV data into SQL tables.
- Set up the environment for later tasks involving **Python generators** for streaming and live data processing.

---

## 🧩 Database Schema

**Database:** `ALX_prodev`  
**Table:** `user_data`

| Column Name | Data Type | Description | Constraints |
|--------------|------------|-------------|--------------|
| `user_id` | CHAR(36) | Unique user identifier (UUID) | Primary Key, Indexed |
| `name` | VARCHAR(255) | User full name | NOT NULL |
| `email` | VARCHAR(255) | User email address | NOT NULL |
| `age` | DECIMAL | User age | NOT NULL |

---

## 🧰 Files

| File Name | Description |
|------------|--------------|
| `seed.py` | Python script to create the database, table, and seed data. |
| `0-main.py` | Test script provided to validate the setup. |
| `user_data.csv` | Sample dataset containing user information. |
| `README.md` | Project documentation. |

---

## ⚙️ Setup Instructions

### 1. Install Requirements
Make sure you have **MySQL Server** and the **MySQL Connector for Python** installed.

```bash
sudo apt update
sudo apt install mysql-server
pip install mysql-connector-python

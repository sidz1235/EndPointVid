import psycopg2

# Define the connection parameters
hostname = '49.206.192.143'
username = 'postgres'
password = 'gres@$#5678'
database = 'vdanalyse'

# Connect to the PostgreSQL server
try:
    conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname
    )
    print("Connected to the database")
    
    # Create a cursor object
    cur = conn.cursor()

    # Create the performance table
    cur.execute("""
    CREATE TABLE performance_data (
        member_id SERIAL PRIMARY KEY,
        Country_Code INT,
        Mobile_Number VARCHAR(15),
        Duration INT,
        Total_Words INT,
        Filler_Words_Per_Minute INT,
        Average_Words_Per_Minute INT,
        Fillers_Per_Minute INT,
        Average_Fillers_Per_Minute INT,
        Eye_Contact_Percentage FLOAT,
        Num_Pauses INT,
        Total_Pause_Time FLOAT,
        Soft_Voices_Percentage FLOAT,
        Medium_Voices_Percentage FLOAT,
        High_Voices_Percentage FLOAT,
        file_name VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    print("Table 'performance' created successfully.")

    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"Unable to connect to the database: {e}")

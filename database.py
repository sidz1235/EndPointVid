
import psycopg2

# Define the connection parameters
hostname = '49.206.192.143'
username = 'postgres'
password = 'gres@$#5678'
database = 'vdanalyse'

# Connect to the PostgreSQL server
try:
    mydb = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname
    )
    # print("Connected to the database")
    
    # Create a cursor object
    
except psycopg2.Error as e:
    pass
    # print(f"Unable to connect to the database: {e}")

cur = mydb.cursor()

def insert_data(databasedata):
    insert_query = """
            INSERT INTO performance_data (
                Country_Code, Mobile_Number, Duration, Total_Words, Filler_Words_Per_Minute,
                Average_Words_Per_Minute, Fillers_Per_Minute,
                Average_Fillers_Per_Minute, Eye_Contact_Percentage,
                Num_Pauses, Total_Pause_Time, Soft_Voices_Percentage,
                Medium_Voices_Percentage, High_Voices_Percentage , file_name
            ) VALUES (
                %(Country_Code)s, %(Mobile_Number)s, %(Duration)s, %(Total_Words)s, %(Filler_Words_Per_Minute)s,
                %(Average_Words_Per_Minute)s, %(Fillers_Per_Minute)s,
                %(Average_Fillers_Per_Minute)s, %(Eye_Contact_Percentage)s,
                %(Num_Pauses)s, %(Total_Pause_Time)s, %(Soft_Voices_Percentage)s,
                %(Medium_Voices_Percentage)s, %(High_Voices_Percentage)s , %(file_name)s
            )
    """
    
    cur.execute(insert_query, databasedata)
    mydb.commit()
    
    print("Data inserted successfully in db!")



def fetch_data_by_mobile_number(mobile_number, country_code):
    cur.execute("""
    SELECT Duration, Total_Words, Soft_Voices_Percentage, Medium_Voices_Percentage, 
           High_Voices_Percentage, Eye_Contact_Percentage, Fillers_Per_Minute, 
           Num_Pauses, file_name, created_at
    FROM performance_data
    WHERE Mobile_Number = %s AND Country_Code = %s
    ORDER BY created_at DESC;
    """, (mobile_number, country_code))
    
    # Fetch all rows as JSON objects
    rows_as_json = []
    for row in cur.fetchall():
        duration, total_words, soft_voice, medium_voice, high_voice, eye_contact, fillers, pauses, file_name, datetime = row
        row_json = {
            "FileName": file_name,
            "Duration": duration,
            "Total Words": total_words,
            "Soft Voice Percentage": soft_voice,
            "Medium Voice Percentage": medium_voice,
            "High Voice Percentage": high_voice,
            "Eye Contact Percentage": eye_contact,
            "Fillers per Minute": fillers,
            "Pauses": pauses,
            "Date and Time": datetime.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
        }
        rows_as_json.append(row_json)
    

    return rows_as_json


    


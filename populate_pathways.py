import mysql.connector
import os


# Database connection setup
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="dmurph64",
        password=input("Enter MySQL password: "),
        database="dmurph64"
    )


# Function to insert basic pathway data
def insert_basic_pathway(cursor, pathway_id, pathway_name):
    insert_query = """
    INSERT INTO Pathway (pathway_id, pathway_name)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE pathway_name = VALUES(pathway_name)
    """
    cursor.execute(insert_query, (pathway_id, pathway_name))


# Function to update pathway details
def update_pathway_details(cursor, pathway_id, description, class_name):
    update_query = """
    UPDATE Pathway
    SET description = %s, class = %s
    WHERE pathway_id = %s
    """
    cursor.execute(update_query, (description, class_name, pathway_id))


# Function to process ecoli_pathways.txt
def process_ecoli_pathways(file_path, cursor):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            # Split pathway ID and name
            pathway_id, pathway_name = line.split("\t", 1)
            # Extract numeric part of pathway_id (e.g., from 'eco01100' to 1100)
            pathway_id = int(pathway_id[3:])

            # Remove 'Escherichia coli K-12 MG1655' from pathway_name
            pathway_name = pathway_name.replace(" - Escherichia coli K-12 MG1655", "").strip()

            insert_basic_pathway(cursor, pathway_id, pathway_name)

# Function to process detailed pathway files
def process_detailed_files(directory_path, cursor):
    details_subdir = os.path.join(directory_path, "pathway_details")

    if not os.path.isdir(details_subdir):
        print(f"Error: Subdirectory {details_subdir} not found.")
        return

    for filename in os.listdir(details_subdir):
        file_path = os.path.join(details_subdir, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt") and filename.startswith("eco"):
            with open(file_path, 'r') as file:
                pathway_id = None
                description = []
                class_name = None
                in_description = False  # Flag for handling multiline DESCRIPTION

                for line in file:
                    line = line.strip()

                    if line.startswith("ENTRY"):
                        pathway_id = int(line.split()[1][3:])  # Extract numeric ID
                    elif line.startswith("DESCRIPTION"):
                        # Start capturing DESCRIPTION (multiline)
                        in_description = True
                        description.append(line.split("DESCRIPTION", 1)[1].strip())
                    elif in_description:
                        if line and not line.startswith("CLASS"):
                            description.append(line.strip())
                        else:
                            in_description = False  # End of DESCRIPTION
                            if line.startswith("CLASS"):
                                class_name = line.split("CLASS", 1)[1].strip()
                    elif line.startswith("CLASS"):
                        class_name = line.split("CLASS", 1)[1].strip()

                # Join multiline DESCRIPTION into a single string
                description = " ".join(description) if description else None

                if pathway_id and (description or class_name):
                    update_pathway_details(cursor, pathway_id, description, class_name)
                    if not class_name:
                        print(f"Warning: Missing class for pathway_id {pathway_id}")

# Main function to populate the database
def populate_database():
    db = connect_to_database()
    cursor = db.cursor()

    # Base directory containing the files
    base_directory = "/var/www/html/dmurph64/finalproject"
    ecoli_pathways_file = os.path.join(base_directory, "ecoli_pathways.txt")

    # Process basic pathways
    print("Processing basic pathways...")
    process_ecoli_pathways(ecoli_pathways_file, cursor)

    # Process detailed pathway files
    print("Processing detailed pathway files...")
    process_detailed_files(base_directory, cursor)

    # Commit and close connection
    db.commit()
    cursor.close()
    db.close()
    print("Database population complete.")


if __name__ == "__main__":
    populate_database()

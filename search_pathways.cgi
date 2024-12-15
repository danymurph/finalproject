#!/usr/bin/env python3
import os
import json
import cgi
import cgitb
import mysql.connector

# Enable debugging
cgitb.enable()

def connect_db():
    try:
        return mysql.connector.connect(
            user=os.environ.get('DB_USER', 'dmurph64'),
            password=os.environ.get('DB_PASSWORD', 'P@ssw0rd'),
            host=os.environ.get('DB_HOST', 'localhost'),
            database=os.environ.get('DB_NAME', 'dmurph64')
        )
    except mysql.connector.Error as err:
        log_error(err)
        return None

def log_error(error):
    # Ensure the log directory exists and has appropriate permissions
    log_file_path = '/var/log/cgi_errors.log'
    try:
        with open(log_file_path, 'a') as log_file:
            log_file.write(str(error) + '\n')
    except Exception as e:
        # If logging fails, print to stderr (visible in server logs)
        print("Content-Type: text/plain\n")
        print("An error occurred and could not be logged.")
        print(str(e))
        exit()

def clean_pathway_name(name):
    return name.replace(" - Escherichia coli K-12 MG1655", "").strip()

def search_pathways(cursor, keyword, limit=10):
    query = """
        SELECT pathway_id, pathway_name, description, class
        FROM Pathway
        WHERE pathway_name LIKE %s OR description LIKE %s
        ORDER BY pathway_name ASC
        LIMIT %s
    """
    search_term = f"%{keyword}%"
    cursor.execute(query, (search_term, search_term, limit))
    results = cursor.fetchall()

    for result in results:
        result['pathway_name'] = clean_pathway_name(result['pathway_name'])
        result['class'] = result.get('class', 'Unclassified').strip()
    return results

def suggest_pathways(cursor, keyword, limit=5):
    query = """
        SELECT DISTINCT pathway_name, class
        FROM Pathway
        WHERE pathway_name LIKE %s
        ORDER BY pathway_name ASC
        LIMIT %s
    """
    search_term = f"{keyword}%"
    cursor.execute(query, (search_term, limit))
    results = cursor.fetchall()
    suggestions = [
        {
            "pathway_name": clean_pathway_name(row['pathway_name']),
            "class": row.get('class', 'Unclassified').strip()
        }
        for row in results
    ]
    return suggestions

def main():
    form = cgi.FieldStorage()
    action = form.getfirst("action", "").strip().lower()
    keyword = form.getfirst("keyword", "").strip()

    print("Content-Type: application/json\n")

    if not keyword:
        response = {"error": "Missing 'keyword' parameter."}
        print(json.dumps(response))
        return

    conn = connect_db()
    if not conn:
        response = {"error": "Database connection failed."}
        print(json.dumps(response))
        return

    cursor = conn.cursor(dictionary=True)
    try:
        if action == "search":
            results = search_pathways(cursor, keyword)
            print(json.dumps(results))
        elif action == "suggest":
            suggestions = suggest_pathways(cursor, keyword)
            print(json.dumps(suggestions))
        else:
            response = {"error": "Invalid 'action' parameter."}
            print(json.dumps(response))
    except mysql.connector.Error as err:
        log_error(err)
        response = {"error": "An error occurred while processing your request."}
        print(json.dumps(response))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

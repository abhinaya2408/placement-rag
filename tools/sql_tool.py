from tools.db_connection import get_connection


def execute_query(query):

    try:

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    except Exception as e:

        return str(e)
import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from news_script import initialize_db, check_response, fetch_news_from_api, populate_db, get_news_from_db

class TestNewsScript(unittest.TestCase):

    @patch('news_script.requests.get')
    def test_check_response(self, mock_get):
        # Test a successful response
        mock_get.return_value.status_code = 200
        response = mock_get()
        try:
            check_response(response)
        except Exception:
            self.fail("check_response() raised Exception unexpectedly for status code 200")

        # Test an unsuccessful response
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = 'Not Found'
        response = mock_get()
        with self.assertRaises(Exception):
            check_response(response)

    @patch('news_script.sqlite3.connect')
    def test_initialize_db(self, mock_connect):
        # Mocking the database connection and cursor
        mock_conn = MagicMock(sqlite3.Connection)
        mock_cursor = MagicMock(sqlite3.Cursor)
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        connection, cursor = initialize_db()

        # Ensure that the database and table are created
        mock_cursor.execute.assert_called_with('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                category TEXT,
                description TEXT
            )
        ''')
        mock_conn.commit.assert_called_once()
        self.assertEqual(connection, mock_conn)
        self.assertEqual(cursor, mock_cursor)

    @patch('news_script.requests.get')
    def test_fetch_news_from_api(self, mock_get):
        # Mocking the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'results': [{'description': 'Sample news 1'}, {'description': 'Sample news 2'}]
        }
        category = 'sports'
        news_list = fetch_news_from_api(category)
        self.assertEqual(len(news_list), 2)
        self.assertIn('Sample news 1', news_list)
        self.assertIn('Sample news 2', news_list)

    @patch('news_script.sqlite3.connect')
    def test_populate_db(self, mock_connect):
        # Mocking the database connection and cursor
        mock_conn = MagicMock(sqlite3.Connection)
        mock_cursor = MagicMock(sqlite3.Cursor)
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        connection, cursor = initialize_db()
        category = 'sports'
        news = 'Sample sports news'
        populate_db(connection, cursor, category, news)
        
        # Ensure that the news is inserted into the database
        mock_cursor.execute.assert_called_with(
            'INSERT INTO news (category, description) VALUES (?, ?)',
            (category, news)
        )
        mock_conn.commit.assert_called_once()

    @patch('news_script.sqlite3.connect')
    def test_get_news_from_db(self, mock_connect):
        # Mocking the database connection and cursor
        mock_conn = MagicMock(sqlite3.Connection)
        mock_cursor = MagicMock(sqlite3.Cursor)
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Setting up the cursor fetchall return value
        category = 'sports'
        mock_cursor.fetchall.return_value = [('Sample sports news',)]
        
        connection, cursor = initialize_db()
        news_list = get_news_from_db(cursor, category)
        
        # Ensure the correct query is executed
        mock_cursor.execute.assert_called_with('SELECT description FROM news WHERE category = ?', (category,))
        self.assertEqual(len(news_list), 1)
        self.assertEqual(news_list[0], 'Sample sports news')

if __name__ == '__main__':
    unittest.main()

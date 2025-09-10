#!/usr/bin/env python3
"""
Database migration script to add detected_objects field to Photo model.
This script adds the detected_objects column to store ML-detected objects as JSON.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from flask import Flask
from moments.core.extensions import db
from sqlalchemy import text

def create_app():
    """Create Flask app for migration."""
    app = Flask('moments')
    from moments.settings import DevelopmentConfig
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    return app

def migrate_detected_objects():
    """Add detected_objects column to photo table."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("""
                SELECT COUNT(*) as count 
                FROM pragma_table_info('photo') 
                WHERE name = 'detected_objects'
            """)).fetchone()
            
            if result.count > 0:
                print("Column 'detected_objects' already exists in photo table.")
                return
            
            # Add the detected_objects column
            db.session.execute(text("""
                ALTER TABLE photo 
                ADD COLUMN detected_objects TEXT
            """))
            
            db.session.commit()
            print("Successfully added 'detected_objects' column to photo table.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error adding detected_objects column: {e}")
            raise

if __name__ == '__main__':
    migrate_detected_objects()

#!/usr/bin/env python3
"""
Database migration script to add alt_text column for ML-generated alternative text.
Run this script after updating the Photo model to add the new field.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from moments import create_app
from moments.core.extensions import db
from sqlalchemy import text

def migrate_alt_text():
    """Add alt_text column to photo table."""
    app = create_app('development')
    
    with app.app_context():
        try:
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('photo')]
            
            if 'alt_text' in columns:
                print("Column 'alt_text' already exists in photo table.")
                return
            
            # Add the new column
            print("Adding alt_text column to photo table...")
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE photo ADD COLUMN alt_text VARCHAR(500)"))
                conn.commit()
            
            print("✅ Database migration completed successfully!")
            print("Column 'alt_text' added to photo table.")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            sys.exit(1)

if __name__ == '__main__':
    migrate_alt_text()

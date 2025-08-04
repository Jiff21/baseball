#!/usr/bin/env python3
"""
Database migration script to add wins/losses columns to the teams table.
This script adds the new vs_lefty_wins, vs_lefty_losses, vs_righty_wins, vs_righty_losses columns.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from sqlalchemy import text

def migrate_database():
    """Add wins/losses columns to the teams table."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if columns already exist
            result = db.engine.execute(text("PRAGMA table_info(teams)"))
            columns = [row[1] for row in result]
            
            columns_to_add = [
                'vs_lefty_wins',
                'vs_lefty_losses', 
                'vs_righty_wins',
                'vs_righty_losses'
            ]
            
            existing_new_columns = [col for col in columns_to_add if col in columns]
            missing_columns = [col for col in columns_to_add if col not in columns]
            
            if existing_new_columns:
                print(f"✅ These columns already exist: {existing_new_columns}")
            
            if not missing_columns:
                print("✅ All wins/losses columns already exist in the database!")
                return True
                
            print(f"🔧 Adding missing columns: {missing_columns}")
            
            # Add missing columns
            for column in missing_columns:
                sql = f"ALTER TABLE teams ADD COLUMN {column} INTEGER DEFAULT 0"
                print(f"   Executing: {sql}")
                db.engine.execute(text(sql))
            
            # Commit the changes
            db.session.commit()
            
            print("✅ Database migration completed successfully!")
            print("🎯 The following columns were added to the teams table:")
            for column in missing_columns:
                print(f"   - {column} (INTEGER, DEFAULT 0)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during migration: {e}")
            db.session.rollback()
            return False

def verify_migration():
    """Verify that the migration was successful."""
    app = create_app()
    
    with app.app_context():
        try:
            # Check table structure
            result = db.engine.execute(text("PRAGMA table_info(teams)"))
            columns = [row[1] for row in result]
            
            required_columns = [
                'vs_lefty_wins',
                'vs_lefty_losses', 
                'vs_righty_wins',
                'vs_righty_losses'
            ]
            
            missing = [col for col in required_columns if col not in columns]
            
            if missing:
                print(f"❌ Migration verification failed. Missing columns: {missing}")
                return False
            else:
                print("✅ Migration verification successful! All wins/losses columns exist.")
                print("📊 Current teams table structure includes:")
                for col in required_columns:
                    print(f"   - {col}")
                return True
                
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            return False

def main():
    """Main function to run the migration."""
    print("🏗️  DATABASE MIGRATION: Adding Wins/Losses Columns")
    print("=" * 60)
    
    # Run migration
    if migrate_database():
        print("\n🔍 Verifying migration...")
        if verify_migration():
            print("\n🎉 Migration completed successfully!")
            print("\nNext steps:")
            print("1. Restart your Flask application")
            print("2. Run the data refresh endpoint: POST /api/refresh-data")
            print("3. The new wins/losses data will be populated with sample values")
        else:
            print("\n❌ Migration verification failed!")
            sys.exit(1)
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()


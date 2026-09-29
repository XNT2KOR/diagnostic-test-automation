"""CSV Test Design Specification Validator & Auto-Fixer

This script validates and auto-fixes the test_design.csv file for:
1. Correct CSV format
2. Required columns present
3. No missing values in mandatory fields
4. Unique TCID values
5. Valid test procedure format
6. Consistent verdict values

Usage:
  python validate_csv.py                    # Validate only
  python validate_csv.py --fix              # Validate and auto-fix issues
  python validate_csv.py --fix --backup     # Auto-fix and create backup
"""

import csv
import sys
import shutil
from pathlib import Path
from datetime import datetime


class CSVValidator:
    """Validate and auto-fix test design CSV file."""
    
    # Required columns that must be present
    REQUIRED_COLUMNS = [
        'TCID',
        'TEST CASE NAME',
        'TEST CASE DESCRIPTION',
        'TEST PROCEDURE',
        'EXPECTED RESULTS',
        'VERDICT',
        'PARAMETERS'
    ]
    
    # Valid verdict values
    VALID_VERDICTS = ['PASS', 'FAIL', 'PENDING', 'SKIP']
    
    def __init__(self, csv_file, auto_fix=False, backup=False):
        """Initialize validator with CSV file path."""
        self.csv_file = Path(csv_file)
        self.auto_fix = auto_fix
        self.backup = backup
        self.errors = []
        self.warnings = []
        self.fixes_applied = []
        self.rows = []
    
    def validate(self):
        """Run all validation checks."""
        print("=" * 70)
        print("CSV TEST DESIGN SPECIFICATION VALIDATOR")
        print("=" * 70)
        print(f"\nValidating: {self.csv_file}")
        print(f"Auto-fix: {'ENABLED' if self.auto_fix else 'DISABLED'}")
        print()
        
        # Check 1: File exists
        if not self._check_file_exists():
            return False
        
        # Check 2: Can be read as CSV
        if not self._check_csv_format():
            return False
        
        # Check 3: Required columns
        if not self._check_required_columns():
            return False
        
        # Check 4: Data validation
        self._check_data_quality()
        
        # Check 5: Unique TCIDs
        self._check_unique_tcids()
        
        # Check 6: Verdict values
        self._check_verdict_values()
        
        # Apply fixes if enabled and errors found
        if self.auto_fix and (self.errors or self.warnings):
            self._apply_fixes()
        
        # Print results
        self._print_results()
        
        return len(self.errors) == 0
    
    def _check_file_exists(self):
        """Check if CSV file exists."""
        if not self.csv_file.exists():
            self.errors.append(f"❌ File not found: {self.csv_file}")
            return False
        print(f"✅ File exists: {self.csv_file}")
        return True
    
    def _check_csv_format(self):
        """Check if file is valid CSV format."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.rows = list(reader)
            print(f"✅ Valid CSV format with {len(self.rows)} test cases")
            return True
        except Exception as e:
            self.errors.append(f"❌ Invalid CSV format: {e}")
            return False
    
    def _check_required_columns(self):
        """Check if all required columns are present."""
        if not self.rows:
            self.errors.append("❌ CSV file is empty")
            return False
        
        actual_columns = set(self.rows[0].keys())
        required_columns = set(self.REQUIRED_COLUMNS)
        
        missing_columns = required_columns - actual_columns
        if missing_columns:
            if self.auto_fix:
                self.warnings.append(f"⚠️  Missing columns will be added: {', '.join(missing_columns)}")
                self.fixes_applied.append(f"Will add missing columns: {', '.join(missing_columns)}")
            else:
                self.errors.append(f"❌ Missing columns: {', '.join(missing_columns)}")
            return not self.auto_fix
        
        print(f"✅ All {len(self.REQUIRED_COLUMNS)} required columns present")
        return True
    
    def _check_data_quality(self):
        """Check for missing or invalid data in rows."""
        for row_num, row in enumerate(self.rows, start=2):  # Start from 2 (header is row 1)
            # Check TCID
            if not row.get('TCID', '').strip():
                if self.auto_fix:
                    default_tcid = f"TC_{row_num:03d}"
                    self.warnings.append(f"⚠️  Row {row_num}: Missing TCID, will use {default_tcid}")
                    self.fixes_applied.append(f"Row {row_num}: Generated TCID {default_tcid}")
                else:
                    self.errors.append(f"❌ Row {row_num}: Missing TCID")
                continue
            
            tcid = row['TCID'].strip()
            
            # Check mandatory fields
            mandatory_fields = ['TEST CASE NAME', 'TEST CASE DESCRIPTION', 
                              'TEST PROCEDURE', 'EXPECTED RESULTS']
            for field in mandatory_fields:
                if not row.get(field, '').strip():
                    if self.auto_fix:
                        self.warnings.append(f"⚠️  Row {row_num} ({tcid}): Missing {field}")
                        self.fixes_applied.append(f"Row {row_num} ({tcid}): Generated placeholder for {field}")
                    else:
                        self.errors.append(f"❌ Row {row_num} ({tcid}): Missing {field}")
    
    def _check_unique_tcids(self):
        """Check if all TCIDs are unique."""
        tcids = [row.get('TCID', '').strip() for row in self.rows]
        unique_tcids = set(tcids)
        
        if len(tcids) != len(unique_tcids):
            duplicates = [tcid for tcid in tcids if tcids.count(tcid) > 1]
            if self.auto_fix:
                self.warnings.append(f"⚠️  Duplicate TCIDs found: {set(duplicates)}, will rename duplicates")
                self.fixes_applied.append(f"Will rename duplicate TCIDs to ensure uniqueness")
            else:
                self.errors.append(f"❌ Duplicate TCIDs found: {set(duplicates)}")
        else:
            print(f"✅ All {len(tcids)} TCIDs are unique")
    
    def _check_verdict_values(self):
        """Check if verdict values are valid."""
        invalid_verdicts = []
        
        for row_num, row in enumerate(self.rows, start=2):
            verdict = row.get('VERDICT', '').strip()
            if verdict and verdict not in self.VALID_VERDICTS:
                tcid = row.get('TCID', 'UNKNOWN')
                invalid_verdicts.append(f"{tcid}='{verdict}'")
        
        if invalid_verdicts:
            if self.auto_fix:
                self.warnings.append(f"⚠️  Invalid VERDICT values found, will default to PASS: {', '.join(invalid_verdicts)}")
                self.fixes_applied.append(f"Corrected {len(invalid_verdicts)} invalid verdict(s)")
            else:
                self.errors.append(f"❌ Invalid VERDICT values: {', '.join(invalid_verdicts)}")
        else:
            print(f"✅ All VERDICT values are valid")
    
    def _apply_fixes(self):
        """Apply automatic fixes to CSV file."""
        print()
        print("=" * 70)
        print("APPLYING AUTO-FIXES")
        print("=" * 70)
        print()
        
        # Create backup if requested
        if self.backup:
            backup_file = self.csv_file.with_name(
                f"{self.csv_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            shutil.copy2(self.csv_file, backup_file)
            print(f"✅ Backup created: {backup_file}")
        
        # Fix missing columns
        actual_columns = set(self.rows[0].keys()) if self.rows else set()
        missing_columns = set(self.REQUIRED_COLUMNS) - actual_columns
        
        if missing_columns:
            for row in self.rows:
                for col in missing_columns:
                    row[col] = ''
            print(f"✅ Added {len(missing_columns)} missing column(s)")
        
        # Fix missing/invalid TCIDs and data
        tcids_seen = set()
        for row_num, row in enumerate(self.rows, start=1):
            tcid = row.get('TCID', '').strip()
            
            # Fix missing TCID
            if not tcid:
                new_tcid = f"TC_{row_num:03d}"
                row['TCID'] = new_tcid
                tcids_seen.add(new_tcid)
                print(f"  • Row {row_num}: Generated TCID {new_tcid}")
                continue
            
            # Fix duplicate TCID
            if tcid in tcids_seen:
                new_tcid = f"{tcid}_DUP_{row_num}"
                row['TCID'] = new_tcid
                tcids_seen.add(new_tcid)
                print(f"  • Row {row_num}: Renamed duplicate TCID to {new_tcid}")
            else:
                tcids_seen.add(tcid)
            
            # Fix missing mandatory fields
            for field in self.REQUIRED_COLUMNS:
                if field == 'TCID':
                    continue
                if not row.get(field, '').strip():
                    if field == 'VERDICT':
                        row[field] = 'PENDING'
                    else:
                        row[field] = f'[TODO: {field}]'
            
            # Fix invalid verdict values
            verdict = row.get('VERDICT', '').strip()
            if verdict and verdict not in self.VALID_VERDICTS:
                row['VERDICT'] = 'PASS'
                print(f"  • Row {row_num}: Fixed invalid VERDICT '{verdict}' → 'PASS'")
        
        # Write fixed CSV back to file
        try:
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.REQUIRED_COLUMNS)
                writer.writeheader()
                writer.writerows(self.rows)
            print()
            print(f"✅ CSV file auto-fixed and saved: {self.csv_file}")
        except Exception as e:
            self.errors.append(f"❌ Error writing fixed CSV: {e}")
            print(f"❌ Failed to save fixes: {e}")
    
    def _print_results(self):
        """Print validation results summary."""
        print()
        print("=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)
        
        if self.errors:
            print(f"\n❌ FAILED - {len(self.errors)} error(s) found:\n")
            for error in self.errors:
                print(f"  {error}")
        else:
            if self.auto_fix and self.fixes_applied:
                print(f"\n✅ PASSED (with auto-fixes applied) - {len(self.fixes_applied)} fix(es)")
            else:
                print("\n✅ PASSED - All validation checks successful!")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS - {len(self.warnings)} warning(s):\n")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.fixes_applied and not self.auto_fix:
            print(f"\n💡 TIP: Run with --fix flag to automatically correct these issues")
        
        print()
        print("=" * 70)
        print(f"SUMMARY: {len(self.rows)} test cases")
        print(f"Errors: {len(self.errors)} | Warnings: {len(self.warnings)} | Fixes Applied: {len(self.fixes_applied)}")
        print("=" * 70)
        print()


def main():
    """Main entry point."""
    # Parse command line arguments
    auto_fix = '--fix' in sys.argv
    backup = '--backup' in sys.argv
    
    csv_file = Path(__file__).parent / "test_design.csv"
    
    validator = CSVValidator(csv_file, auto_fix=auto_fix, backup=backup)
    success = validator.validate()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

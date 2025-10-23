"""
Crosstab Parser for Survey Detailed Tables
Parses Environics-style banner/crosstab Excel files
"""

import pandas as pd
import json
import re
from typing import Dict, List, Tuple, Any


class CrosstabParser:
    """Parse survey crosstab/banner tables into structured data"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.xl_file = pd.ExcelFile(file_path)
        self.sheets = {}
        self.questions = []

    def parse_all_sheets(self) -> Dict[str, Any]:
        """Parse all sheets in the Excel file"""
        result = {
            'metadata': {
                'filename': self.file_path.split('/')[-1],
                'sheets': self.xl_file.sheet_names,
                'total_questions': 0
            },
            'banners': {}
        }

        for sheet_name in self.xl_file.sheet_names:
            print(f"Parsing {sheet_name}...")
            banner_data = self.parse_banner(sheet_name)
            result['banners'][sheet_name] = banner_data

        # Get total questions from first banner
        if result['banners']:
            first_banner = list(result['banners'].values())[0]
            result['metadata']['total_questions'] = len(first_banner['questions'])

        return result

    def parse_banner(self, sheet_name: str) -> Dict[str, Any]:
        """Parse a single banner sheet"""
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)

        # Find header information
        demographic_headers, header_row_idx = self._find_demographic_headers(df)
        column_labels, label_row_idx = self._find_column_labels(df)

        # Find all questions
        questions = self._find_questions(df)

        # Parse each question's data
        parsed_questions = []
        for q in questions:
            question_data = self._parse_question_data(
                df, q, demographic_headers, column_labels
            )
            parsed_questions.append(question_data)

        # Check for INDICES TABLE
        indices_data = self._find_and_parse_indices(df, demographic_headers, column_labels)
        if indices_data:
            parsed_questions.append(indices_data)

        # Generate a descriptive name based on demographics
        banner_display_name = self._generate_banner_display_name(demographic_headers)

        return {
            'sheet_name': sheet_name,
            'display_name': banner_display_name,
            'demographics': demographic_headers,
            'column_labels': column_labels,
            'questions': parsed_questions,
            'total_questions': len(parsed_questions)
        }

    def _generate_banner_display_name(self, demographics: List[Dict]) -> str:
        """Generate a descriptive display name based on demographics"""
        if not demographics:
            return "Total Only"

        # Get unique categories
        categories = []
        seen = set()
        for demo in demographics:
            cat = demo['category']
            if cat not in seen:
                categories.append(cat)
                seen.add(cat)

        # Limit to first 3-4 categories for display
        if len(categories) <= 3:
            return " / ".join(categories)
        else:
            return " / ".join(categories[:3]) + " + more"

    def _find_demographic_headers(self, df: pd.DataFrame) -> Tuple[List[Dict], int]:
        """Find the row containing demographic category headers"""
        for idx in range(min(20, len(df))):
            row = df.iloc[idx]
            # Look for common demographic keywords
            row_text = ' '.join([str(x) for x in row if pd.notna(x)])
            if any(keyword in row_text for keyword in ['Region', 'Age', 'Gender', 'Education',
                                                        'Attendance', 'Frequency', 'Freq',
                                                        'Volunteer', 'Tenure', 'Ministry',
                                                        'happiness', 'Relationships', 'purpose',
                                                        'Understand']):
                # We found the category row (e.g., "Region", "Age", "Gender")
                # The next row contains the actual demographic values
                category_row = df.iloc[idx]
                value_row = df.iloc[idx + 1]

                headers = []
                current_category = None

                # Build mapping of columns to categories
                for col_idx in range(len(category_row)):
                    if pd.notna(category_row[col_idx]):
                        cell_text = str(category_row[col_idx]).strip()
                        # Check if this is a category header (not empty and not just whitespace)
                        if cell_text and len(cell_text) > 2 and cell_text not in ['TOTAL']:
                            # Could be any category name
                            current_category = cell_text

                    # Now get the value from the row below
                    if col_idx > 0 and pd.notna(value_row[col_idx]):
                        value_text = str(value_row[col_idx]).strip()
                        if '\n' in value_text:
                            # Extract all lines before the dashes
                            lines = value_text.split('\n')
                            label_lines = []
                            for line in lines:
                                line = line.strip()
                                if line.startswith('---') or line.startswith('==='):
                                    break
                                if line:
                                    label_lines.append(line)

                            # Join all label lines with space
                            label = ' '.join(label_lines)

                            if label:
                                headers.append({
                                    'category': 'TOTAL' if label == 'TOTAL' else (current_category if current_category else 'Unknown'),
                                    'label': label,
                                    'column_index': col_idx
                                })

                return headers, idx

        return [], -1

    def _find_column_labels(self, df: pd.DataFrame) -> Tuple[List[str], int]:
        """Find row with column labels (A), (B), (C), etc."""
        for idx in range(min(20, len(df))):
            row = df.iloc[idx]
            if pd.notna(row[1]) and '(A)' in str(row[1]):
                labels = []
                for cell in row[1:]:
                    if pd.notna(cell):
                        text = str(cell).strip()
                        # Extract letter from (A), (B), etc.
                        match = re.search(r'\(([A-Z])\)', text)
                        if match:
                            labels.append(match.group(1))
                return labels, idx

        return [], -1

    def _find_questions(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Find all question rows in the dataframe"""
        questions = []

        for idx, row in df.iterrows():
            if pd.notna(row[0]) and isinstance(row[0], str):
                text = str(row[0]).strip()
                # Look for question pattern: Q followed by number and period
                if re.match(r'^Q\d+\.', text):
                    questions.append({
                        'row': idx,
                        'text': text,
                        'id': self._extract_question_id(text)
                    })

        return questions

    def _extract_question_id(self, text: str) -> str:
        """Extract question ID (e.g., 'Q2' from 'Q2. How often...')"""
        match = re.match(r'^(Q\d+)', text)
        return match.group(1) if match else 'Unknown'

    def _find_and_parse_indices(self, df: pd.DataFrame, demographics: List[str],
                                 column_labels: List[str]) -> Dict[str, Any]:
        """Find and parse the INDICES TABLE section"""
        # Look for "INDICES TABLE" marker
        indices_row = -1
        for idx in range(len(df)):
            if pd.notna(df.iloc[idx, 0]):
                text = str(df.iloc[idx, 0]).strip()
                if 'INDICES TABLE' in text:
                    indices_row = idx
                    break

        if indices_row == -1:
            return None

        # Parse indices similar to questions
        response_data = []

        # Start parsing from a few rows after the INDICES TABLE marker
        start_row = indices_row + 5
        end_row = min(start_row + 50, len(df))  # Look ahead up to 50 rows

        for idx in range(start_row, end_row):
            row = df.iloc[idx]

            if pd.notna(row[0]):
                response_text = str(row[0]).strip()

                # Skip certain rows
                skip_patterns = [
                    '====', '----', 'Comparison Groups',
                    'Paired', 'Uppercase', 'Total'
                ]
                if any(pattern in response_text for pattern in skip_patterns):
                    continue

                # Check if this looks like an index name (contains "Index")
                if 'Index' in response_text or response_text in ['SUBSAMPLE']:
                    # Extract values for each demographic column
                    values = []
                    for demo in demographics:
                        col_idx = demo['column_index']
                        if col_idx < len(row):
                            cell_value = row[col_idx]
                            try:
                                if pd.notna(cell_value):
                                    if isinstance(cell_value, str) and '%' in cell_value:
                                        values.append(cell_value)
                                    else:
                                        values.append(float(cell_value))
                                else:
                                    values.append(None)
                            except (ValueError, TypeError):
                                values.append(str(cell_value) if pd.notna(cell_value) else None)
                        else:
                            values.append(None)

                    if values and any(v is not None for v in values):
                        response_data.append({
                            'response': response_text,
                            'values': values
                        })

        if not response_data:
            return None

        return {
            'id': 'INDICES',
            'text': 'INDICES TABLE - Composite Metrics',
            'row': indices_row,
            'responses': response_data
        }

    def _parse_question_data(self, df: pd.DataFrame, question: Dict,
                            demographics: List[str], column_labels: List[str]) -> Dict[str, Any]:
        """Parse data for a specific question"""
        start_row = question['row']

        # Find the end of this question's data (next question, or INDICES TABLE)
        end_row = start_row + 100  # Default lookahead
        for idx in range(start_row + 1, min(start_row + 150, len(df))):
            row_text = str(df.iloc[idx, 0]) if pd.notna(df.iloc[idx, 0]) else ''
            # Stop at next question OR at INDICES TABLE
            if re.match(r'^Q\d+\.', row_text) or 'INDICES TABLE' in row_text:
                end_row = idx
                break

        # Extract response options and their values
        response_data = []

        for idx in range(start_row + 1, min(end_row, len(df))):
            row = df.iloc[idx]

            # Skip empty rows and separator rows
            if pd.notna(row[0]):
                response_text = str(row[0]).strip()

                # Skip certain rows
                skip_patterns = [
                    '====', '----', 'Comparison Groups',
                    'Paired', 'Uppercase', 'SUBSAMPLE'
                ]
                if any(pattern in response_text for pattern in skip_patterns):
                    continue

                if response_text and response_text not in ['']:
                    # Extract values for each demographic column (using their column indices)
                    values = []
                    for demo in demographics:
                        col_idx = demo['column_index']
                        if col_idx < len(row):
                            cell_value = row[col_idx]
                            # Try to convert to numeric, otherwise keep as string
                            try:
                                if pd.notna(cell_value):
                                    # Check if it's a percentage
                                    if isinstance(cell_value, str) and '%' in cell_value:
                                        values.append(cell_value)
                                    else:
                                        values.append(float(cell_value))
                                else:
                                    values.append(None)
                            except (ValueError, TypeError):
                                values.append(str(cell_value) if pd.notna(cell_value) else None)
                        else:
                            values.append(None)

                    if values and any(v is not None for v in values):
                        response_data.append({
                            'response': response_text,
                            'values': values
                        })

        return {
            'id': question['id'],
            'text': question['text'],
            'row': question['row'],
            'responses': response_data
        }

    def export_to_json(self, output_path: str):
        """Export parsed data to JSON file"""
        data = self.parse_all_sheets()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data

    def get_question_by_id(self, question_id: str, banner: str = 'BANNER 1') -> Dict:
        """Get specific question data"""
        data = self.parse_all_sheets()
        if banner in data['banners']:
            for q in data['banners'][banner]['questions']:
                if q['id'] == question_id:
                    return q
        return None

    def get_all_question_ids(self) -> List[str]:
        """Get list of all question IDs"""
        data = self.parse_all_sheets()
        if data['banners']:
            first_banner = list(data['banners'].values())[0]
            return [q['id'] for q in first_banner['questions']]
        return []

    def search_questions(self, search_term: str) -> List[Dict]:
        """Search questions by text"""
        data = self.parse_all_sheets()
        results = []

        if data['banners']:
            first_banner = list(data['banners'].values())[0]
            for q in first_banner['questions']:
                if search_term.lower() in q['text'].lower():
                    results.append({
                        'id': q['id'],
                        'text': q['text']
                    })

        return results


if __name__ == '__main__':
    # Test the parser
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = '/Users/adityashah/Desktop/NAC/Environics - New Apostolic Church - Member Survey - Detailed Tables October 2025.xlsx'

    print(f"Parsing: {file_path}")
    parser = CrosstabParser(file_path)

    # Export to JSON
    output_file = 'crosstab_data.json'
    data = parser.export_to_json(output_file)

    print(f"\n✓ Parsed successfully!")
    print(f"✓ Total sheets: {len(data['banners'])}")
    print(f"✓ Total questions: {data['metadata']['total_questions']}")
    print(f"✓ Exported to: {output_file}")

    # Show sample question
    if data['banners']:
        first_banner = list(data['banners'].values())[0]
        if first_banner['questions']:
            sample_q = first_banner['questions'][0]
            print(f"\n=== Sample Question ===")
            print(f"ID: {sample_q['id']}")
            print(f"Text: {sample_q['text'][:100]}...")
            print(f"Responses: {len(sample_q['responses'])}")

#!/usr/bin/env python3.11
"""
Update Google Docs with content and apply bold formatting
"""

import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Document IDs
QUESTIONS_DOC_ID = "1CYECMcw8pPu-a7H27ChbKcRWVnV7PQJKy5QHsSvJElw"
COMMENTS_DOC_ID = "1trD4JzyBQtHEKXt0lVWPfayGo89kM182T_HXAupYP3A"

SCOPES = ['https://www.googleapis.com/auth/documents']

def get_credentials():
    """Load credentials from token file"""
    token_file = '/home/ubuntu/token.json'
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    return creds

def append_and_format(service, doc_id, content):
    """Append content and apply bold formatting to titles/headers"""
    try:
        # Step 1: Get current end index
        document = service.documents().get(documentId=doc_id).execute()
        end_index = document.get('body').get('content')[-1].get('endIndex') - 1
        
        # Step 2: Insert the text
        insert_request = [{
            'insertText': {
                'location': {'index': end_index},
                'text': f'\n\n{content}'
            }
        }]
        
        service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': insert_request}
        ).execute()
        
        # Step 3: Get the document again to find what we just inserted
        document = service.documents().get(documentId=doc_id).execute()
        
        # Step 4: Find and format the newly added text
        format_requests = []
        content_elements = document.get('body').get('content')
        
        for element in content_elements:
            if 'paragraph' in element:
                paragraph = element['paragraph']
                if 'elements' in paragraph:
                    for elem in paragraph['elements']:
                        if 'textRun' in elem:
                            text_run = elem['textRun']
                            text = text_run.get('content', '')
                            start_index = elem['startIndex']
                            end_index = elem['endIndex']
                            
                            # Only format if this is in the range we just added
                            if start_index >= end_index - len(content) - 10:
                                text_stripped = text.strip()
                                should_bold = False
                                
                                if text_stripped:
                                    # Check patterns
                                    if ('=' * 10 in text or '-' * 10 in text or
                                        text_stripped.startswith('GENERATED:') or
                                        text_stripped.startswith('QUESTION ') or
                                        text_stripped.startswith('RESPONSE ') or
                                        text_stripped.startswith('TITLE:') or
                                        text_stripped.startswith('POST BODY:') or
                                        text_stripped.startswith('YOUR RESPONSE:') or
                                        text_stripped.startswith('POST:') or
                                        text_stripped.startswith('AUTHOR:') or
                                        text_stripped.startswith('URL:')):
                                        should_bold = True
                                
                                if should_bold:
                                    format_requests.append({
                                        'updateTextStyle': {
                                            'range': {
                                                'startIndex': start_index,
                                                'endIndex': end_index
                                            },
                                            'textStyle': {'bold': True},
                                            'fields': 'bold'
                                        }
                                    })
        
        # Step 5: Apply formatting
        if format_requests:
            service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': format_requests}
            ).execute()
        
        return True
        
    except HttpError as error:
        print(f'An error occurred: {error}')
        return False
    except Exception as e:
        print(f'Error: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

def update_docs(questions_file, responses_file):
    """Update both Google Docs with formatted content"""
    
    print("=" * 80)
    print("UPDATING GOOGLE DOCS (WITH FORMATTING)")
    print("=" * 80)
    print()
    
    # Get credentials
    creds = get_credentials()
    
    # Build the service
    service = build('docs', 'v1', credentials=creds)
    
    # Read and update questions
    try:
        with open(questions_file, 'r') as f:
            questions_content = f.read()
        
        print(f"📝 Updating Questions Doc...")
        print(f"   File: {questions_file}")
        print(f"   Length: {len(questions_content)} characters")
        
        if append_and_format(service, QUESTIONS_DOC_ID, questions_content):
            print(f"   ✅ Success (with bold formatting)!")
        else:
            print(f"   ❌ Failed")
        print()
        
    except Exception as e:
        print(f"❌ Error with questions: {str(e)}")
        print()
    
    # Read and update responses
    try:
        with open(responses_file, 'r') as f:
            responses_content = f.read()
        
        print(f"💬 Updating Comments Doc...")
        print(f"   File: {responses_file}")
        print(f"   Length: {len(responses_content)} characters")
        
        if append_and_format(service, COMMENTS_DOC_ID, responses_content):
            print(f"   ✅ Success (with bold formatting)!")
        else:
            print(f"   ❌ Failed")
        print()
        
    except Exception as e:
        print(f"❌ Error with responses: {str(e)}")
        print()
    
    print("=" * 80)
    print("✅ GOOGLE DOCS UPDATED!")
    print("=" * 80)
    print()
    print("View your docs:")
    print(f"  Questions: https://docs.google.com/document/d/{QUESTIONS_DOC_ID}/edit")
    print(f"  Comments:  https://docs.google.com/document/d/{COMMENTS_DOC_ID}/edit")
    print()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3.11 update_and_format_docs.py <questions_file> <responses_file>")
        sys.exit(1)
    
    questions_file = sys.argv[1]
    responses_file = sys.argv[2]
    
    try:
        update_docs(questions_file, responses_file)
    except Exception as e:
        print()
        print("❌ ERROR")
        print()
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()

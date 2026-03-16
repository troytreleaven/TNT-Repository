#!/usr/bin/env python3
"""
Google Forms Creator - Lead with Impact Survey
Creates a professional survey in Google Forms
"""

import os
import sys
import json

# Google Forms API setup
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Config
SCOPES = ['https://www.googleapis.com/auth/forms', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '/data/.openclaw/workspace/mission-control/google-credentials.json'

def get_service():
    """Get Google Forms service"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('forms', 'v1', credentials=credentials)

def create_lead_with_impact_survey():
    """Create the Lead with Impact survey form"""
    
    service = get_service()
    
    # Create form
    form_body = {
        'info': {
            'title': 'Lead with Impact - Program Feedback Survey',
            'description': 'Thank you for participating in the Lead with Impact program! Your feedback helps us continuously improve the experience for future leaders. This survey takes approximately 5-7 minutes to complete.',
            'documentTitle': 'Lead with Impact Feedback'
        }
    }
    
    form = service.forms().create(body=form_body).execute()
    form_id = form['formId']
    
    print(f"✅ Form created: https://docs.google.com/forms/d/{form_id}/edit")
    print(f"📋 Share link: https://docs.google.com/forms/d/{form_id}/viewform")
    
    # Add questions
    questions = [
        # Section 1: Onboarding Experience
        {
            'title': 'Section 1: Onboarding Experience',
            'description': 'Please rate your experience with the onboarding process (forms, DISC assessment, and coaching call).',
            'type': 'pageBreak'
        },
        {
            'title': 'How satisfied were you with the overall onboarding experience?',
            'type': 'scale',
            'low': 1,
            'high': 5,
            'lowLabel': 'Very Dissatisfied',
            'highLabel': 'Very Satisfied',
            'required': True
        },
        {
            'title': 'The onboarding coaching call helped clarify my goals and expectations for the program.',
            'type': 'scale',
            'low': 1,
            'high': 5,
            'lowLabel': 'Strongly Disagree',
            'highLabel': 'Strongly Agree',
            'required': True
        },
        {
            'title': 'What could we improve about the onboarding process?',
            'type': 'text',
            'required': False
        },
        
        # Section 2: 3-Day Boot Camp
        {
            'title': 'Section 2: 3-Day Leadership Boot Camp',
            'description': 'Please share your feedback on the intensive 3-day boot camp experience.',
            'type': 'pageBreak'
        },
        {
            'title': 'How satisfied were you with the 3-day Leadership Boot Camp?',
            'type': 'scale',
            'low': 1,
            'high': 5,
            'lowLabel': 'Very Dissatisfied',
            'highLabel': 'Very Satisfied',
            'required': True
        },
        {
            'title': 'The instructors were knowledgeable and engaging.',
            'type': 'scale',
            'low': 1,
            'high': 5,
            'lowLabel': 'Strongly Disagree',
            'highLabel': 'Strongly Agree',
            'required': True
        },
        {
            'title': 'The content was relevant to my leadership role and challenges.',
            'type': 'scale',
            'low': 1,
            'high': 5,
            'lowLabel': 'Strongly Disagree',
            'highLabel': 'Strongly Agree',
            'required': True
        },
        {
            'title': 'What was the most valuable takeaway from the boot camp?',
            'type': 'paragraph',
            'required': False
        },
        
        # Section 3: Leadership Labs
        {
            'title': 'Section 3: Leadership Labs (Weekly Sessions)',
            'description': 'Please rate your experience with the ongoing Leadership Labs.',
            'type': 'pageBreak'
        },
        {
            'title': 'The Leadership Labs met my expectations for ongoing development.',
            'type': 'scale',
            'low': 1,
            'high': 5,
            'lowLabel': 'Strongly Disagree',
            'highLabel': 'Strongly Agree',
            'required': True
        },
        {
            'title': 'I have been able to apply what I learned in the Labs to my actual work.',
            'type': 'scale',
            'low': 1,
            'high': 5,
            'lowLabel': 'Strongly Disagree',
            'highLabel': 'Strongly Agree',
            'required': True
        },
        
        # Section 4: Overall Program
        {
            'title': 'Section 4: Overall Program Experience',
            'description': 'Final questions about your complete Lead with Impact journey.',
            'type': 'pageBreak'
        },
        {
            'title': 'How likely are you to recommend Lead with Impact to a colleague or friend?',
            'type': 'scale',
            'low': 0,
            'high': 10,
            'lowLabel': 'Not at all likely (0)',
            'highLabel': 'Extremely likely (10)',
            'required': True
        },
        {
            'title': 'What has been the biggest impact of this program on your leadership?',
            'type': 'paragraph',
            'required': False
        },
        
        # Additional Comments
        {
            'title': 'Additional Comments',
            'description': 'Please share any other feedback, suggestions, or comments you\'d like us to know.',
            'type': 'pageBreak'
        },
        {
            'title': 'Any additional comments or feedback?',
            'type': 'paragraph',
            'required': False
        }
    ]
    
    # Batch add questions
    for q in questions:
        if q.get('type') == 'pageBreak':
            # Add page break
            item = {
                'title': q.get('title', ''),
                'description': q.get('description', ''),
                'pageBreakItem': {}
            }
        elif q.get('type') == 'scale':
            item = {
                'title': q['title'],
                'questionItem': {
                    'question': {
                        'required': q.get('required', False),
                        'scaleQuestion': {
                            'low': q['low'],
                            'high': q['high'],
                            'lowLabel': q.get('lowLabel', ''),
                            'highLabel': q.get('highLabel', '')
                        }
                    }
                }
            }
        elif q.get('type') == 'paragraph':
            item = {
                'title': q['title'],
                'questionItem': {
                    'question': {
                        'required': q.get('required', False),
                        'textQuestion': {
                            'paragraph': True
                        }
                    }
                }
            }
        else:  # text
            item = {
                'title': q['title'],
                'questionItem': {
                    'question': {
                        'required': q.get('required', False),
                        'textQuestion': {
                            'paragraph': False
                        }
                    }
                }
            }
        
        # Add to form
        service.forms().batchUpdate(
            formId=form_id,
            body={'requests': [{'createItem': {'item': item, 'location': {'index': 0}}}]}).execute()
    
    print("\n✅ All questions added!")
    print(f"\n🔗 Share this link with participants:")
    print(f"https://docs.google.com/forms/d/{form_id}/viewform")
    
    return form_id

if __name__ == "__main__":
    try:
        form_id = create_lead_with_impact_survey()
        print(f"\n🎉 Survey created successfully!")
        print(f"Form ID: {form_id}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

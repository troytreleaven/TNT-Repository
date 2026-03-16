#!/bin/bash
# Quick Form Builder Script for Troy
# This creates a Google Form via the Forms API with proper OAuth

echo "📝 Lead with Impact Survey Creator"
echo "=================================="
echo ""
echo "This will create a complete 12-question survey in your Google account."
echo ""
echo "STEP 1: Go to https://script.google.com/home"
echo "STEP 2: Click 'New Project'"
echo "STEP 3: Delete the default code and paste this entire script:"
echo ""
echo "--- COPY EVERYTHING BELOW THIS LINE ---"
echo ""

cat << 'FORM_SCRIPT'
function createLeadWithImpactSurvey() {
  // Create the form
  var form = FormApp.create('Lead with Impact - Program Feedback Survey');
  form.setDescription('Thank you for participating in the Lead with Impact program! Your feedback helps us continuously improve the experience for future leaders. This survey takes approximately 5-7 minutes to complete.');
  form.setConfirmationMessage('Thank you for your feedback! Your insights help us improve the Lead with Impact program for future leaders. If you have any additional thoughts, please don\'t hesitate to reach out to Troy Treleaven at ttreleaven@dalecarnegie.ca or 905-928-1034.');
  form.setCollectEmail(true);
  
  // Section 1: Onboarding
  form.addPageBreakItem()
    .setTitle('Section 1: Onboarding Experience')
    .setHelpText('Please rate your experience with the onboarding process (forms, DISC assessment, and coaching call).');
  
  form.addScaleItem()
    .setTitle('How satisfied were you with the overall onboarding experience?')
    .setBounds(1, 5)
    .setLabels('Very Dissatisfied', 'Very Satisfied')
    .setRequired(true);
  
  form.addScaleItem()
    .setTitle('The onboarding coaching call helped clarify my goals and expectations for the program.')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);
  
  form.addTextItem()
    .setTitle('What could we improve about the onboarding process?')
    .setRequired(false);
  
  // Section 2: Boot Camp
  form.addPageBreakItem()
    .setTitle('Section 2: 3-Day Leadership Boot Camp')
    .setHelpText('Please share your feedback on the intensive 3-day boot camp experience.');
  
  form.addScaleItem()
    .setTitle('How satisfied were you with the 3-day Leadership Boot Camp?')
    .setBounds(1, 5)
    .setLabels('Very Dissatisfied', 'Very Satisfied')
    .setRequired(true);
  
  form.addScaleItem()
    .setTitle('The instructors were knowledgeable and engaging.')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);
  
  form.addScaleItem()
    .setTitle('The content was relevant to my leadership role and challenges.')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);
  
  form.addParagraphTextItem()
    .setTitle('What was the most valuable takeaway from the boot camp?')
    .setRequired(false);
  
  // Section 3: Leadership Labs
  form.addPageBreakItem()
    .setTitle('Section 3: Leadership Labs (Weekly Sessions)')
    .setHelpText('Please rate your experience with the ongoing Leadership Labs.');
  
  form.addScaleItem()
    .setTitle('The Leadership Labs met my expectations for ongoing development.')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);
  
  form.addScaleItem()
    .setTitle('I have been able to apply what I learned in the Labs to my actual work.')
    .setBounds(1, 5)
    .setLabels('Strongly Disagree', 'Strongly Agree')
    .setRequired(true);
  
  // Section 4: Overall
  form.addPageBreakItem()
    .setTitle('Section 4: Overall Program Experience')
    .setHelpText('Final questions about your complete Lead with Impact journey.');
  
  form.addScaleItem()
    .setTitle('How likely are you to recommend Lead with Impact to a colleague or friend?')
    .setBounds(0, 10)
    .setLabels('Not at all likely (0)', 'Extremely likely (10)')
    .setRequired(true);
  
  form.addParagraphTextItem()
    .setTitle('What has been the biggest impact of this program on your leadership?')
    .setRequired(false);
  
  // Section 5: Additional Comments
  form.addPageBreakItem()
    .setTitle('Section 5: Additional Comments')
    .setHelpText('Please share any other feedback, suggestions, or comments you\'d like us to know.');
  
  form.addParagraphTextItem()
    .setTitle('Any additional comments or feedback?')
    .setRequired(false);
  
  // Get and log the form URL
  var formUrl = form.getPublishedUrl();
  var editUrl = form.getEditUrl();
  
  Logger.log('Form created successfully!');
  Logger.log('Share URL: ' + formUrl);
  Logger.log('Edit URL: ' + editUrl);
  
  // Show URLs in a dialog
  var ui = FormApp.getUi();
  ui.alert('Form Created!', 
    'Share URL:\n' + formUrl + '\n\nEdit URL:\n' + editUrl, 
    ui.ButtonSet.OK);
  
  return formUrl;
}

// Run this function to create the form
function run() {
  createLeadWithImpactSurvey();
}
FORM_SCRIPT

echo ""
echo "--- COPY EVERYTHING ABOVE THIS LINE ---"
echo ""
echo "STEP 4: Click the 'Save' icon (💾)"
echo "STEP 5: Click 'Run' (▶️) next to the 'run' function"
echo "STEP 6: Click 'Review Permissions' → Choose your Google account → Click 'Allow'"
echo "STEP 7: The form URLs will appear in the logs at the bottom"
echo ""
echo "✅ That's it! Your survey will be created with all 12 questions."

echo "# Employee Data Generator

This is the code that creates the fake data and loads to bucket in GCP.

## Features
- Generates fake employee data including:
  - Personal information
  - Job details
  - Salary information
  - Contact details
- Automatically saves to CSV file
- Uploads to GCP bucket

## How to Run
1. Install requirements:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Run the script:
   \`\`\`bash
   python Extract.py
   \`\`\`" > README.md

# Add and commit the README
git add README.md
git commit -m "Add simple README"
git push origin main

import csv
import random
from datetime import datetime, timedelta

# Sample data pools
first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Robert', 'Lisa',
               'William', 'Jennifer', 'James', 'Mary', 'Christopher', 'Patricia', 'Daniel',
               'Linda', 'Matthew', 'Barbara', 'Anthony', 'Susan', 'Mark', 'Jessica', 'Donald',
               'Karen', 'Steven', 'Nancy', 'Paul', 'Betty', 'Andrew', 'Helen', 'Joshua', 'Sandra',
               'Kenneth', 'Dorothy', 'Kevin', 'Ashley', 'Brian', 'Kimberly', 'George', 'Emily',
               'Timothy', 'Donna', 'Ronald', 'Michelle', 'Edward', 'Carol', 'Jason', 'Amanda',
               'Jeffrey', 'Melissa', 'Ryan', 'Deborah', 'Jacob', 'Stephanie', 'Gary', 'Rebecca',
               'Nicholas', 'Sharon', 'Eric', 'Laura', 'Jonathan', 'Cynthia', 'Stephen', 'Kathleen']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
              'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
              'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
              'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
              'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
              'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker']

departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations',
               'Customer Support', 'Product', 'Legal', 'IT']

locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
             'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Seattle',
             'Denver', 'Boston', 'Portland', 'Atlanta', 'Miami', 'Detroit']

job_levels = ['Junior', 'Mid-Level', 'Senior', 'Lead', 'Manager', 'Director']

satisfaction_levels = ['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Dissatisfied']

work_life_balance = ['Excellent', 'Good', 'Fair', 'Poor']

benefits_rating = ['Excellent', 'Good', 'Average', 'Below Average', 'Poor']

would_recommend = ['Definitely', 'Probably', 'Not Sure', 'Probably Not', 'Definitely Not']

tenure_years = ['< 1 year', '1-2 years', '2-5 years', '5-10 years', '10+ years']

remote_preference = ['Fully Remote', 'Hybrid (3 days office)', 'Hybrid (2 days office)',
                     'Mostly Office', 'Fully Office']

feedback_topics = [
    'Great team collaboration and culture',
    'Good work-life balance',
    'Competitive salary and benefits',
    'Interesting and challenging projects',
    'Strong leadership and clear direction',
    'Flexible working hours',
    'Professional development opportunities',
    'Modern tools and technology',
    'Inclusive and diverse workplace',
    'Clear career progression path',
    'Could improve communication between teams',
    'Would like more training opportunities',
    'Office space needs improvement',
    'Benefits package could be better',
    'More transparency from leadership needed',
    'Workload can be overwhelming at times',
    'Salary not competitive with market',
    'Limited remote work options',
    'Need better work equipment',
    'Unclear performance evaluation process'
]

# Generate data
data = []
start_date = datetime(2024, 1, 1)

for i in range(1, 1001):
    # Generate employee info
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    age = random.randint(22, 65)
    department = random.choice(departments)
    location = random.choice(locations)
    job_level = random.choice(job_levels)
    tenure = random.choice(tenure_years)

    # Generate ratings (with some correlation)
    # Higher job levels tend to be more satisfied
    satisfaction_weights = [0.35, 0.30, 0.20, 0.10, 0.05] if job_level in ['Manager', 'Director', 'Lead'] else [0.15, 0.25, 0.30, 0.20, 0.10]
    satisfaction = random.choices(satisfaction_levels, weights=satisfaction_weights)[0]

    # Work-life balance
    wlb_weights = [0.25, 0.40, 0.25, 0.10] if department not in ['Sales', 'Operations'] else [0.10, 0.30, 0.40, 0.20]
    work_life = random.choices(work_life_balance, weights=wlb_weights)[0]

    # Benefits
    benefits = random.choice(benefits_rating)

    # Would recommend (correlated with satisfaction)
    if satisfaction in ['Very Satisfied', 'Satisfied']:
        recommend = random.choices(would_recommend, weights=[0.40, 0.35, 0.15, 0.07, 0.03])[0]
    elif satisfaction == 'Neutral':
        recommend = random.choices(would_recommend, weights=[0.10, 0.25, 0.40, 0.15, 0.10])[0]
    else:
        recommend = random.choices(would_recommend, weights=[0.05, 0.10, 0.20, 0.35, 0.30])[0]

    # Remote preference
    remote = random.choice(remote_preference)

    # Survey date (spread over Q1 2024)
    survey_date = start_date + timedelta(days=random.randint(0, 89))

    # Feedback (correlated with satisfaction)
    if satisfaction in ['Very Satisfied', 'Satisfied']:
        feedback = random.choice(feedback_topics[:10])  # Positive feedback
    else:
        feedback = random.choice(feedback_topics[10:])  # Constructive feedback

    # Employee ID
    emp_id = f"EMP{i:04d}"

    row = {
        'Employee_ID': emp_id,
        'Name': name,
        'Age': age,
        'Department': department,
        'Location': location,
        'Job_Level': job_level,
        'Tenure': tenure,
        'Overall_Satisfaction': satisfaction,
        'Work_Life_Balance': work_life,
        'Benefits_Rating': benefits,
        'Would_Recommend': recommend,
        'Remote_Preference': remote,
        'Survey_Date': survey_date.strftime('%Y-%m-%d'),
        'Feedback': feedback
    }

    data.append(row)

# Write to CSV
with open('large_sample_survey.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['Employee_ID', 'Name', 'Age', 'Department', 'Location', 'Job_Level',
                  'Tenure', 'Overall_Satisfaction', 'Work_Life_Balance', 'Benefits_Rating',
                  'Would_Recommend', 'Remote_Preference', 'Survey_Date', 'Feedback']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)

print("✅ Generated large_sample_survey.csv with 1000 employee survey responses!")
print("\nDataset includes:")
print(f"  - 1000 employees")
print(f"  - {len(departments)} departments")
print(f"  - {len(locations)} locations")
print(f"  - {len(job_levels)} job levels")
print(f"  - Multiple satisfaction and rating categories")
print(f"  - Survey dates spread across Q1 2024")
print("\nPerfect for testing:")
print("  ✓ Filtering performance")
print("  ✓ Chart generation")
print("  ✓ Comparison mode")
print("  ✓ Data export")
print("  ✓ Search functionality")

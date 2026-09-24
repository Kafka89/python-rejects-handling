# python-rejects-handling
Python project done to automatically handle lines in file rejected due to data issue (incorrect/missing value). The aim was to eliminate manual corrections. 

1. Problem: 20+ reports are generated monthly and, after they pass the validation stage, logs are created too. Logs list data quality issues per the deal number like incorrect product code, etc. Those reports need to be manually amended and reuploaded to the data warehouse. Reports are provided as TXT files using fixed-width, position-based format. Large and difficult to work with manually. 
2. Solution: Build template where users will put instructions regarding each account (eg. "delete", "change") and python script to read the template and act accordingly.

Problem compelxity is low but volume and task frequency is significant. Manual handling triggers futher issues, eg. corrupts fields positions. 


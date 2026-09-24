import pandas as pd, os
import time #, warnings
import csv

s = time.time()
#warnings.filterwarnings('error') / disabled

print("Collecting change event data....")
inputfile = 'reject_template_draft.xlsx'
df = pd.read_excel(inputfile, sheet_name=0)
cols = [0,1,3,4]
df = df.drop(df.columns[cols], axis=1)
result = df.melt(id_vars=['Deal id'], var_name="Parameter", value_name="Target").dropna()
result['Deal id'] = result['Deal id'].astype(str).str[:10].apply(lambda x: '0'+x.strip() if len(x.strip()) == 9 else x.strip())
# removing duplicated entries
result = result.drop_duplicates()
# deal id + change type as unique value
result['Deal id'] = result['Deal id']+";"+result['Parameter']
cols= [1]
result = result.drop(result.columns[cols], axis=1)


#Validation - start
try:
    changes = result.set_index('Deal id').T.to_dict('list')
except UserWarning:
    print("Check if values provided for deal_id(s) are unique")
    os.system("pause")
    exit()

#separate deal id from change type for validation
id_num = result['Deal id'].str.split(';', n=1, expand=True)
id_list=id_num[0].values.tolist()
rejectfile = 'Report.txt'
with open(rejectfile, 'r') a
s r:
    reader = csv.reader(r)
    keyacc = []
    for line in reader:
        format = line[0][0:5]
        deal_id = line[0][20:30]
        keyacc.append(deal_id)

print("Validating Deal IDs...")
check = all(item in keyacc for item in id_list)
if check is True:
    pass
if check is False:
    print(f'There are Deal IDs in template that are missing in the report file. Check and re-run.')
    os.system("pause")
    exit()

#Validation - end

#Report is a flat file and fields are position based (no delimiter).
#Staging - product change first, then nature change

clearedfile_stg = 'Report_cleared.txt'
clearedfile = 'Cleared.txt'

print("Applying changes to Report file...")
#Product
with open(rejectfile, 'r') as r, open(clearedfile_stg, 'w+') as wr:
    accounts = changes.keys()
    r.seek(0)
    reader = csv.reader(r)
    for key in accounts:
        acc, param = key.split(';')
        for line in reader:
            lkp = line[0][20:30]
            format = line[0][1:5]
            if acc == lkp:
                if str(changes[key]) == "['deletethecre']":
                    pass
                elif param == "SUPPRODUIT":
                    if format in("MBTP","METP","MRHB","OPGE","MRBI","MIHB","ORHB","PEIE","PESB","PEHB","OCRP"):
                        wr.write(line[0][0:373] + ('00' + str(changes[key])[1:-1])[-2:] + line[0][375:4002] + "\n")
                    if format in ["MRET","PEEB"]:
                        wr.write(line[0][0:1082] + ('00' + str(changes[key])[1:-1])[-2:] + line[0][1084:4002] + "\n")
        r.seek(0)
#Nature
with open(clearedfile_stg, 'r') as r, open(clearedfile, 'w') as w:
    accounts = changes.keys()
    r.seek(0)
    reader = csv.reader(r)
    for key in accounts:
        acc, param = key.split(';')
        for line in reader:
            lkp = line[0][20:30]
            format = line[0][1:5]
            if acc == lkp:
                if param == "NATURTITRE":
                    if format in ("MBTP", "METP", "MRHB", "OPGE", "MRBI", "MIHB", "ORHB", "PEIE", "PESB", "PEHB", "OCRP", "PEEB"):
                        w.write(line[0][0:986] + ('00' + str(changes[key])[2:-2])[-2:] + line[0][988:4002] + "\n")
                    else:
                        w.write(line[0] + "\n")

        r.seek(0)

os.remove(clearedfile_stg)
e=time.time()
print(f"Finished after {e-s} seconds")
os.system("pause")


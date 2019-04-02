import re
import os
from tqdm import tqdm

procress_LCSTS_file_path = 'PART_III.txt'

dir_list = ['short_text','summary']
human_score_list = [1,2,3,4,5]

for dir_name in dir_list :
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

for dir_name in dir_list : 
    for human_score in human_score_list :
        path = os.path.join(dir_name, str(human_score))
        if not os.path.exists(path):
            os.makedirs(path)

with tqdm() as pbar:
    with open(procress_LCSTS_file_path, 'r') as procress_LCSTS_file :
        now_process_doc_num = ''
        human_score = ''
        summary_text = ''
        short_text = ''
        summary_in_next = False
        short_text_in_next = False
        for line in procress_LCSTS_file.readlines():
            if summary_in_next :
                summary_text = line.strip()  
                summary_in_next = False          
            if short_text_in_next :
                short_text = line.strip()
                short_text_in_next = False
            if '<doc' in line :
                now_process_doc_num = re.findall("\d+",line)[0]                
            elif '<human_label>' in line:                
                human_score = re.findall("\d+",line)[0]
            elif '<summary>' in line:    
                summary_in_next = True
            elif '<short_text>' in line:    
                short_text_in_next = True   
            elif  '</doc>' in line :
                with open(os.path.join('summary' , human_score, str(now_process_doc_num)+'.summary'),'w') as wsummaryf:
                    wsummaryf.write(summary_text.replace('。','。\n'))
                with open(os.path.join('short_text' , human_score, str(now_process_doc_num)+'.short_text'),'w') as wshort_textf:
                    wshort_textf.write(short_text.replace('。','。\n'))
                now_process_doc_num = -1
                human_score = -1
                summary_text = ''
                short_text = ''
                summary_in_next = False
                short_text_in_next = False                 
                pbar.update()


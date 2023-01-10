# import sys
from datetime import datetime as dt, timedelta as delt


def func():
    lst = []
    study_count = []
    output_f = open("Total_Study_Record.txt", "w")
    with open("Study_Time.txt", "r") as f:
        for line in f:
            lst.append(line.strip())
            if line[:2].isdigit():
                study_count.append(line.split("(")[0].strip())

        for i in range(len(lst)):
            for j in range(i+1, len(lst)):
                if lst[i][:16] == lst[j][:16]:
                    if lst[i][:2].isdigit():
                        for plus in range(1, 3):
                            h1, m1, s1 = list(
                                map(int, lst[i+plus][12:].split(":")))
                            h2, m2, s2 = list(
                                map(int, lst[j+plus][12:].split(":")))

                            total_time = (
                                dt(1, 1, 1, 0, 0, 0)+delt(hours=h1+h2, minutes=m1+m2, seconds=s1+s2)).time()
                            lst[i+plus] = f'{"Study Time" if plus==1 else "Other Time"}: {total_time}'
                            lst[j] = ""
                            lst[j+plus] = ""

        lst = [i for i in lst if i]

        for index, text in enumerate(lst):
            text += ("\n" if ((text[0] == "O")
                     and (index != len(lst))) else "")
            if len(text) > 17 and text[:2].isdigit():
                text = text[:-30]+":-"
                print(text, file=output_f)
                print(
                    f'Studied in {study_count.count(text[:-2])} {"sitting" if study_count.count(text[:-2])==1 else "sittings"}!', file=output_f)
            else:
                print(text, file=output_f)

    output_f.close()

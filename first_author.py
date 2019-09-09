import re
import csv


def make_name_list():
    with open("chinese-family-name.txt", encoding="utf-8") as f:
        word_list = []
        for line in f.readlines():
            c = line.split()[1]
            word_list.append(c)
    name_list = list(set(word_list))
    return name_list


def judge(faml_name, name_list):
    if faml_name.lower() in name_list:
        return True
    else:
        return False


def get_first_au(line):
    faml_name = line.split()[1]
    fst_name = line.split()[2][:-1]

    return faml_name, fst_name


def get_second_au(line):
    if not line.split()[2][-2:-1] == ".":
        faml_name = line.split()[3]
        fst_name = line.split()[4][:-1]

    return faml_name, fst_name


def get_journal(line):
    if "Nature." in line:
        journal = "Nature"
    elif "Cell." in line:
        journal = "Cell"
    else:
        journal = "Science"

    return journal


def get_pmid(line):
    c = line.split()
    pmid = c[-1][:-1]

    return pmid


def main():
    name_list = make_name_list()
    csvfile = open("first_author.csv", "w", newline="", encoding="utf-8")
    writer = csv.writer(csvfile)
    writer.writerow(['pmid', 'journal', 'name'])

    with open("pubmed_result.txt", encoding="utf-8") as f:
        next(f)
        i = 0
        for block in f.read().split("\n\n\n"):
            line1 = block.split("\n")[0]
            faml_name, fstname = get_first_au(line1)
            if judge(faml_name, name_list) and re.match("[A-Z]{1,2}$",
                                                        fstname):
                journal = get_journal(block)
                line_1 = block.split("\n")[-1]
                pmid = get_pmid(line_1)
                i += 1
                name = faml_name+" "+fstname
                list_to_write = [pmid, journal, name]
                writer.writerow(list_to_write)
                print(pmid+" "+journal+" "+name+"\n")
            else:
                continue
    csvfile.close()
    print(i)


if __name__ == "__main__":
    main()

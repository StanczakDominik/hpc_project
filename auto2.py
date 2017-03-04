import subprocess
import os
import re

# dokąd zapisujemy plik konfiguracyjny
proof_file_location = "/common/opt/etc/proof/proof.conf"

# gdzie wyrzucamy pliki
output_file_directory = "/common/automate_results/"

# budowa stringu konfiguracyjnego
result_string = "master pcmaster01.pcluster.hpclab\n" # to musi być zawsze na początku - taki admin
# workery na poszczególnych nodach
masterworker = "worker pcmaster01.pcluster.hpclab\n"
n1worker = "worker pcnode01.pcluster.hpclab\n"
n2worker = "worker pcnode02.pcluster.hpclab\n"
n3worker = "worker pcnode03.pcluster.hpclab\n"

def conf_str(wm, w):
    """funkcja zwracająca tekst stringa konfiguracyjnego
    np. z argumentami 1, 1, 2:
    master pcmaster01

    worker pcmaster01

    worker pcnode01

    worker pcnode02
    worker pcnode02"""
    # TODO: przerobić pod pcnode03 (w1=w2=w3)
    return result_string + wm * masterworker + w * n1worker + w * n2worker + w * n3worker

# ile maksymalnie może być workerów na każdym node
max_workers_master = 3 # bo jeden jest zajęty przez admina
max_workers_node = 4 # wszystkie 4 rdzenie

for i in range(max_workers_master, -1, -1): # [3 2 1 0]
    for j in range(max_workers_node, -1, -1): # [ 4 3 2 1 0]
        l = j
        k = j
        total_workers = i + j + k + l # suma
        if total_workers > 5: # warunek zabezpieczający przed bardzo długimi runami, można zastąpić if True jeśli jesteśmy odważni
            index = str(i)+str(j)+str(k)+str(l) # string np. 014, działa dobrze dopóki pracujemy na prockach <10rdzeniowych
            output_file_path = output_file_directory + index # pełna nazwa pliku np. /common/automate_results/014
            if os.path.isfile(output_file_path): # jeśli ten plik już tam jest
                print(index + " exists, skipping") # olewamy
            else:
                print("running for " + index)
                with open(proof_file_location, "w") as proof_file: # zapisuję treść conf file do pliku
                    proof_file.write(conf_str(i,j))

                # francuzi na to mówią piece de resistance, znaczy że to wykonuje główną robotę w kodzie
                # 1. odpalam basha z dostępem do zmiennych środowiskowych (-i)
                # 2. odpalam roota
                # 3. check_output zrzuca treść bashowego outputu do stringa
                # 4. [-100:] wycina ostatnie 100 znaków (chyba znaków, nie linijek) bitowych
                var = subprocess.check_output(["/bin/bash", '-i', '-c', "root -q -b runProofCluster.C", "exit"])[-100:]
                print(var)
                print("finished run")
                result_output = var.decode("utf-8") # 5. konwersja na utf-8 do stringa
                result_variable = re.findall('HEREISRESULT(.*?)HEREENDRESULT', result_output, re.DOTALL)[0]
                #6. ^ regexem wyciągam zmienną ze stringa którego printuję w kodzie

                print(result_variable)
                with open(output_file_path, "w") as output_file:
                    # zapisuję do pliku 014 w /common/automate_results jako 0,1,4,liczbowy_runtime
                    output_file.write(",".join([str(i),str(j),str(k),str(l),result_variable]))
print("Execution finished!")

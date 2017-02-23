import subprocess
import os
import re

proof_file_location = "/common/opt/etc/proof/proof.conf"
# proof_file_location = "/home/dominik/hpc/test.conf"

output_file_directory = "/common/automate_results/"

result_string = "master pcmaster01.pcluster.hpclab\n"
masterworker = "worker pcmaster01.pcluster.hpclab\n"
n1worker = "worker pcnode01.pcluster.hpclab\n"
n2worker = "worker pcnode02.pcluster.hpclab\n"

def conf_str(wm, w1, w2):
  return result_string + wm * masterworker + w1 * n1worker + w2 * n2worker

max_workers_master = 3
max_workers_node = 4
conf_strings = {}
# for i in range(3, max_workers_master+1):
#     for j in range(4,max_workers_node+1):
#         for k in range(4,max_workers_node+1):

for i in range(0, max_workers_master+1):
    for j in range(0,max_workers_node+1):
        for k in range(0,max_workers_node+1):
            i = max_workers_master - i
            j = max_workers_node - j
            k = max_workers_node - k
            total_workers = i + j + k
            if total_workers > 5:
                index = str(i)+str(j)+str(k)

                var1, var2, var3 = index
                output_file_path = output_file_directory + index
                if os.path.isfile(output_file_path):
                    print(index + " exists, skipping")
                else:
                    print("running for " + index)
                    with open(proof_file_location, "w") as proof_file:
                        proof_file.write(conf_str(i,j,k))

                    var = subprocess.check_output(["/bin/bash", '-i', '-c', "root -q -b runProofCluster.C", "exit"])[-100:]
                    print(var)
                    print("finished run")
                    result_output = var.decode("utf-8")
                    # print(result_output)
                    result_variable = re.findall ( 'HEREISRESULT(.*?)HEREENDRESULT', result_output, re.DOTALL)[0]
                    print(result_variable)
                    with open(output_file_path, "w") as output_file:
                        output_file.write(var1+","+var2+","+var3+","+result_variable)
print("Execution finished!")

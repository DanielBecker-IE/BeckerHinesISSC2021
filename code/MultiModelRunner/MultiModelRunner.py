# -*- coding: utf-8 -*-
import jinja2
import pandas
import subprocess as sp
import matplotlib.pyplot as plt
import datetime
import hashlib


def generate(template, output, **kwargs):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template))
    output_from_parsed_template = env.get_template('').render(kwargs)
    with open(output, "wb") as f:
        try:
            f.write(output_from_parsed_template.encode('utf8'))
        except Exception as exc:
            print(exc)
            print(output_from_parsed_template)


def genPopulation(a,b):
    return "+".join(["'{0}'".format(i) for i in ("1" * a + "0"*b)])

#return Count and Count of Not
def genCounter(a):
    return "+".join(['ZERO ']+["'{0}'".format(i) for i in ("X" * a)]) #We need a ZERO, it's a bit wierd not to have an empty multiset

# BEGIN
models = []
results = pandas.DataFrame()
for counter in range(0, 11):
    AuxDataset: str = genPopulation(counter, 10-counter)
    AuxDataset1Counter: str = genCounter(counter)
    AuxDataset0Counter: str = genCounter(10-counter)

    filename = 'generated/AttackingDET_{0}_{1}.spthy'.format(counter,10-counter)
    generate('AttackingDET.spthy.jinja2',
             filename,
             NAME='AttackingDet_{0}_{1}'.format(counter, 10-counter),
             AuxDataset=AuxDataset, AuxDataset1Counter=AuxDataset1Counter, AuxDataset0Counter=AuxDataset0Counter)
    models.append(filename)
# counter=0

#for filename in models:
    print(filename)
    command="tamarin-prover --parse-only {0}".format(filename)
    child = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
    stdout, stderr = child.communicate()
    rc = child.returncode
    result = -1
    if rc != 0 :
        print(stdout)
        print(stderr)
        print("Parse failed")

    else:
        print("Parse OK. Attempting proof...")
        command = "tamarin-prover --prove {0}".format(filename)
        child = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
        stdout, stderr = child.communicate()
        rc = child.returncode
        temp = None
        if rc != 0:
            print(stdout)
            print(stderr)
            print("Proof attempt failed for: {0}".format(filename))
        else:
            print("")
            if 'falsified - no trace found' in stdout.decode("utf-8") :
                result = 0
            else:
                result = 1

    temp = pandas.DataFrame.from_records(
        { 'Filename': filename,
         'MD5': hashlib.md5(open(filename, "r").read().encode('utf-8')).hexdigest(),
         'Index': counter,
         'Percent': "{0}/{1}".format(counter * 10, (10 - counter) * 10),
         'Result': result},
        index=[counter])
    results = pandas.concat([results, temp])
    counter += 1
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
print(results)

plt.plot('Percent', 'Result', data=results, marker='x')
plt.show()

print("Done @{0}".format(datetime.datetime.now()))




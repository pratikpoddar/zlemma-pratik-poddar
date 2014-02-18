import json
import urllib2

# Edit at location: https://docs.google.com/a/zlemma.com/spreadsheet/ccc?key=0Ang7Vqp7FIPSdHV6d0gwSkcxTjZfc2xBU3F3YjlZT0E#gid=0

d = json.load(urllib2.urlopen('https://spreadsheets.google.com/feeds/list/0Ang7Vqp7FIPSdHV6d0gwSkcxTjZfc2xBU3F3YjlZT0E/od6/public/basic?hl=en_US&alt=json'))
output = {}

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

execfile("skill_list.py")
skills = map(lambda x: slugify(x), skill_list)

for entry in d['feed']['entry']:
	try:
		num = entry['content']['$t'].split(',')[1].replace('num: ','').strip()
		skill2 = entry['content']['$t'].split(',')[0].replace('skill2: ','').strip()
		skill1 = entry['title']['$t'].strip()

		if skill1 not in skills:
			print skill1 + " is not a skill"
			raise
		if skill2 not in skills:
			print skill2 + " is not a skill"
			raise
		try:
			output[skill1][skill2] = num
		except:
			output[skill1] = {}
			output[skill1][skill2] = num
	except Exception as e:
		print "Not able to read " + str(e) + " " + str(entry)

print "Final Manual Input Dict: "
print output
with open('manualinput.txt', 'w') as infile:
                infile.write(json.dumps(output))


# Edit at location: https://docs.google.com/a/zlemma.com/spreadsheet/ccc?key=0Ang7Vqp7FIPSdG1QWjBwLTNJUTZzbktWVXNocGtSb3c#gid=0

d = json.load(urllib2.urlopen('https://spreadsheets.google.com/feeds/list/0Ang7Vqp7FIPSdG1QWjBwLTNJUTZzbktWVXNocGtSb3c/od6/public/basic?hl=en_US&alt=json'))
output = {}

for entry in d['feed']['entry']:
        try:
                num = entry['content']['$t'].split(',')[1].replace('num: ','').strip()
                skill2 = entry['content']['$t'].split(',')[0].replace('skill2: ','').strip()
                skill1 = entry['title']['$t'].strip()

                try:
                        output[skill1][skill2] = num
                except:
                        output[skill1] = {}
                        output[skill1][skill2] = num
        except Exception as e:
                print "Not able to read " + str(e) + " " + str(entry)

print "Final Manual Forced Input Dict: "
print output
with open('manualforcedinput.txt', 'w') as infile:
                infile.write(json.dumps(output))

# Edit at location https://docs.google.com/a/zlemma.com/spreadsheet/ccc?key=0AjPfOfZ0QaixdGEzZ2djdHJRVFgtR3pZejhVQlZnSEE#gid=0

d = json.load(urllib2.urlopen('https://spreadsheets.google.com/feeds/list/0AjPfOfZ0QaixdGEzZ2djdHJRVFgtR3pZejhVQlZnSEE/od6/public/basic?hl=en_US&alt=json'))
output = {}

for entry in d['feed']['entry']:
	try:
                s = entry['content']['$t']
                a = map(lambda x: x.strip().split(':')[1].strip(), s.split(','))
                output[entry['title']['$t']] = [tuple(a[i:i+2]) for i in range(0, len(a), 2)]
	except:
		pass
print "Department Mapping of Skills: "
print output
with open('manualdepartmentmapping.txt', 'w') as infile:
                infile.write(json.dumps(output))



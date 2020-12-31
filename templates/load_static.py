import re

html_file = open('account/register.html')
data = html_file.read()
lines = html_file.readlines()
html_file.close()

newdata = data
matches = re.findall(r'src="assets/(.+?)"', data)
for match in matches:
    new = "{{% static '{match}' %}}".format(match=match)
    newdata = newdata.replace('assets/'+match, new)


matches = re.findall(r'href="assets/(.+?)"', newdata)
for match in matches:
    new = "{{% static '{match}' %}}".format(match=match)
    newdata = newdata.replace('assets/'+match, new)


with open('account/register.html', 'w') as file:
    file.write(newdata)

import glob

from urlextract import URLExtract

file_names = glob.glob("log/*.txt")
file_list = []

for f in file_names:
    file_list.append(f)

file_list.sort()

extractor = URLExtract()

for i, file_name in enumerate(file_list):

    f1 = open(file_name, mode='r', encoding='cp932')
    f2 = open(file_name.replace('txt', 'html'), mode='w', encoding='UTF-8')

    title = file_name[-12:-8] + '年' + \
        file_name[-8:-6] + '月' + file_name[-6:-4] + '日のログ'
    header = '<html><head><title>' + title + '</title></head>\n'
    body = '<body color=\"#f0f0f0\">\n'
    log = '<b>' + title + '</b><br /><br />\n'
    f2.write(header + body + log)

    for input_line in f1:

        if input_line == '\n':
            continue
        urls = extractor.find_urls(input_line)

        time_string = '<span style="color:#0000ff;">' + \
            input_line[0:5] + '</span> '
        body_string = input_line[6:].rstrip('\r\n')
        body_string = body_string.replace('<', '&lt;').replace('>', '&gt;')

        if 'joined' in body_string:
            body_string = '<span style="color:#ff0000;">' + body_string + '</span>'
        if 'New Mode' in body_string:
            body_string = '<span style="color:#7777ff;">' + body_string + '</span>'
        if 'New topic' in body_string:
            body_string = '<span style="color:#7777ff;">' + body_string + '</span>'
        if 'Topic for' in body_string:
            body_string = '<span style="color:#7777ff;">' + body_string + '</span>'
        if 'has left' in body_string:
            body_string = '<span style="color:#227722;">' + body_string + '</span>'
        if 'now known' in body_string:
            body_string = '<span style="color:#ff7722;">' + body_string + '</span>'

        for u in urls:
            body_string = body_string.replace(
                u, '<a href=\'' + u + '\' target=_blank>' + u + '</a>')

        body_string = body_string + '<br />\n'

        f2.write(time_string + body_string)

    if i + 1 != len(file_list):
        next_name = file_list[i + 1][-12:].replace('txt', 'html')
        title_next = next_name[0:4] + '年' + \
            next_name[4:6] + '月' + next_name[6:8] + '日のログ'
        next_link = '<br />\n<a href=\'' + next_name + \
            '\'>' + title_next + '</a><br />\n'
        f2.write(next_link)

    footer = '</body></html>'
    f2.write(footer)

    f1.close()
    f2.close()

    print(file_name + ' done.')

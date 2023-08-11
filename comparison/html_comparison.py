import difflib

def compare_html_files(file1_path, file2_path):
    with open(file1_path, 'r', encoding='utf-8') as file1:
        content1 = file1.readlines()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        content2 = file2.readlines()

    differ = difflib.HtmlDiff()
    comparison_html = differ.make_file(content1, content2)

    with open('comparison.html', 'w', encoding='utf-8') as comparison_file:
        comparison_file.write(comparison_html)

file1_path = 'youtube_desktop_bot.html'
file2_path = 'youtube_desktop_user.html'

compare_html_files(file1_path, file2_path)
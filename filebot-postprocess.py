# Run Program: 
# "C:\path\to\python.exe" "C:\path\to\filebot-postprocess.py" "%L" "" "%N" "multi" "" "%F"
#
# Test with Console:
# "C:\path\to\python.exe" "C:\path\to\filebot-postprocess.py" "Movie" "5" "Avatar" "multi" "" "X:\Files\Avatar"


import sys
import subprocess
import requests


# required args
label, state, title, kind, file, directory = sys.argv[1:7]


command = [
	'filebot', '-script', 'fn:amc',
	'--output', 'E:/Media',
	'--log-file', 'E:/Media/amc.log',
	'--action', 'move',
	'--conflict', 'auto',
	'-non-strict',
	'--def',
		'movieFormat={plex}',
		'''seriesFormat="TV Shows/{n}/Season {s.pad(2)}/{n} - {s00e00} - {t}{'.'+lang}"''',
		'''animeFormat="Anime/{n}/Season {s.pad(2)}/{n} - {s00e00} - {t}{'.'+lang}"''',
		'clean=y',
		'unsorted=y',
		'music=y',
		'artwork=y',
		'ut_label=' + label,
		'ut_state=' + state,
		'ut_title=' + title,
		'ut_kind='  + kind,
		'ut_file='  + file,
		'ut_dir='   + directory
]

# execute command only for certain conditions (disabled by default)
'''
if state not in ['5', '11']:
	print('Illegal state: %s' % state)
	sys.exit(0)
'''


# execute command (and hide cmd window)
process = subprocess.Popen(command, stdout=subprocess.PIPE)
try:
	for c in iter(lambda: process.stdout.read(1), ''):
		sys.stdout.write(c)
except:
    process.kill()
    process.wait()
    raise
retcode = process.poll()
if retcode:
    raise subprocess.CalledProcessError(retcode, process.args, output=stdout, stderr=stderr)

print("Refreshing Plex Library")
res = requests.get("http://127.0.0.1:32400/library/sections/all/refresh?X-Plex-Token=XJsCG5MK65gv7GHypuew")
res.raise_for_status()

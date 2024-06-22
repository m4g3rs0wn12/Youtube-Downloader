import PyInstaller.__main__


PyInstaller.__main__.run([
	'yt_downloader.py',
        '--onedir',
        '--onefile',
        '--windowed',
        '-n' 'YouTube 720p Downloader',
        '-i' 'icon.ico'
    ])

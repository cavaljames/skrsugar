set folderPath to "EDY:Users:sugar:PycharmProjects:skrsugar:screenshot:"
tell application "Finder"
	activate
	open alias folderPath
	delay 0.5
	tell application "System Events"
		keystroke "a" using {command down}
	end tell
end tell

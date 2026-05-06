tell application "Contacts"
	repeat
		set myGroup to text returned of (display dialog "What group name do you want to remove from the Note field?" default answer "")
		if myGroup is "" then
			display alert "Please enter your answer to continue."
		else
			exit repeat
		end if
	end repeat
	repeat with aperson in people of group myGroup
		if myGroup is equal to note of aperson then
			set the note of aperson to missing value
		else
			if myGroup is in note of aperson then
				set mytext to note of aperson as text
				set the note of aperson to my trimParagraphs(mytext)
			end if
		end if
	end repeat
	save
end tell

on trimParagraphs(theText)
	set theParagraphs to paragraphs 1 thru ((count of the paragraph of theText) - 2) of theText
	set AppleScript's text item delimiters to return
	set theText to theParagraphs as string
	set AppleScript's text item delimiters to ""
	return theText
end trimParagraphs


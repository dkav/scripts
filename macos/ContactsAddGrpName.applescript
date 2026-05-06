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
		if note of aperson is missing value then
			set the note of aperson to myGroup
		else
			set the note of aperson to note of aperson & return & return & myGroup
		end if
	end repeat
	save
end tell

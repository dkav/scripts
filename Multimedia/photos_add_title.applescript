on run {}
	
	set title to the text returned of (display dialog "Enter title for image/s (blank for filename):" default answer "")
	
	tell application "Photos"
		activate
		
		set imageSel to (get selection)
		
		if imageSel is {} then
			error "Please Select Image/s."
		else
			if title = "" then
				repeat with img in imageSel
					tell img
						set the name to (text 1 thru -5 of (filename as text))
					end tell
				end repeat
			else
				set counter to 1
				repeat with img in imageSel
					tell img
						set the name to title & " - " & counter as text
						set counter to counter + 1
					end tell
				end repeat
			end if
		end if
	end tell
	
end run
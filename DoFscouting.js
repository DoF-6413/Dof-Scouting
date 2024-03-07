// DoFscouting.js (derived from ScoutingPASS.js)
//
// The "guts" of the Scounting application
// Original credit to Team 2451 - PWNAGE
//
// This version has been modified to suit Team 6413's needs with all the extra stuff removed
//
// Key to the field names that need to be in the DOM for the scripts to work properly:
// input_e = TBA Event code
// input_l_## = Match Level to scout (qm, sf, f)
// input_m = Match number (Match-input on our original form)
// input_r_## = Robot position (r1, r2, r3, b1, b2, b3)
// input_t = = Team number (TeamNumber-input on our original form)

/**
* Load the configuration data from the config_data value (found in the YYYY_config.js file that should get loaded separately).
*
* @return -1 if there was an error in the config data, 0 if the configuration was loaded successfully
*/
function configure() {
	try {
		var mydata = JSON.parse( config_data );
		}
	catch ( err ) {
		// Log the error to the console first...
		console.log( `Error parsing configuration file` )
		console.log( err.message )
		console.log( 'Use a tool like http://jsonlint.com/ to help you debug your config file' )
		
		// Then inject it into the top of the web page so scouts can see something is broken!
		var warning = document.getElementById( "header_warning" )
		warning.innerHTML = `Error parsing configuration file: ${err.message}<br><br>Use a tool like <a href="http://jsonlint.com/">http://jsonlint.com/</a> to help you debug your config file`
		return -1
		}

	// Set the page title if we were given one
	// TODO: Leaving this in for now just to test loading from a config file.  Take it out eventually.
	if ( mydata.hasOwnProperty( 'title' ) ) {
		document.title = mydata.title;
		}

	// Set the event code if we were given one
	if ( mydata.hasOwnProperty( 'eventCode' ) ) {
		document.getElementById( "input_e" ).value = mydata.eventCode;
		}

	return 0
	}


/**
* Clear out all of the scouting related fields on the form and set numeric inputs to be 0.
*/
function clearScoutingFields() {
	// Time to zap all data inputs to be our defaults.  Lets just
	// do it top to bottom, left to right...
	document.getElementById( "Leave-input" ).checked = false;

	document.getElementById( "NoShow-input" ).checked = false;

	document.getElementById( "AutoSpeaker-input" ).value = "0";
	document.getElementById( "AutoSpeakerMiss-input" ).value = "0";

	document.getElementById( "AutoAmp-input" ).value = "0";
	// document.getElementById( "AutoAmpMiss-input" ).value = "0";

	document.getElementById( "TeleSpeaker-input" ).value = "0";
	document.getElementById( "TeleSpeakerMiss-input" ).value = "0";

	document.getElementById( "TeleAmp-input" ).value = "0";
	// document.getElementById( "TeleAmpMiss-input" ).value = "0";

	document.getElementById( "TeleClimb-0" ).checked = false;
	document.getElementById( "TeleClimb-1" ).checked = false;
	document.getElementById( "TeleClimb-2" ).checked = false;
	document.getElementById( "TeleClimb-3" ).checked = false;
	document.getElementById( "TeleClimb-4" ).checked = false;

	// Clear the Climb input
	clearRadioList( "TeleClimb-input" );

	document.getElementById( "Trap-input" ).value = "0";
	document.getElementById( "TrapMiss-input" ).value = "0";

	document.getElementById( "Mic-input" ).value = "0";
	document.getElementById( "MicMiss-input" ).value = "0";

	document.getElementById( "Parked-input" ).checked = false;

	// Clear the Plays Defense input
	clearRadioList( "PlayDefense-input" );

	document.getElementById( "Card-0" ).checked = true;
	document.getElementById( "Card-1" ).checked = false;
	document.getElementById( "Card-2" ).checked = false;

	document.getElementById( "Died-input" ).checked = false;

	document.getElementById( "DefenseOnly-input" ).checked = false;

	document.getElementById( "Comment-input" ).value = "";

	// Remove the QR code
	$('#qrcode').html( '' );
}

/**
* Clear the data on the form with only minor exceptions to make moving to the next match faster
*/
function resetFormForNextMatch() {
	var match = 0;

	// NO need to save off values we want to keep as we are going to just zap items we want and
	// ignore the rest leaving them alone...

	// Get the match number
	match = parseInt( document.getElementById( "input_m" ).value );

	// Clear the "validated" state of the <BODY>.  This will NOT discard any values.  We have to manually
	// do that ourselves.
	$('body').removeClass( 'was-validated' );

	// Erase the team name happy text that is no longer validate
	document.getElementById( "teamname-label" ).innerHTML = "";

	// Update the match and team numbers for the next match
	if ( match == NaN ) {
		// If we got no match value, zap both match number AND team number
		document.getElementById( "input_m" ).value = ""
		document.getElementById( "input_t" ).value = ""
	}
	else {
		// Bump the match number then update the team number (and happy text)
		document.getElementById( "input_m" ).value = match + 1

		if ( ( getCurrentMatch() != "" ) && 
		     ( teams ) &&
			 ( getRobot() != "" && typeof getRobot() ) ) {
			document.getElementById( "input_t" ).value = getCurrentTeamNumberFromRobot().replace( "frc", "" );
			onTeamnameChange();
			}
		else {
			document.getElementById( "input_t" ).value = ""
			}
		}

	// Zap the scout initials and then clear out the scouting fields

	document.getElementById( "input_s" ).value = "";

	clearScoutingFields();
}


/**
* Get the robot code for the selected robot on the form.
*
* @return "" if no robot is selected or a value in the format of "z#" where z is either r or b and # is a value between 1 and 3
*/
function getRobot() {
	if ( document.getElementById( "input_r_r1" ).checked ) {
		return "r1";
		}
	else if ( document.getElementById( "input_r_r2" ).checked ) {
		return "r2";
		}
	else if ( document.getElementById( "input_r_r3" ).checked ) {
		return "r3";
		}
	else if ( document.getElementById( "input_r_b1" ).checked ) {
		return "b1";
		}
	else if ( document.getElementById( "input_r_b2" ).checked ) {
		return "b2";
		}
	else if ( document.getElementById( "input_r_b3" ).checked ) {
		return "b3";
		}
	else {
		return "";
		}
	}


/**
* Verify that a robot has been selected on the form.
*
* @return true if some robot has been selected, false otherwise.
*/
function validateRobot() {
	if ( document.getElementById( "input_r_r1" ).checked ||
		 document.getElementById( "input_r_r2" ).checked ||
		 document.getElementById( "input_r_r3" ).checked ||
		 document.getElementById( "input_r_b1" ).checked ||
		 document.getElementById( "input_r_b2" ).checked ||
		 document.getElementById( "input_r_b3" ).checked ) {
		return true
		}
	else {
		return false
		}
	}


/**
* Get the code for the selected match level being scouted on the form
*
* @return "qm" for qualifiers, "sf" for playoffs/double elimination, "f" for finals
*/
function getLevel() {
	if ( document.getElementById( "input_l_qm" ).checked ) {
		return "qm";
		}
	else if ( document.getElementById( "input_l_sf" ).checked ) {	// Was "de" in the original script but that is 110% wrong since TBA does NOT use "de"!
		return "sf";
		}
	else if ( document.getElementById( "input_l_f" ).checked ) {
		return "f";
		}
	else {
		return "";
		}
	}



/**
* Get the team name for the give team number
*
* @param {teamNumber} The team number to get the name for
*
* @return A string that represents the teams name or "" if the team info is not available (or there is no such team number at the event)
*/
function getTeamName( teamNumber ) {
	if ( teamNumber !== undefined ) {
		if ( teams ) {
			var teamKey = "frc" + teamNumber;
			var ret = "";
			Array.from( teams ).forEach( team => ret = team.key == teamKey ? team.nickname : ret );
			return ret;
			}
		}

	return "";
	}


/**
* Get the TBA match information (both alliances) for the specified TBA match key
*
* @param {matchKey} The TBA match code for the currently selected match and event
*
* @return A JS struct with both red and blue alliance information extracted from the schedule.  Or an empty
*			string if there is no schedule data (or the matchKey is bogus)
*/
function getMatch( matchKey ) {
	// This needs to be different than getTeamName() because of how JS stores their data
	if ( matchKey !== undefined ) {
		if ( schedule ) {
			var ret = "";
			Array.from( schedule ).forEach( match => ret = match.key == matchKey ? match.alliances : ret );
			return ret;
			}
		}

	return "";
	}


/**
* Get the team number for the currently selected match and robot position
*
* @return The team number as an integer value (sans the TBA frc prefix)
*/
function getCurrentTeamNumberFromRobot() {
	if ( getRobot() != "" && typeof getRobot() !== 'undefined' && getCurrentMatch() != "" ) {
		if ( getRobot().charAt(0) == "r" ) {
			return getCurrentMatch().red.team_keys[ parseInt( getRobot().charAt(1) ) - 1 ]
			}
		else if ( getRobot().charAt(0) == "b" ) {
			return getCurrentMatch().blue.team_keys[ parseInt( getRobot().charAt(1) ) - 1 ]
			}
		}

	// TODO: We really should return some value like 0 if we have no robot or match number selected yet?
	}


/**
* Get the TBA match key for the configured event and selected match level and match number.
*
* @return A string that represents the TBA event code for any level ( e.g. 2023azva_qm3 = Q3 at AZ East or 2023azgl_f1m2 = Finals 2 at AZ West)
*			or an empty string if the match level is not a recognized one ( e.g. "de" for double elimination)
*/
function getCurrentMatchKey() {
	// The original line below does NOT work for ANY match level besides Qualifiers!
	// The scripts do NOT properly construct the match code for Semifinals AND Finals.  
	// The match code for Semifinals is <eventCode>_sf<#>m1, not <eventCode>_sf<#>
	// The match code for Finals is <eventCode>_f1m<#>, not <eventCode>_f<#>
	// return document.getElementById( "input_e" ).value + "_" + getLevel() + document.getElementById( "input_m" ).value;

	// Here is my version that does work for all match levels.  The match key conforms to TBAs current standard
	level = getLevel();

	if ( level == "qm" ) {
		return document.getElementById( "input_e" ).value + "_" + level + document.getElementById( "input_m" ).value;
		}
	else if ( level == "sf" ) {
		return document.getElementById( "input_e" ).value + "_" + level + document.getElementById( "input_m" ).value + "m1";
		}
	else if ( level == "f" ) {
		return document.getElementById( "input_e" ).value + "_" + level + "1m" + document.getElementById( "input_m" ).value;
		}
	else {
		return "";
		}
	}


/**
* Get the match data for the currently selected match
*
* @return A JS struct with both red and blue alliance information extracted from the schedule for the current match selection.
*			OR an empty string if there is no schedule data (or the matchKey is bogus)
*/
function getCurrentMatch() {
	return getMatch( getCurrentMatchKey() );
	}


/**
* Update the match/team information on the form to match the inputs that were changed.
*
* @param {event} DOM event notification for a changed element
*/
function updateMatchStart( event ) {
	// If there is no match data available OR no team data was loaded, do nothing more
	if ( ( getCurrentMatch() == "" ) || ( ! teams ) ) {
		console.log( "No match or team data." );
		return;
		}

	// Was the change to one of the robot selections (e.g. Red1 or Blue3)?  If so, update the robot info in the DOM
	if ( event.target.id.startsWith( "input_r" ) ) {
		document.getElementById( "input_t" ).value = getCurrentTeamNumberFromRobot().replace( "frc", "" );
		onTeamnameChange();
		}

	// Was the change to the match number?  If so, update the robot info in the DOM
	if ( event.target.id == "input_m" ) {
		if ( getRobot() != "" && typeof getRobot() ) {
			document.getElementById( "input_t" ).value = getCurrentTeamNumberFromRobot().replace( "frc", "" );
			onTeamnameChange();
			}
		}

	// TODO: Why is there no check for the match level changing ( e.g. Semifinals or Final)?  If that changed
	// and we have schedule data we should be able to update the team name and number.  Perhaps they expect
	// scouts to also change from, say, Quals to Semifinals AND then change the match number.  However if the
	// steps are done in the reverse order, NOTHING will happen.  Hmmm....

	// TODO: Why is there no check for the team number changing?  There is an onChange script on the item but
	// we do not do anything if that changed.  Probably because the team number could be wrong (scouts do make
	// mistakes) or we would have to change the Robot item to be different ( e.g. Red1 -> Blue3).  It is too messy
	// to deal with a bad team change that could mess up other items.  Since we are now training scouts to set the
	// match level then robot position then match number, they should NOT be touching the team number field.
	// We probably should remove the onChange event from the item_t item OR simply use the other item values to
	// "reset" the team number to the one that matches the other inputs OR we could simply disable the field AND
	// remove the onChange handler.  I like the last option so I may go there.  For now though I'll just leave this TODO!
	}


/**
* Given the name of some radio list on the page, clear all of the radio buttons so none are checked.  This is a
* utility routine to make clearing multiple radio button lists easier than doing the same work over and over in
* another routine.
*
* @param {listName} The name of a readio button list to clear
*/
function clearRadioList( listName ) {
	var ele = document.getElementsByName( listName );
	for( var i = 0; i < ele.length; i++ )
		ele[ i ].checked = false;
}

/**
* Update the match information on the form to match the state of the NoShow checkbox when it gets changed.
* If the checkbox is Enabled then nearly all values need to get set to 0 / disabled.  We do NOT want to try to
* preserve the previous value in case the scout accidentally clicked it.  It is up to them to restore any lost data.
*
* @param {event} DOM event notification for a changed element
*/
function updateNoShow( event ) {
	// Safety check to make sure we are only doing this when called from the NoShow checkbox (NoShow-input) and 
	// the action is to check the checkbox, not clear it.
	if ( event.target.id.startsWith( "NoShow-input" ) && event.target.checked ) {
		// Zap all the scouting fields then set some defaults for a true No Show robot
		clearScoutingFields()

		// Restore the No Show checkbox 
		document.getElementById( "NoShow-input" ).checked = true;

		// Climb should be "Not Attempted"
		document.getElementById( "TeleClimb-0" ).checked = true;

		// All end game check lists should all be "Not Attempted" / "Not shown"
		document.getElementById( "Card-0" ).checked = true;

        // Set automatic "NO SHOW" comment!
        document.getElementById( "Comment-input" ).value = "NO SHOW";
		}
}


/**
* Update the team name text on the screen based on what team number is set in the DOM
*
* @param {event} UNUSED
*/
function onTeamnameChange( event ) {
	// The team number is held in the input_t (formerly TeamNumber-input) item in the DOM!
	var newNumber = document.getElementById( "input_t" ).value;
	var teamLabel = document.getElementById( "teamname-label" );
	
	if ( newNumber != "" ) {
		teamLabel.innerText = getTeamName( newNumber ) != "" ? "You are scouting " + getTeamName( newNumber ) : "That team isn't playing this match, please double check to verify correct number";
		}
	else {
		teamLabel.innerText = "";
		}
	}


/**
* When the page loads, load in our configuration and then load the team and schedule data
* for the event in the configuration.
*/
window.onload = function () {
    // Load the event configuration data and inject some of it into the DOM for use below
	var ret = configure();

	// If we could load and parse the configuration then lets try to get data from TBA for the event
	if ( ret != -1 ) {
		// Get the eventCode that was injected into the DOM when the configuration was loaded
		var ec = document.getElementById( "input_e" ).value;

		// Attempt to load the teams for the event from TBA
		getTeams( ec );

		// Attempt to load the match schedule for the event from TBA
		getSchedule( ec );
		}
	};
	

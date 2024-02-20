// TBAInterface funcitons to pull data from TheBlueAlliance.com
//
// Slightly reformatted from the original source to add comments.  The TBA key is the
// original one from ScoutingPASS.  We really should get our own but thats something to do
// AFTER the bigger changes are added to our scouting app.

// The teams at the selected event
var teams = null;

// The match schedule at the selected event
var schedule = null;

// The TBA API key to use when making TBA API calls
var authKey = "uTHeEfPigDp9huQCpLNkWK7FBQIb01Qrzvt4MAjh9z2WQDkrsvNE77ch6bOPvPb6";

/**
* Get list of teams at the event
*
* @param {eventCode} - The TBA event code (i.e. 2024azva) to pull the team list for
*/
function getTeams( eventCode ) {
	// Request the team list if we have an API key.
	if ( authKey ) {
		var xmlhttp = new XMLHttpRequest();
		var url = "https://www.thebluealliance.com/api/v3/event/" + eventCode + "/teams/simple";

		xmlhttp.open( "GET", url, true );
		xmlhttp.setRequestHeader( "X-TBA-Auth-Key", authKey );
		xmlhttp.onreadystatechange = function() {
			// State 4 means that the request had been sent, the server had finished returning the response and 
			// the browser had finished downloading the response content. Basically the AJAX call has completed.
			if ( this.readyState == 4 && this.status == 200 ) {
				var response = this.responseText;
				teams = JSON.parse( response );
			}
		};
		// Send request
		xmlhttp.send();
	}
}

/**
* Get schedule for the specified event
*
* @param {eventCode} - The TBA event code (i.e. 2024azva) to pull the schedule for
*/
function getSchedule( eventCode ) {
	// Request the team list if we have an API key.
	if ( authKey ) {
		var xmlhttp = new XMLHttpRequest();
		var url = "https://www.thebluealliance.com/api/v3/event/" + eventCode + "/matches/simple";
		
		xmlhttp.open( "GET", url, true );
		xmlhttp.setRequestHeader( "X-TBA-Auth-Key", authKey );
		xmlhttp.onreadystatechange = function() {
			// State 4 means that the request had been sent, the server had finished returning the response and 
			// the browser had finished downloading the response content. Basically the AJAX call has completed.
			if ( this.readyState == 4 && this.status == 200 ) {
				var response = this.responseText;
				schedule = JSON.parse( response );
			}
		};
		// Send request
		xmlhttp.send();
	}
}

<table width="100%" class="mainWindow">
<tr><td class="mainWindowHead">
<?php
echo '<p>Setup time period</p>';


if (get_get('subaction')) {
	session_set('subaction', get_get('subaction') );
}

if (get_get('pid')) {
	session_set('periode_pid', get_get('pid'));
}
//echo "<p>Pid now: " . session_get('periode_pid');

if (get_get('tid')) {
	session_set('periode_tid', get_get('tid'));
}

$profileinfo = $dbh->brukerprofilInfo(session_get('periode_pid') );
echo '<div class="subheader">' . $profileinfo[0] . '</div>';

?>
</td></tr>

<tr><td>
<?php
include("loginordie.php");
loginOrDie();


echo '<p>';
echo gettext("To add a new time period, you have to click on the time you want the time period to start (on the time table below).");

// funksjonen returnerer "" eller " checked " avhengig om en dag er inkludert i 
// perioden, for bruk i endrePeriode

function getChecked($helg, $dag) {
	if ($dag == 0) // Mandag - Fredag
		if ($helg == 1 OR $helg == 2) return " checked ";
	if ($dag == 1) // Lørdag eller Søndag
		if ($helg == 1 OR $helg == 3) return " checked ";
	return "";
}

function helgdescr($helg) {
	switch($helg) {
		case 1 : return gettext('All week');
		case 2 : return gettext('Weekdays');
		case 3 : return gettext('Weekend');
		default: return gettext('Uknown');
	}
}





if (!$dbh->permissionProfile( session_get('uid'), session_get('periode_pid') ) ) {
    echo "<h2>Security violation</h2>";
    exit(0);
} 

if ( isset($coor1) OR isset($coor2) ) {
	
	if (isset($coor2)) {
		$dtype = 3; $coor=$coor2;
	} else {
		$dtype = 2; $coor=$coor1;
	}
	
	preg_match("/^\?[0-9]+,([0-9]+)$/i", $coor, $match);
	$units = round((($match[1]-10) / 7.5) + 12) % 48;
	$time = floor($units / 2);
	$min = ($units % 2) * 30; 
	if ($min > 9 ) $klokke = "$time:$min"; else
	$klokke = "$time:0$min";
	
	$tidsid = $dbh->nyTidsperiode($dtype, $klokke, session_get('periode_pid') );
	
	if ($tidsid > 0) { 
	echo gettext("<p><font size=\"+3\">OK</font>, a new time periods is created. Go to the form below to setup alerts for this time period.");
	  session_set('subaction', "endre");
	} else {
	echo "<p><font size=\"+3\">" . gettext('An error</font> occured, a new profile is <b>not</b> created."');
	}
	
	session_set('periode_tid', $tidsid);
  
}


// Endre ting angående en periode både info, adresser og utstyrsgrupper
if (session_get('subaction') == 'endreperiode') {

	$dbh->endrePeriodeinfo(session_get('periode_tid'), post_get('dagtype'), post_get('time'), post_get('min') );
	echo gettext("<p><font size=\"+3\">OK</font>, time period properies are changed.");

}

// Fjerne en varsling
if (session_get('subaction') == 'slett') {
	$dbh->endreVarsleadresse( session_get('periode_tid'), get_get('daid'), get_get('deid'), 4 );
	echo gettext("<p><font size=\"+3\">OK</font>, an alert subscription is removed.");

}


// Endre ting angående en periode både info, adresser og utstyrsgrupper
if (session_get('subaction') == 'nyvarsling') {

	reset ($HTTP_POST_VARS);
	$adrs = null;
	$eqgrps = null;
	while ( list($n, $val) = each ($HTTP_POST_VARS)) {
		if ( preg_match("/eqgrp([0-9]+)/i", $n, $m) ) {   // Equipment groups
			$eqgrps[] = $m[1];
		}
		if ( preg_match("/adr([0-9]+)/i", $n, $m) ) {   // Address
			$adrs[] = $m[1];
		}
	}
	
	if ( sizeof($adrs) < 1 OR sizeof($eqgrps) < 1 ) {
		echo "<p><font size=\"+3\">" . gettext('An error</font> occured, at least one address and one equipment group has to be selected."');
	} else {
		
		foreach ($adrs AS $aid)
			foreach ($eqgrps AS $eid)	
				$dbh->endreVarsleadresse(session_get('periode_tid'), $aid, $eid, post_get('queuetype') );
				//echo '<p>A:' . $aid . 'E:' . $eid . 'Q:' . post_get('queuetype'). ':' ;		
		
		echo gettext("<p><font size=\"+3\">OK</font>, new alert subscriptions is added.");
	}	

}







// Hente ut info om periode
$periodeinfo = $dbh->periodeInfo(session_get('periode_tid') );


// Setup general properties for time period
echo '<div class="newelement"><h2>' . gettext('Setup time period properties') . '</h2>';

echo "<form name=\"endre\" method=\"post\" action=\"index.php?action=periode-setup&subaction=endreperiode\">";

echo '<table cellpadding=0 cellspacing=0 border=0 width="100%"><tr><td width="40%">';

// Setup start time
echo '<p>' . gettext('Start time') . ": ";
echo '<input name="time" type="text" id="time" value="' . 
	leading_zero($periodeinfo[1], 2, 0) . '" size="2" maxlength="2"> : ';
echo '<input name="min" type="text" id="min" value="' .
	leading_zero($periodeinfo[2], 2, 0) . '" size="2" maxlength="2">  ';
	
echo '</td><td width="40%">';	

// Setup day type		weekend / weekdays etc.

echo '<p><select name="dagtype">';
for ($i = 1; $i <= 3; $i++) {
	$selected = ( $periodeinfo[0] == $i ) ? ' selected' : '';
	echo '<option value="' . $i . '"' . $selected . '>' . helgdescr($i) . '</option>';
}
echo '</select>';

echo '</td><td width="20%">';

echo '<p><input type="submit" name="Submit" value="' . gettext("Save changes") . '">  ';

echo '</td></tr></table>';

echo "</form></div>";
echo '<form name="nyv" method="post" action="index.php?action=periode-setup&subaction=nyvarsling">';

// List over current alerts.
$varslingliste = new Lister( 46,
	array(gettext('Equipment'), gettext('Type'), gettext('Address'), gettext('Queue'), gettext('Options')),
	array(30, 15, 30, 20, 5),
	array('left', 'left', 'left', 'left', 'right'),
	array(true, true, true, true, false),
	1);

if ( get_exist('sortid') )
	$varslingliste->setSort(get_get('sort'), get_get('sortid') );

$varslinger = $dbh->listAlleVarsleAdresser(session_get('uid'), 
	session_get('periode_tid'), $varslingliste->getSort());

for ($j = 0; $j < sizeof($varslinger); $j++) {
	switch($varslinger[$j][2]) {
		case 1 : $type_icon = '<p><img alt="ikon" src="icons/mail.gif" border=0>&nbsp;E-post'; break;
		case 2 : $type_icon = '<p><img alt="ikon" src="icons/mobil.gif" border=0>&nbsp;SMS'; break;
		case 3 : $type_icon = '<p><img alt="ikon" src="icons/irc.gif" border=0>&nbsp;IRC'; break;
		case 4 : $type_icon = '<p><img alt="ikon" src="icons/icq.gif" border=0>&nbsp;ICQ'; break;				
		default : $type_icon = '<p><img alt="ikon" src="" border=0>&nbsp;Ukjent'; break;				
	}
	
	if ($varslinger[$j][6] == 't') {
		$owner_icon = '<img alt="Mine" src="icons/person1.gif">';
	} else {
		$owner_icon = '<img alt="Shared" src="icons/person100.gif">';	
	}

	switch ($varslinger[$j][3] ) {
		case 1: $queue_type = '<img src="icons/queue.png" alt="Queue">Queue [Daily]'; break;
		case 2: $queue_type = '<img src="icons/queue.png" alt="Queue">Queue [Weekly]'; break;
		case 3: $queue_type = '<img src="icons/queue.png" alt="Queue">Queue [Next time period]'; break;
		case 0: $queue_type = '<img src="icons/direct.png" alt="Queue">Immidiate'; break;
		case 4: $queue_type = 'QUEUE TYPE IS DEPRECATED'; break;
		default: $queue_type = 'Uknown'; break;
	}
	
	$delete_icon = '<a href="index.php?action=periode-setup&subaction=slett&deid=' . $varslinger[$j][4] . 
		'&daid=' . $varslinger[$j][0] . '">' .
		'<img alt="Delete" src="icons/delete.gif" border=0></a>';

	$varslingliste->addElement( array(
		'<p>' . $owner_icon .  $varslinger[$j][5], // equipment group name
		$type_icon, // alert type
		$varslinger[$j][1], // address
		$queue_type, // queue
		$delete_icon, // options
		) );	
}			

echo "<h2>" . gettext("Current alert subscriptions for this time period.") . "</h2>" . 
	$varslingliste->getHTML();



echo '<p>&nbsp;<div class="newelement">';
echo '<h2>Add new alerts subscriptions for time period</h2>';
echo '<h3>Select one or more equipment groups</h3>';

// List over all equipment groups.
$utst = new Lister( 47,
	array(gettext('Check'), gettext('Owner'), gettext('Equipment group'), gettext('#periods'), gettext('#filters')),
	array(10, 10, 50, 15, 15),
	array('left', 'left', 'left', 'left', 'left'),
	array(false, false, false, false, false),
	1);

if ( get_exist('sortid') )
	$utst->setSort(get_get('sort'), get_get('sortid') );

$ut = $dbh->listUtstyr(session_get('uid'), 1 );
for ($i = 0; $i < sizeof($ut); $i++) {

	if ($ut[$i][4] == 't') {
		$min = "<img alf=\"Min\" src=\"icons/person1.gif\">"; 
	} else {
		$min = "<img alf=\"Gruppe\" src=\"icons/person100.gif\">";
	}

	if ($ut[$i][5] == 't') {
		$valgt = " checked";
	} else {
		$valgt = "";
	}

	if ($ut[$i][2] > 0 ) { 
		$ap = $ut[$i][2]; 
	} else { 
		$ap = "<img alt=\"Ingen\" src=\"icons/stop.gif\">"; 
	}

	if ($ut[$i][3] > 0 ) { 
		$af = $ut[$i][3]; 
	} else { 
		$af = "<img alt=\"Ingen\" src=\"icons/stop.gif\">"; 
	}
	$check = '<input type="checkbox" name="eqgrp' . $ut[$i][0] . '">';
	
	$utst->addElement( array(
		$check, //Checkbox
		$min, // eier
		$ut[$i][1], // navn
		$ap, // antall perioder
		$af  // antall filtre
		) );

	//$utst->addElement(new HTMLCell($adrt) );
}
echo $utst->getHTML();





// List all my addresses

echo '<h3>Select one or more alert addresses</h3>';

$l = new Lister( 48,
		array(gettext('Check'), gettext('Type'), gettext('Address') ),
		array(10, 30, 60),
		array('left', 'left', 'left', 'right'),
		array(false, false, false ),
		0 
);

if ( get_exist('sortid') )
	$l->setSort(get_get('sort'), get_get('sortid') );

$adr = $dbh->listAdresser(session_get('uid'), 0 );

for ($i = 0; $i < sizeof($adr); $i++) {


	switch($adr[$i][2]) {
		case 1 : $type = '<img alt="mail" src="icons/mail.gif" border=0>&nbsp;' . gettext("E-mail"); break;
		case 2 : $type = '<img alt="sms" src="icons/mobil.gif" border=0>&nbsp;' . gettext("SMS"); break;
		case 3 : $type = '<img alt="irc" src="icons/irc.gif" border=0>&nbsp;' . gettext("IRC"); break;
		case 4 : $type = '<img alt="icq" src="icons/icq.gif" border=0>&nbsp;' . gettext("ICQ"); break;				
		default : $type = '<img alt="ukjent" src="" border=0>&nbsp;' . gettext("Unknown"); break;				
	}


	$check = '<input type="checkbox" name="adr' . $adr[$i][0] . '">';
	
	$l->addElement( array(
		$check, // $check
  		$type,  // type
		$adr[$i][1]  // adresse 
		) 
	);
}

echo $l->getHTML();


echo '<table cellpadding=0 cellspacing=0 border=0 width="100%"><tr><td width="50%">';
echo '<h3>Select queueing type</h3>';
echo '<p><select name="queuetype">';
echo '<option value="0" selected>Immiate</option>';
echo '<option value="1">Queue [Daily]</option>';
echo '<option value="2">Queue [Weekly]</option>';
echo '<option value="3">Queue</option>';
echo '</select></td><td width="50%">';


echo '<p><input type="submit" name="Submit" value="' . gettext("Add alert subscriptions to time period") . '">  ';
echo "</form>";
echo '</td></tr></table></div>';

echo '<p><form name="finnished" method="post" action="index.php?action=periode">';
echo '<input align="right" type="submit" name="Submit" value="' . gettext('Finished setting up this time period') . '">';
echo '</form>';

?>

</td></tr>
</table>

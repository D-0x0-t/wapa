<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- WAPA browser GUI -->
<head>
  <title>WAPA</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="icon" type="image/x-icon" href="../img/favicon.ico">
</head>

<body bgcolor="#a1d9d3">
<center>
<table cellspacing=0 cellpadding=2 width=1000 height=350 border=0>

<tr>
  <td colspan="3" align="center" valign="MIDDLE">
    <h1><abbr title="Wireless Access Point Auditor">WAPA</abbr> browser GUI</h1>
  </td>
</tr>
<tr>
  <td colspan="3">&nbsp;</td>
</tr>
<tr>
  <td colspan="3" align="center" valign="MIDDLE">
    <h2>Welcome to the wireless access point auditor query builder</h2>
  </td>
</tr>
<?php 
    if (isset($_REQUEST['next'])){ 
        $action = $_REQUEST['what_to_do'];
        if ($action == "scan"){
            $interfaces_list = shell_exec('iwconfig | grep wl | awk "{print \$1}" | tr " " "\n"');
?>
                <tr>
                    <td colspan="3" align="center" valign="MIDDLE">
                        <p>In order to perform a scan, please, select a network interface:</p>
                    </td>
                </tr>
                <tr>
                    <td colspan="3" align="center" valign="MIDDLE">
                        <p><pre><?php echo $interfaces_list; ?></pre></p></br>
                        <form action="scan/" method="post">
                            <label for="iface">Insert the name of the interface to use:</label>
                            <input type="text" id="iface" name="iface"></br></br>
                            <label for="timer">Insert a value in seconds</label>
                            <input type="number" id="timer" name="timer"><br><br>
                            <input type="submit" value="Next" name="do_scan">
                        </form>
                    </td>
                </tr>
<?php
        } elseif ($action == "attack") {
?>
                <tr>
                    <td colspan="3" align="center" valign="MIDDLE">
                        <p></p>
                    </td>
                </tr>
                <tr>
                    <td colspan="3" align="center" valign="MIDDLE">
                        <h1>test</h1>
                    </td>
                </tr>

<?php
        } else { // demo
?>
                <tr>
                    <td colspan="3" align="center" valign="MIDDLE">
                        <p></p>
                    </td>
                </tr>
                <tr>
                    <td colspan="3" align="center" valign="MIDDLE">
                        <h1>test</h1>
                    </td>
                </tr>

<?php
        }
?>

<?php


    } else {
?>


        <tr>
        <td colspan="3" align="center" valign="MIDDLE">
            <p>Choose an option from the following:</p>
        </td>
        </tr>
        <tr>
        <td colspan="3" align="center" valign="MIDDLE">
            <form action="" method="post">
                <label for="what_to_do">I want to</label>
                <select id="what_to_do" name="what_to_do">
                    <option value="scan">scan near networks</option>
                    <option value="attack">attack near networks</option>
                    <option value="demo">see a demonstration</option>
                </select>
                </br>
                </br>
                </br>
                <input type="submit" value="Next" name="next">
            </form>
        </td>
        </tr>
<?php
    }
?>
<tr><td colspan=5>&nbsp;</td></tr>
<tr>
  <td align=center width=200 valign="MIDDLE">
    <a href="../help">
        <p>Help</p>
    </a>
  </td>
  <td align=center width=200 valign="MIDDLE">
    <a href="../">
      <p>Home</p>
    </a>
  </td>
</tr>
</table>
</body>
</html>

#!/usr/local/bin/perl
# Start the Ajaxterm webserver on a random port, then print an iframe for
# a URL that proxies to it

BEGIN { push(@INC, ".."); };
use WebminCore;
use Socket;
&init_config();

&ui_print_header(undef, $text{'index_title'}, "", undef, 1, 1);

# Check for python
$python = &has_command("python");
if (!$python) {
	&ui_print_endpage(&text('index_epython', "<tt>python</tt>"));
	}

# Pick a free port
&get_miniserv_config(\%miniserv);
$port = $miniserv{'port'} + 1;
$proto = getprotobyname('tcp');
socket(TEST, PF_INET, SOCK_STREAM, $proto) ||
	&error("Socket failed : $!");
setsockopt(TEST, SOL_SOCKET, SO_REUSEADDR, pack("l", 1));
while(1) {
	last if (bind(TEST, sockaddr_in($port, INADDR_ANY)));
	$port++;
	}
close(TEST);

# Run the Ajaxterm webserver
$pid = fork();
if (!$pid) {
	chdir("$module_root_directory/ajaxterm");
	untie(*STDIN); open(STDIN, "</dev/null");
	untie(*STDOUT); open(STDOUT, ">/dev/null");
	untie(*STDERR); open(STDERR, ">/dev/null");
	exec($python, "ajaxterm.py", "--port", $port, "--log");
	exit(1);
	}

# Wait for it to come up
$try = 0;
while(1) {
	my $err;
	&open_socket("localhost", $port, TEST2, \$err);
	last if (!$err);
	$try++;
	if ($try > 30) {
		&error(&text('index_estart', 30, $port));
		}
	sleep(1);
	}
close(TEST2);

# Show the iframe
print "<center>\n";
print "<iframe src=$gconfig{'webprefix'}/$module_name/proxy.cgi/$port/ ",
      "width=580 height=420 frameborder=0></iframe><br>\n";
print "<input type=button onClick='window.open(\"proxy.cgi/$port/\", \"ajaxterm\", \"toolbar=no,menubar=no,scrollbars=no,resizable=yes,width=580,height=420\")' value='$text{'index_popup'}'>\n";
print "</center>\n";

# Fork process that checks for inactivity
if (!fork()) {
	untie(*STDIN); close(STDIN);
	untie(*STDOUT); close(STDOUT);
	untie(*STDERR); close(STDERR);
	$statfile = "$ENV{'WEBMIN_VAR'}/$module_name/$port";
	while(1) {
		my @st = stat($statfile);
		if (@st && time() - $st[9] > $config{'timeout'}) {
			# No activity
			last;
			}
		if (!kill(0, $pid)) {
			# Dead
			last;
			}
		sleep(10);
		}
	unlink($statfile);
	kill('KILL', $pid);
	exit(0);
	}

&ui_print_footer("/", $text{'index'});


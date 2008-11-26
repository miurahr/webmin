#!/usr/local/bin/perl
# Show a list of signing keys, with a form to add

require './bind8-lib.pl';
$access{'defaults'} || &error($text{'dnssec_ecannot'});
&ui_print_header(undef, $text{'dnssec_title'}, "",
		 undef, undef, undef, undef, &restart_links());

# Create keys table
@keys = &list_dnssec_keys();
foreach $k (@keys) {
	# XXX
	}
print &ui_form_columns_table(
	"delete_dnssec.cgi",
	[ [ undef, $text{'dnssec_delete'} ] ],
	0,
	undef,
	undef,
	[ $text{'dnssec_id'}, $text{'dnssec_alg'}, $text{'dnssec_bits'},
	undef,
	\@table);

# Show new new form
print &ui_form_start("create_dnssec.cgi", "post");
print &ui_table_start($text{'dnssec_header'}, undef, 2);

# XXX key name

# XXX key algorithm
# XXX default to DSA

# XXX bits

print &ui_table_end();
print &ui_form_end([ [ undef, $text{'create'} ] ]);

&ui_print_footer("", $text{'index_return'});
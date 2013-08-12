from livesettings import config_register, ConfigurationGroup, StringValue, LongStringValue, MultipleStringValue

SUBJECT="Your GenieDB cluster is ready!"
PLAINTEXT="""
Hi {username}, please find the information for your cluster below. I wanted to
point out a few things that you will need.

1. There is a default database '{db}' created.
2. To create any table that you want replicated, you should add
   'ENGINE=GenieDB' to the end of the SQL statement.
   e.g. CREATE TABLE {db}.foo(a INT PRIMARY KEY, b INT) ENGINE=GenieDB;
3. To create any non-replicated table, you can use ENGINE=MyISAM or
   ENGINE=InnoDB.
4. You should set up application servers close to the individual servers.
5. The common DNS name
   {cluster_dns}
   will automatically find the nearest database
6. The nodes can be directly accessed using specific domain name (notice the
   -1, -2 etc) or IP addresses.

This cluster will be available for your use until {trial_end:%d}{ord}
{trial_end:%B}, at which point we can discuss the results of your trial and
whether or not you want to move forward. Please don't hesitate to let me know
if you have any questions or issues. We are happy to help with your testing or
answer any questions you may have regarding distributed system architecture.

Cluster Details
username: {dbusername}
password: {dbpassword}   <-- Please change the password at your earliest
                             convenience :)  The change needs to be done on
                             all servers individually.
database: {db}
port: {port}

LBR DNS: {cluster_dns}

{node_text}
"""
HTML="""<html>
  <head>
    <style>
* {{
  font-family:verdana,geneva,sans-serif;
}}
    </style>
  </head>
  <body>
    <p>Hi {username}, please find the information for your cluster below. I wanted to point out a few things that you will need.</p>
    <ol>
      <li>There is a default database &quot;{db}&quot; created.</li>
      <li>To create any table that you want replicated, <strong>you should add &quot;ENGINE=GenieDB&quot;</strong> to the end of the SQL statement.
        <ul>
          <li>e.g. CREATE TABLE {db}.foo(a INT PRIMARY KEY, b INT) ENGINE=GenieDB;</li>
        </ul>
      </li>
      <li>To create any non-replicated table, you can use ENGINE=MyISAM or ENGINE=InnoDB.</li>
      <li>You should set up application servers close to the individual servers.</li>
      <li>The common DNS name <strong>{cluster_dns}</strong> will automatically find the nearest database.</li>
      <li>The nodes can be directly accessed using specific domain name (notice the -1, -2 etc) or IP addresses.</li>
    </ol>
    <p>This cluster will be available for your use until {trial_end:%d}{ord} {trial_end:%B}, at which point we can discuss the results of your trial and whether or not you want to move forward. Please don&#39;t hesitate to let me know if you have any questions or issues. We are happy to help with your testing or answer any questions you may have regarding distributed system architecture.</p>
    <p><strong>Cluster Details</strong></p>
    <p>Username: {dbusername}</p>
    <p>Password: {dbpassword} &lt;-- Please change the password at your earliest convenience :-)&nbsp;<span style="font-size: 11pt;">The change needs to be done on all servers individually.</span></p>
    <p>Database: {db}</p>
    <p>Port: {port}</p>
    <p>&nbsp;</p>
    <p>Common DNS: <strong>{cluster_dns}</strong></p>
    <p>&nbsp;</p>
{node_html}
</body>
</html>
"""
PLAINTEXT_PER_NODE="""
Node {nid}
Location: {region}
DNS: {node_dns}
IP: {node_ip}
"""
HTML_PER_NODE="""
    <p><strong>Node {nid}</strong></p>
    <p>Location: {region}</p>
    <p>DNS: {node_dns}</p>
    <p>IP: {node_ip}</p>
"""
SENDER="newcustomer@geniedb.com"
RECIPIENTS=["newcustomer@geniedb.com"]

EMAIL_GROUP = ConfigurationGroup(
	'api_email',
	"EMail settings"
)

config_register(StringValue(
	EMAIL_GROUP,
	'SENDER',
	default=SENDER,
	description="Address to send emails from"
))
config_register(MultipleStringValue(
	EMAIL_GROUP,
	'RECIPIENTS',
	default=RECIPIENTS,
	description="Addresses to send emails to"
))
config_register(StringValue(
	EMAIL_GROUP,
	'SUBJECT',
	default=SUBJECT,
	description="Email subject"
))
config_register(LongStringValue(
	EMAIL_GROUP,
	'PLAINTEXT_PER_NODE',
	default=PLAINTEXT_PER_NODE,
	description="Plain text for each node",
        help_text="""Template parameters:
{nid} = Node ID
{region} = Region
{node_dns} = DNS Address
{node_ip} = IP Address
"""
))
config_register(LongStringValue(
	EMAIL_GROUP,
	'HTML_PER_NODE',
	default=HTML_PER_NODE,
	description="HTML for each node",
        help_text="""Template parameters:
{nid} = Node ID
{region} = Region
{node_dns} = DNS Address
{node_ip} = IP Address
"""
))
config_register(LongStringValue(
	EMAIL_GROUP,
	'PLAINTEXT',
	default=PLAINTEXT,
	description="Plain text email body",
        help_text="""Template parameters:
{node_text} = concatenated per-node plaintext
{node_html} = concatenated per-node HTML
{username} = DBaaS username
{cluster_dns} = Latency Based Routing DNS Address
{trial_end} = date when trial ends
{ord} = Ordinal for day of month of trial_end
{port} = Port mysqld is listening on
{db} = MySQL database name
{dbusername} = MySQL username
{dbpassword} = MySQL password
"""
))
config_register(LongStringValue(
	EMAIL_GROUP,
	'HTML',
	default=HTML,
	description="HTML email body",
        help_text="""Template parameters:
{node_text} = concatenated per-node plaintext
{node_html} = concatenated per-node HTML
{username} = DBaaS username
{cluster_dns} = Latency Based Routing DNS Address
{trial_end} = date when trial ends
{ord} = Ordinal for day of month of trial_end
{port} = Port mysqld is listening on
{db} = MySQL database name
{dbusername} = MySQL username
{dbpassword} = MySQL password
"""
))

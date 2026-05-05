# wazuh-sms-alert-integration
Custom SMS alert integration for Wazuh SIEM


# Wazuh Custom Integration: Office SMS Alerts (via API)
This documentation explains how to integrate Wazuh with an external SMS Gateway API to send high-priority alerts (Level 10+) directly to mobile devices using JSON format.

# Overview
Wazuh allows integration with external APIs via its framework. This custom integration triggers when an alert matches the specified criteria and sends the alert data to a pre-configured SMS endpoint.

# Features
Real-time SMS alert for critical threats                                                              
Server down/up হলে instant notification                                                                       
Faster incident response                                                                                         
Works with Wazuh SIEM                                                                                            

# Prerequisites
Wazuh Manager installed and running.

Access to an SMS Gateway API (or a custom script to handle the SMS).

Root/Sudo privileges on the Wazuh Manager server.

# Step 1: Configuration in ossec.conf
First, you need to tell Wazuh to use the custom integration. Edit the Wazuh manager configuration file:

Bash
nano /var/ossec/etc/ossec.conf
Add the following block inside the <ossec_config> section:

XML
<integration>
  <name>office_sms</name>
  <level>10</level>
  <alert_format>json</alert_format>
</integration>
Parameters:
name: The name of the executable script (must start with custom-).

level: The minimum alert level that triggers this integration (e.g., 10 for high-security events).

alert_format: The data format sent to the script (JSON is recommended for modern APIs).

# Step 2: Create the Integration Script
Wazuh looks for integration scripts in /var/ossec/integrations/. The script name must match the <name> tag in ossec.conf with a custom- prefix.

Create the file:

Bash
touch /var/ossec/integrations/custom-office_sms
chmod 750 /var/ossec/integrations/custom-office_sms
chown root:wazuh /var/ossec/integrations/custom-office_sms
Add your logic (Example using Python/Bash to call your SMS API):
(Note: This is where you put your Python code that sends the POST request to the SMS Gateway).

# Step 3: Restart Wazuh Manager
To apply the changes, restart the Wazuh manager service:

Bash
systemctl restart wazuh-manager
Step 4: Testing & Verification
To ensure the integration is working, you can monitor the active logs:

1. Check Integration Logs
Bash
tail -f /var/ossec/logs/ossec.log | grep -i "office_sms"
2. Simulate a Level 10 Alert
You can use a tool like logger to trigger a rule that meets the level 10 threshold. For example, multiple failed SSH logins often trigger high-level rules.

3. Verify the Payload
If you are using a tool like Webhook.site for testing, verify that the JSON payload contains the rule.id, description, and full_log.

# Troubleshooting
Permissions: Ensure the script in /var/ossec/integrations/ has the correct owner (root:wazuh).

Format: If the API requires a specific JSON structure, ensure your script parses the Wazuh alert properly before sending.

Firewall: Ensure the Wazuh manager has outbound access to your SMS Gateway API URL.

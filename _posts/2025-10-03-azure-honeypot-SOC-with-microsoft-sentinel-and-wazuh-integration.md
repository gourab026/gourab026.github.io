---
title: Azure Honeypot SOC with Microsoft Sentinel and Wazuh Integration
author: gourabdg47
date: 2025-10-03 11:52:00
categories:
  - Project
  - Home-Lab-2
tags:
  - writing
  - project
  - cybersecurity
render_with_liquid: true
---


Of course\! Here is your blog post converted into proper Markdown format, ready for publishing.

-----

# Building an Azure Honeypot SOC: A Step-by-Step Guide with Microsoft Sentinel and Wazuh

Hey fellow cyber enthusiasts\! Ever wondered how to get *hands-on* with a Security Operations Center (SOC) environment without breaking the bank? In this post, I'll walk you through setting up an Azure-based honeypot, integrating it with **Microsoft Sentinel** for cloud-native SIEM capabilities, and then forwarding those logs to a **Wazuh** server running on GCP for cross-cloud visibility and advanced threat detection. This is a journey I recently undertook, and I'm excited to share the steps with you.

Let's dive in\!

-----

## Getting Started with Azure 

First things first, you'll need an Azure account.

  * **Create an Azure Account**: If you don't have one, sign up and get your free $200 credit. I used a personal email address for my setup.
  * **Access the Azure Portal**: Navigate to the [Azure Portal](https://www.google.com/search?q=https://portal.azure.com/).

-----

## Setting Up Your Azure Infrastructure 

We'll start by creating the foundational elements in Azure.

### 1\. Create a Resource Group

A resource group acts as a logical container for your Azure resources.

  * **Name**: `RG-SOC-L1`
  * **Subscription**: Select your active subscription.
  * **Region**: East US 2 (This is important for network latency and service availability).

### 2\. Create a Virtual Network (VNet)

Your VNet will house your honeypot VM and define its network boundaries.

  * **Resource Group**: Select `RG-SOC-L1`.
  * **Name**: `VNet-SOC-Lab`
  * **Region**: East US 2 (Matches your Resource Group).
  * **Other settings**: Keep all other settings as default for simplicity.

### 3\. Deploy Your Honeypot Virtual Machine (VM)

This is the star of our show – a Windows 10 VM deliberately exposed to the internet.

  * **Service**: Search for and select "Azure Virtual Machine".
  * **Resource Group**: `RG-SOC-L1`
  * **Virtual Machine Name**: `SECURE-NET-EAST`
  * **Region**: East US 2
  * **Image**: Windows 10 Pro, version 22H2 - x64 Gen2 (ensure it's eligible for free services).
  * **Administrator Account**:
      * **Username**: `<your-vm-username>`
      * **Password**: `<Your-Complex-Password-Here>`
    > **Security Note**: Even for a lab, never use simple or default passwords. Always create a strong, unique password\!
  * **Disk**: Default - 127 GB Premium SSD.
  * **Networking**:
      * **Virtual Network**: `VNet-SOC-Lab`
      * **Delete public IP and NIC when VM is deleted**: Set to True.
  * **Management**: Keep default.
  * **Monitoring**: Boot diagnostics - Disable.
  * **Advanced**: Keep default.

-----

## Exposing Your Honeypot (The "Danger" Part\!) 

To ensure our honeypot attracts attention, we need to open it up.

1.  Navigate to your Resource Group: Go back to **RG-SOC-L1**.
2.  Access Network Security Group (NSG): Click on the NSG associated with your VM (it will typically have `-nsg` in its name).
3.  **Delete Existing RDP Rule**: Go to "Inbound security rules" and delete the default RDP rule.
4.  **Add a New Inbound Rule**:
      * **Source**: Any
      * **Source port ranges**: `*`
      * **Destination**: Any
      * **Destination port ranges**: `*`
      * **Protocol**: Any
      * **Action**: Allow
      * **Priority**: Lower than 65500 (e.g., `100`)
      * **Name**: `DANGER_AnythingEverything`

### Disabling the Windows Firewall

Further exposing our honeypot requires turning off the local firewall.

1.  **Connect to your VM**: Use Remote Desktop Connection (RDC) from your local machine with the VM's public IP and the credentials you created above.
2.  **Disable Windows Defender Firewall**:
      * Inside the VM, type `wf.msc` in the Run dialog to open Windows Defender Firewall.
      * Click on "Windows Defender Firewall Properties".
      * Go through each tab (Domain Profile, Private Profile, Public Profile) and set "**Firewall state**" to **Off**.

### Verifying Exposure and Initial Attack Logs 

  * **Ping the VM**: From your local machine, ping the VM's public IP to confirm connectivity.
  * **Check for Failed Login Events**: Inside your VM, open **Event Viewer** (type `eventvwr.msc` in Run). Navigate to **Windows Logs \> Security** and filter for **Event ID 4625** (failed login attempts). You should start seeing these as your honeypot attracts attention\!

-----

## Integrating with Azure Log Analytics & Microsoft Sentinel 

Now, let's collect and analyze these logs with Azure's native security tools.

### 1\. Create a Log Analytics Workspace

This workspace will be the central repository for your VM's logs.

  * **Search**: In the Azure portal, search for "Log Analytics Workspace".
  * **Resource Group**: `RG-SOC-L1`
  * **Name**: `LOG-SOC-L1`

### 2\. Deploy Microsoft Sentinel

Microsoft Sentinel is Azure's cloud-native SIEM.

1.  **Create Sentinel**: In the Azure portal, search for "Microsoft Sentinel" and click "Create".
2.  **Select Workspace**: Choose your `LOG-SOC-L1` workspace.
3.  **Configure Data Connector**:
      * Inside Sentinel, go to "**Content hub**".
      * Search for "Windows Security Event" and install it.
      * Click on the "Windows Security Event" solution, then "**Manage**", and select "**Windows Security Events via AMA**" (Azure Monitor Agent).
      * Click "**Open connector page**".
4.  **Create a Data Collection Rule (DCR)**:
      * **Name**: `DCR-windows`
      * **Resources**: Select your VM - `SECURE-NET-EAST`.
      * **Collect**: Choose "**All events**".
5.  **Verification**: Go to your VM's settings in the Azure portal -\> "**Extensions**". Ensure the newly created collector shows up.

> **Important**: Make sure your VM is running during these steps\!

### Verify Logs in Log Analytics

1.  Go to your `LOG-SOC-L1` Log Analytics Workspace.
2.  Select "**Logs**".
3.  In the Kusto Query Language (KQL) editor, type the following and run the query. You should now see your security events flowing in\!
    ```kql
    SecurityEvent
    ```

> **Note on Sentinel Free Trial**: Remember that Microsoft Sentinel typically offers a free trial (e.g., 10 GB/day for both Sentinel and Log Analytics). Keep an eye on your consumption to avoid unexpected charges after the trial period.

-----

## Cross-Cloud SIEM with Wazuh (on GCP)

To add another layer of visibility and demonstrate cross-cloud integration, we'll onboard our Azure VM's logs to a Wazuh server. I already had a GCP instance running with free credit for this.

### 1\. Set Up Wazuh Server (on GCP)

If you don't have Wazuh already, here's a quick way to get it running.

1.  **Install Wazuh**:
    ```bash
    curl -sO https://packages.wazuh.com/4.13/wazuh-install.sh && sudo bash ./wazuh-install.sh -a
    ```
2.  **Access Wazuh UI**: Once installed, navigate to `https://<your_wazuh_server_ip>:443` and log in with the provided credentials.

### 2\. Install and Configure Wazuh Agent on Azure VM

This agent will forward logs from your Windows 10 honeypot to your Wazuh server.

1.  On the Azure VM (**PowerShell as Administrator**):
    ```powershell
    Invoke-WebRequest -Uri https://packages.wazuh.com/4.x/windows/wazuh-agent-4.13.1-1.msi -OutFile $env:tmp\wazuh-agent; msiexec.exe /i $env:tmp\wazuh-agent /q WAZUH_MANAGER='<YOUR_WAZUH_SERVER_IP>' WAZUH_AGENT_NAME='azure-win-L1'
    ```
    (Note: Replace `<YOUR_WAZUH_SERVER_IP>` with the actual public IP of your Wazuh server on GCP).
2.  **Verify Agent Configuration**:
      * Open `C:\Program Files (x86)\ossec-agent\ossec.conf` with Notepad.
      * Ensure the `<client><server><address>` section contains the correct IP of your Wazuh server.
3.  **Configure Auto-Start & Start Agent**:
    ```powershell
    sc config WazuhSvc start= auto
    NET START WazuhSvc
    ```

### 3\. Verify Agent Connection on Wazuh Server

On your Wazuh Server (via SSH):

```bash
sudo /var/ossec/bin/manage_agents -l
```

You should see your `azure-win-L1` agent listed\!

### Visualizing Attacks with Wazuh Maps

Wazuh's Kibana integration allows for stunning geospatial visualizations of attacks.

  * Create a new **Map Visualization** in Wazuh (Kibana).
  * **Index pattern**: `wazuh-alerts-*`
  * **Geospatial field**: `Geolocation.location`
  * Enable tooltips and add relevant fields for more context (e.g., `rule.description`, `src_ip`).
  * **Enjoy the Visualization**: You'll start seeing attack origins light up on your map in real-time\!

-----

## Next Steps & Enhancements (TO-DOs) 

This setup is a fantastic starting point. Here's a list of crucial next steps to enhance your SOC capabilities:

  * **Understand and Study Sysmon Logs**: Sysmon provides incredibly detailed host-level telemetry that's invaluable for threat hunting.
  * **Set Up Sysmon Log Collection**: Configure Sysmon on your Azure VM.
  * **Ingest Sysmon Logs into Wazuh**: Create the necessary configurations in Wazuh to receive and parse Sysmon events.
  * **Create Custom Wazuh Rules**: Develop specific rules to accurately classify malicious activities based on Sysmon and other logs.
  * **Perform Cyber Threat Intelligence (CTI)**: Deep-dive into the attackers' tactics, techniques, and procedures (TTPs) using your collected IOCs.
  * **Learn to Mitigate Attacks from Wazuh**: Explore Wazuh's active response capabilities to automate blocking or containment actions.

-----

## Architecture Overview

Here's a simplified view of the architecture we've built:

```
L1 (Outer layer) - Azure Subscription
  |
  +-- L1 NSG (Network Security Group / Cloud Firewall)
  |      (Internet traffic connects through here)
  |
  +-- L2 Resource Group (RG-SOC-L1)
        |
        +-- L3 VNet (VNet-SOC-Lab)
              |
              +-- L4 VM Instance (SECURE-NET-EAST - Our Honeypot)
              |     |
              |     +-- Log Analytics Workspace (LOG-SOC-L1)
              |     |
              |     +-- Microsoft Sentinel (SIEM - Connected to LOG-SOC-L1)
              |     |
              |     +-- Wazuh Agent (Forwarding logs to GCP Wazuh Server)
              |
              +-- GCP Instance (Hosting Wazuh Server)
```

By following these steps, you'll have a fully functional, cross-cloud SOC lab where you can practice real-world threat detection, investigation, and response. **Happy hunting\!**

For further details on setting up Sysmon and rules, I highly recommend watching this video: [Sysmon and rules](https://www.google.com/search?q=https://www.youtube.com/watch%3Fv%3DVIDEO_ID_HERE) (You'll need to replace the URL with the actual video link).


> To get in touch with me or for general discussion please visit [ZeroDayMindset Discussion](https://github.com/orgs/X3N0-G0D/discussions/1) 
{: .prompt-info }

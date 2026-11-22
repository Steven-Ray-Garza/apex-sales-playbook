Set-Location "$HOME\apex-sales-playbook"
Get-Clipboard | Set-Content -Path "POWERSHELL_SOP.md" -Encoding UTF8
git add POWERSHELL_SOP.md
git commit -m "docs: add Windows PowerShell 5.1 end-to-end operating manual"
git push

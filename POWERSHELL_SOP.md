Set-Location "$HOME\apex-sales-playbook"
Get-Clipboard -Raw | Set-Content -Path "POWERSHELL_SOP.md" -Encoding UTF8
git add POWERSHELL_SOP.md
git commit -m "docs: update POWERSHELL_SOP.md to v3.1 (6 modes, Van Westendorp, sources vault)"
git push

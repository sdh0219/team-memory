# team-memory 技能家族安装脚本（Windows）：遍历 skills\ 下所有技能目录，逐一复制到各 agent 的技能目录。
# 用法: powershell -File install.ps1 [-Target zcode|agents|claude|all]   默认 all。
param(
  [ValidateSet("zcode", "agents", "claude", "all")]
  [string]$Target = "all"
)

$skillsDir = Join-Path $PSScriptRoot "..\skills"
$skills = Get-ChildItem -Path $skillsDir -Directory
$map = @{
  zcode  = Join-Path $HOME ".zcode\skills"
  agents = Join-Path $HOME ".agents\skills"
  claude = Join-Path $HOME ".claude\skills"
}

$targets = if ($Target -eq "all") { $map.Values } else { , $map[$Target] }

foreach ($dir in $targets) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  foreach ($skill in $skills) {
    $dest = Join-Path $dir $skill.Name
    if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
    Copy-Item -Recurse -Force $skill.FullName $dest
    Write-Host "OK 已安装 $($skill.Name) 到 $dest"
  }
}

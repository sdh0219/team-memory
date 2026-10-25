# team-memory 安装脚本（Windows）：把 skills/team-memory 复制到各 agent 的技能目录。
# 用法: powershell -File install.ps1 [-Target zcode|agents|claude|all]   默认 all。
param(
  [ValidateSet("zcode", "agents", "claude", "all")]
  [string]$Target = "all"
)

$src = Join-Path $PSScriptRoot "..\skills\team-memory"
$map = @{
  zcode  = Join-Path $HOME ".zcode\skills"
  agents = Join-Path $HOME ".agents\skills"
  claude = Join-Path $HOME ".claude\skills"
}

$targets = if ($Target -eq "all") { $map.Values } else { , $map[$Target] }

foreach ($dir in $targets) {
  $dest = Join-Path $dir "team-memory"
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
  Copy-Item -Recurse -Force $src $dest
  Write-Host "OK 已安装到 $dest"
}

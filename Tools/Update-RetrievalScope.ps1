param(
  [string]$KnowledgeRoot = "",
  [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($KnowledgeRoot)) {
  $repoRoot = Split-Path -Parent $PSScriptRoot
  $KnowledgeRoot = Join-Path $repoRoot "Knowledge"
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
  $OutputPath = Join-Path $KnowledgeRoot "Assets/retrieval_scope.json"
}

$primaryStatuses = @("wiki-expanded", "source-expanded", "reference")
$appliedContextStatuses = @("project-expanded")
$routingStatuses = @("entrypoint", "map", "wiki-map", "operating-guide", "policy")
$activeStatuses = @("active")
$personalStatuses = @("personal-context")
$excludedStatuses = @("wiki-standardized", "template", "migration-report", "source-outline")
$penaltyPatterns = @(
  [regex]::Unescape("\uac15\uc758\uc5d0\uc11c\u0020\ub098\uc628\u0020\uac1c\ub150"),
  [regex]::Unescape("\uc608\uc81c\u0020\ud558\ub098\ub9cc\u0020\ubcf4\uace0"),
  [regex]::Unescape("\uc774\u0020\uac1c\ub150\uc744\u0020\ud55c\u0020\ubb38\uc7a5")
)

function Get-FrontmatterField {
  param(
    [string]$Frontmatter,
    [string]$Name
  )

  $pattern = "(?m)^" + [regex]::Escape($Name) + ":\s*`"?([^`"\r\n]+)`"?"
  $match = [regex]::Match($Frontmatter, $pattern)
  if ($match.Success) {
    return $match.Groups[1].Value.Trim()
  }
  return ""
}

function Get-MarkdownTitle {
  param(
    [string]$Text,
    [string]$Fallback
  )

  $match = [regex]::Match($Text, "(?m)^#\s+(.+)$")
  if ($match.Success) {
    return $match.Groups[1].Value.Trim()
  }
  return [System.IO.Path]::GetFileNameWithoutExtension($Fallback)
}

$knowledgeFullPath = (Resolve-Path -LiteralPath $KnowledgeRoot).Path
$repoRoot = Split-Path -Parent $knowledgeFullPath
$markdownFiles = Get-ChildItem -Recurse -File -Filter *.md $knowledgeFullPath | Sort-Object FullName
$items = @()

foreach ($file in $markdownFiles) {
  $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
  $frontmatter = ""
  $frontmatterMatch = [regex]::Match($text, "(?s)^---\r?\n(.*?)\r?\n---")
  if ($frontmatterMatch.Success) {
    $frontmatter = $frontmatterMatch.Groups[1].Value
  }

  $status = Get-FrontmatterField -Frontmatter $frontmatter -Name "status"
  $type = Get-FrontmatterField -Frontmatter $frontmatter -Name "type"
  $placeholderCount = 0

  foreach ($pattern in $penaltyPatterns) {
    $placeholderCount += ([regex]::Matches($text, [regex]::Escape($pattern))).Count
  }

  $relativePath = $file.FullName.Substring($repoRoot.Length + 1) -replace "\\", "/"
  $bucket = "quarantine"
  $reason = "not_in_default_answer_index"

  if ($primaryStatuses -contains $status) {
    $bucket = "primary_answer_index"
    $reason = "official_source_or_reference_note"
  }
  elseif ($appliedContextStatuses -contains $status) {
    $bucket = "applied_context_index"
    $reason = "project_application_context_not_official_ground_truth"
  }
  elseif ($routingStatuses -contains $status) {
    $bucket = "routing_index"
    $reason = "navigation_or_policy_context"
  }
  elseif ($activeStatuses -contains $status) {
    $bucket = "on_demand_context"
    $reason = "active_working_document"
  }
  elseif ($personalStatuses -contains $status) {
    $bucket = "personal_context"
    $reason = "personal_reflection_excluded_from_default_answer_index"
  }
  elseif ($excludedStatuses -contains $status) {
    $bucket = "quarantine"
    $reason = "draft_template_or_audit_document"
  }

  if ($status -eq "wiki-standardized") {
    $reason = "wiki_standardized_requires_expansion_before_default_indexing"
  }

  if ($placeholderCount -gt 0) {
    $reason = $reason + "; contains_boilerplate_or_placeholder"
  }

  $items += [ordered]@{
    path = $relativePath
    title = Get-MarkdownTitle -Text $text -Fallback $file.Name
    type = $type
    status = $status
    bucket = $bucket
    placeholder_count = $placeholderCount
    reason = $reason
  }
}

$buckets = [ordered]@{}
foreach ($bucketName in @("primary_answer_index", "applied_context_index", "routing_index", "on_demand_context", "personal_context", "quarantine")) {
  $bucketItems = @($items | Where-Object { $_["bucket"] -eq $bucketName })
  $buckets[$bucketName] = [ordered]@{
    count = $bucketItems.Count
    paths = @($bucketItems | ForEach-Object { $_["path"] })
  }
}

$statusCounts = [ordered]@{}
$items | Group-Object { $_["status"] } | Sort-Object Name | ForEach-Object {
  $statusCounts[$_.Name] = $_.Count
}

$scope = [ordered]@{
  generated_at = (Get-Date -Format "yyyy-MM-dd")
  source_root = $knowledgeFullPath
  total_markdown_files = $items.Count
  policy = [ordered]@{
    primary_answer_index_statuses = $primaryStatuses
    applied_context_index_statuses = $appliedContextStatuses
    routing_index_statuses = $routingStatuses
    on_demand_context_statuses = $activeStatuses
    personal_context_statuses = $personalStatuses
    quarantine_statuses = $excludedStatuses
    default_answer_index_excludes_wiki_standardized = $true
  }
  counts_by_status = $statusCounts
  buckets = $buckets
  items = $items
}

$json = $scope | ConvertTo-Json -Depth 8
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText($OutputPath, $json + "`r`n", $utf8NoBom)

Write-Output "retrieval_scope generated: $($items.Count) files"
foreach ($bucketName in $buckets.Keys) {
  Write-Output "${bucketName}: $($buckets[$bucketName].count)"
}

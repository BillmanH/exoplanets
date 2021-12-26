# Load the conda environment
conda activate exoplanets
# Load the json file:
$json = Get-Content 'infra\env-vars.json' | Out-String | ConvertFrom-Json
$omited = "ALLOWED_HOSTS", "stage", "abspath", ""

foreach($v in $json.PSObject.Properties)
{
    if ($omited -contains $v.Name) {
        Write-Host $v.Name "is omitted"
    } else {
        $valstring = $v.Value | Out-String
        $namstring = $v.Name | Out-String
        $command = "conda env config vars set $namstring=$valstring" 
        $command = $command -replace "`t|`n|`r",""
        $v.Name + " : " + $v.Value
        Invoke-expression $command
    }
}


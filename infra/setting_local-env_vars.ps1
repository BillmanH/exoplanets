# Load the conda environment
conda activate exoplanets
# Load the json file:
$json = Get-Content 'infra\env-vars.json' | Out-String | ConvertFrom-Json

foreach($v in $json.PSObject.Properties)
{
    if ($v.Name -eq "ALLOWED_HOSTS" -or $v.Name -eq "stage") {
        Write-Host $v.Name "is omitted"
    } else {
        $v.Name + " : " + $v.Value
        conda env config vars set $v.Name=$v.Value
    }
}


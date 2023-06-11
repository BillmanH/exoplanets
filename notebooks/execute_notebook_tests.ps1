# jupyter nbconvert --execute --to html notebook.ipynb


Get-ChildItem –Path "notebooks" –Recurse |
    Foreach-Object {
        if ( $_.FullName -Match ".ipynb" )
            {
                # Write-Host $_.FullName
                Write-Output "Executing Notebook:  "  $_.FullName
                # jupyter nbconvert --execute --to html $_.FullName
                jupyter nbconvert $_.FullName --to notebook --execute 
            }
    }

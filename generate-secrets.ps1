# Generate secrets for deployment
$jwt_access = [System.Guid]::NewGuid().ToString('N') + [System.Guid]::NewGuid().ToString('N')
$jwt_refresh = [System.Guid]::NewGuid().ToString('N') + [System.Guid]::NewGuid().ToString('N')
$mongo_pass = [System.Guid]::NewGuid().ToString('N')
$postgres_pass = [System.Guid]::NewGuid().ToString('N')

Write-Output "Generated Secrets for Deployment:"
Write-Output "================================="
Write-Output ""
Write-Output "JWT_ACCESS_SECRET=$jwt_access"
Write-Output "JWT_REFRESH_SECRET=$jwt_refresh"
Write-Output "MONGO_PASSWORD=$mongo_pass"
Write-Output "POSTGRES_PASSWORD=$postgres_pass"
Write-Output ""
Write-Output "IMPORTANT: Use the SAME JWT secrets across all three services!"

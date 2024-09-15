$configPath = "C:\Users\sf\.ssh\config"
$instanceName = "terraform-instance"
$zone = "us-central1-a"

# 获取最新的 IP 地址
$newIP = gcloud compute instances describe $instanceName --zone=$zone --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

if ($newIP) {
    # 读取现有配置
    $config = Get-Content $configPath

    # 更新 HostName
    $config = $config -replace '(?<=HostName\s+)\S+', $newIP

    # 写回配置文件
    $config | Set-Content $configPath

    Write-Host "SSH config updated with new IP: $newIP"
} else {
    Write-Host "Failed to retrieve IP address for $instanceName"
}
# URL Attack Detector - Silent Launcher

# 1. Clear Port 8080 (Common Spring Boot port)
$conn = Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue
if ($conn) {
    Stop-Process -Id $conn.OwningProcess -Force
}

# 2. Start ML Service (Python) Hidden
Start-Process -FilePath "python" -ArgumentList "ml_service/app.py" -WindowStyle Hidden -WorkingDirectory $PSScriptRoot

# 3. Start Spring Backend (Java) Hidden
Start-Process -FilePath "cmd.exe" -ArgumentList "/c mvnw.cmd spring-boot:run" -WindowStyle Hidden -WorkingDirectory $PSScriptRoot

# 4. Wait for startup and launch Browser
Start-Sleep -Seconds 12
Start-Process "http://localhost:8080/"

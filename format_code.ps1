# Executar o isort
Write-Host "Executando isort..."
python -m isort .

# Executar o black
Write-Host "Executando black..."
python -m black .

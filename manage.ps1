<#
.SYNOPSIS
    Project management script for Windows (Makefile alternative)

.DESCRIPTION
    Runs common development tasks like starting the server, testing, linting, and docker management.

.EXAMPLE
    .\manage.ps1 run
    .\manage.ps1 docker-up
#>

param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("run", "test", "lint", "format", "migrate", "docker-up", "docker-down")]
    [string]$Command
)

Switch ($Command) {
    "run" {
        Write-Host "Starting uvicorn..." -ForegroundColor Green
        uvicorn app.main:app --reload
    }
    "test" {
        Write-Host "Running tests..." -ForegroundColor Green
        pytest tests/
    }
    "lint" {
        Write-Host "Running linting..." -ForegroundColor Green
        Write-Host "Running flake8..."
        flake8 app tests
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Running mypy..."
            mypy app tests
        }
    }
    "format" {
        Write-Host "Formatting code..." -ForegroundColor Green
        Write-Host "Running black..."
        black app tests
        Write-Host "Running isort..."
        isort app tests
    }
    "migrate" {
        Write-Host "Running migrations..." -ForegroundColor Green
        alembic upgrade head
    }
    "docker-up" {
        Write-Host "Starting Docker containers..." -ForegroundColor Green
        # Try docker-compose first, fall back to docker compose
        if (Get-Command "docker-compose" -ErrorAction SilentlyContinue) {
            docker-compose -f docker/docker-compose.yml up -d --build
        } else {
            docker compose -f docker/docker-compose.yml up -d --build
        }
    }
    "docker-down" {
        Write-Host "Stopping Docker containers..." -ForegroundColor Green
        if (Get-Command "docker-compose" -ErrorAction SilentlyContinue) {
            docker-compose -f docker/docker-compose.yml down
        } else {
            docker compose -f docker/docker-compose.yml down
        }
    }
}

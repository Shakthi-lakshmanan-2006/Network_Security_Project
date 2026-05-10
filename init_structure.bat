@echo off
SETLOCAL EnableDelayedExpansion
title Enterprise Project Structure Initializer (Windows Native)
echo ==============================================================================
echo           INITIALIZING NETWORK SECURITY & SOCIAL ENGINEERING PROJECT           
echo ==============================================================================
echo [INFO] Working Directory: %CD%
echo [INFO] Verification scanning running...
echo ------------------------------------------------------------------------------

:: ------------------------------------------------------------------------------
:: PHASE 1: DIRECTORY HIERARCHY EVALUATION & CREATION
:: ------------------------------------------------------------------------------

echo [BUILD] Processing Core System Directories...

set "DIRS[0]=backend"
set "DIRS[1]=backend\routes"
set "DIRS[2]=backend\controllers"
set "DIRS[3]=backend\services"
set "DIRS[4]=backend\utils"
set "DIRS[5]=backend\middleware"
set "DIRS[6]=backend\models"
set "DIRS[7]=database"
set "DIRS[8]=logs"
set "DIRS[9]=uploads"
set "DIRS[10]=static"
set "DIRS[11]=static\reports"
set "DIRS[12]=static\sample_data"
set "DIRS[13]=docs"
set "DIRS[14]=tests"
set "DIRS[15]=tests\test_frontend"
set "DIRS[16]=frontend"
set "DIRS[17]=frontend\client"
set "DIRS[18]=frontend\client\public"
set "DIRS[19]=frontend\client\src"
set "DIRS[20]=frontend\client\src\components"
set "DIRS[21]=frontend\client\src\components\common"
set "DIRS[22]=frontend\client\src\components\dashboard"
set "DIRS[23]=frontend\client\src\components\alerts"
set "DIRS[24]=frontend\client\src\components\network"
set "DIRS[25]=frontend\client\src\components\training"
set "DIRS[26]=frontend\client\src\pages"
set "DIRS[27]=frontend\client\src\services"
set "DIRS[28]=frontend\client\src\context"
set "DIRS[29]=frontend\client\src\utils"
set "DIRS[30]=frontend\client\src\styles"

for /L %%i in (0,1,30) do (
    eval if not exist "!DIRS[%%i]!" (
        mkdir "!DIRS[%%i]!"
        echo   [+] Created directory: !DIRS[%%i]!
    ) else (
        echo   [~] Verified existing directory: !DIRS[%%i]!
    )
)

:: ------------------------------------------------------------------------------
:: PHASE 2: ROOT INTEGRATION FILES CREATION
:: ------------------------------------------------------------------------------

echo ------------------------------------------------------------------------------
echo [BUILD] Processing Project Root Configuration Matrices...

if not exist ".env" (
    type nul > ".env"
    echo   [+] Generated base asset: .env
) else (echo   [~] Checked: .env exists.)

if not exist ".gitignore" (
    type nul > ".gitignore"
    echo   [+] Generated base asset: .gitignore
) else (echo   [~] Checked: .gitignore exists.)

if not exist "README.md" (
    type nul > "README.md"
    echo   [+] Generated base asset: README.md
) else (echo   [~] Checked: README.md exists.)


:: ------------------------------------------------------------------------------
:: PHASE 3: BACKEND ARCHITECTURAL SOURCE INITIALIZATION
:: ------------------------------------------------------------------------------

echo ------------------------------------------------------------------------------
echo [BUILD] Initializing Backend Engine Components...

:: Base Python App Contexts
if not exist "backend\__init__.py" (type nul > "backend\__init__.py" & echo   [+] File initialized: backend\__init__.py)
if not exist "backend\app.py" (type nul > "backend\app.py" & echo   [+] File initialized: backend\app.py)
if not exist "backend\config.py" (type nul > "backend\config.py" & echo   [+] File initialized: backend\config.py)
if not exist "backend\database.py" (type nul > "backend\database.py" & echo   [+] File initialized: backend\database.py)
if not exist "backend\models.py" (type nul > "backend\models.py" & echo   [+] File initialized: backend\models.py)
if not exist "backend\requirements.txt" (type nul > "backend\requirements.txt" & echo   [+] File initialized: backend\requirements.txt)

:: Module Internal Packages Initializations
if not exist "backend\routes\__init__.py" (type nul > "backend\routes\__init__.py")
if not exist "backend\controllers\__init__.py" (type nul > "backend\controllers\__init__.py")
if not exist "backend\services\__init__.py" (type nul > "backend\services\__init__.py")
if not exist "backend\utils\__init__.py" (type nul > "backend\utils\__init__.py")
if not exist "backend\middleware\__init__.py" (type nul > "backend\middleware\__init__.py")

:: Route Execution Enclaves
if not exist "backend\routes\auth_routes.py" (type nul > "backend\routes\auth_routes.py" & echo   [+] Route initialized: auth_routes.py)
if not exist "backend\routes\dashboard_routes.py" (type nul > "backend\routes\dashboard_routes.py" & echo   [+] Route initialized: dashboard_routes.py)
if not exist "backend\routes\alert_routes.py" (type nul > "backend\routes\alert_routes.py" & echo   [+] Route initialized: alert_routes.py)
if not exist "backend\routes\network_routes.py" (type nul > "backend\routes\network_routes.py" & echo   [+] Route initialized: network_routes.py)
if not exist "backend\routes\phishing_routes.py" (type nul > "backend\routes\phishing_routes.py" & echo   [+] Route initialized: phishing_routes.py)
if not exist "backend\routes\training_routes.py" (type nul > "backend\routes\training_routes.py" & echo   [+] Route initialized: training_routes.py)
if not exist "backend\routes\admin_routes.py" (type nul > "backend\routes\admin_routes.py" & echo   [+] Route initialized: admin_routes.py)

:: Logical Controllers Execution Layers
if not exist "backend\controllers\auth_controller.py" (type nul > "backend\controllers\auth_controller.py" & echo   [+] Controller initialized: auth_controller.py)
if not exist "backend\controllers\alert_controller.py" (type nul > "backend\controllers\alert_controller.py" & echo   [+] Controller initialized: alert_controller.py)
if not exist "backend\controllers\network_controller.py" (type nul > "backend\controllers\network_controller.py" & echo   [+] Controller initialized: network_controller.py)

:: Background Thread Services Engine Clusters
if not exist "backend\services\network_monitor.py" (type nul > "backend\services\network_monitor.py" & echo   [+] Thread Service initialized: network_monitor.py)
if not exist "backend\services\intrusion_detector.py" (type nul > "backend\services\intrusion_detector.py" & echo   [+] Engine Service initialized: intrusion_detector.py)
if not exist "backend\services\phishing_detector.py" (type nul > "backend\services\phishing_detector.py" & echo   [+] Threat Service initialized: phishing_detector.py)
if not exist "backend\services\alert_manager.py" (type nul > "backend\services\alert_manager.py" & echo   [+] Event Service initialized: alert_manager.py)
if not exist "backend\services\email_service.py" (type nul > "backend\services\email_service.py" & echo   [+] Comms Service initialized: email_service.py)
if not exist "backend\services\threat_intelligence.py" (type nul > "backend\services\threat_intelligence.py" & echo   [+] Intel Service initialized: threat_intelligence.py)

:: System Utilities Matrix
if not exist "backend\utils\validators.py" (type nul > "backend\utils\validators.py" & echo   [+] Utility asset mapped: validators.py)
if not exist "backend\utils\helpers.py" (type nul > "backend\utils\helpers.py" & echo   [+] Utility asset mapped: helpers.py)
if not exist "backend\utils\decorators.py" (type nul > "backend\utils\decorators.py" & echo   [+] Utility asset mapped: decorators.py)
if not exist "backend\utils\logger.py" (type nul > "backend\utils\logger.py" & echo   [+] Utility asset mapped: logger.py)

:: Routing Filtering Middleware Layers
if not exist "backend\middleware\auth_middleware.py" (type nul > "backend\middleware\auth_middleware.py" & echo   [+] Security Interceptor initialized: auth_middleware.py)
if not exist "backend\middleware\rate_limiter.py" (type nul > "backend\middleware\rate_limiter.py" & echo   [+] Resource Interceptor initialized: rate_limiter.py)


:: ------------------------------------------------------------------------------
:: PHASE 4: FRONTEND APPLICATION CLIENT ARTIFACT MAPPER
:: ------------------------------------------------------------------------------

echo ------------------------------------------------------------------------------
echo [BUILD] Structuring React SPA Client Subsystems...

:: Main Render Context Points
if not exist "frontend\client\src\App.js" (type nul > "frontend\client\src\App.js" & echo   [+] Render Target structured: App.js)
if not exist "frontend\client\src\index.js" (type nul > "frontend\client\src\index.js" & echo   [+] Execution Target structured: index.js)

:: Component Container Interfaces (Pages)
if not exist "frontend\client\src\pages\Login.jsx" (type nul > "frontend\client\src\pages\Login.jsx" & echo   [+] Interface view compiled: Login.jsx)
if not exist "frontend\client\src\pages\Dashboard.jsx" (type nul > "frontend\client\src\pages\Dashboard.jsx" & echo   [+] Interface view compiled: Dashboard.jsx)
if not exist "frontend\client\src\pages\Alerts.jsx" (type nul > "frontend\client\src\pages\Alerts.jsx" & echo   [+] Interface view compiled: Alerts.jsx)
if not exist "frontend\client\src\pages\NetworkMonitor.jsx" (type nul > "frontend\client\src\pages\NetworkMonitor.jsx" & echo   [+] Interface view compiled: NetworkMonitor.jsx)
if not exist "frontend\client\src\pages\PhishingDetection.jsx" (type nul > "frontend\client\src\pages\PhishingDetection.jsx" & echo   [+] Interface view compiled: PhishingDetection.jsx)
if not exist "frontend\client\src\pages\Training.jsx" (type nul > "frontend\client\src\pages\Training.jsx" & echo   [+] Interface view compiled: Training.jsx)
if not exist "frontend\client\src\pages\Settings.jsx" (type nul > "frontend\client\src\pages\Settings.jsx" & echo   [+] Interface view compiled: Settings.jsx)

:: Network Dynamic Async Connectors (Services)
if not exist "frontend\client\src\services\api.js" (type nul > "frontend\client\src\services\api.js" & echo   [+] API Client proxy deployed: api.js)
if not exist "frontend\client\src\services\authService.js" (type nul > "frontend\client\src\services\authService.js" & echo   [+] Authentication endpoint proxy deployed: authService.js)
if not exist "frontend\client\src\services\alertService.js" (type nul > "frontend\client\src\services\alertService.js" & echo   [+] Incident stream proxy deployed: alertService.js)
if not exist "frontend\client\src\services\networkService.js" (type nul > "frontend\client\src\services\networkService.js" & echo   [+] Transport stream proxy deployed: networkService.js)

:: Internal Engine Stores, Wrappers and Functional Assets
if not exist "frontend\client\src\context\AuthContext.js" (type nul > "frontend\client\src\context\AuthContext.js" & echo   [+] Internal Engine element instantiated: AuthContext.js)
if not exist "frontend\client\src\utils\helpers.js" (type nul > "frontend\client\src\utils\helpers.js" & echo   [+] Client helper utility instantiated: utils\helpers.js)
if not exist "frontend\client\src\utils\constants.js" (type nul > "frontend\client\src\utils\constants.js" & echo   [+] System definitions array mapped: utils\constants.js)
if not exist "frontend\client\src\styles\theme.js" (type nul > "frontend\client\src\styles\theme.js" & echo   [+] Theme engine sheet dropped: theme.js)


:: ------------------------------------------------------------------------------
:: PHASE 5: EXTRA DATA PIPELINES, TEST BEDS AND DOCUMENTATION ASSETS
:: ------------------------------------------------------------------------------

echo ------------------------------------------------------------------------------
echo [BUILD] Generating Peripheral Systems Framework Layers...

if not exist "database\seed_data.js" (type nul > "database\seed_data.js" & echo   [+] Database structural seeder ready: seed_data.js)
if not exist "tests\test_backend.py" (type nul > "tests\test_backend.py" & echo   [+] Testing script context deployed: test_backend.py)

:: System Engineering Blueprints Documentation Target Files
if not exist "docs\API_DOCUMENTATION.md" (type nul > "docs\API_DOCUMENTATION.md" & echo   [+] Documentation target provisioned: API_DOCUMENTATION.md)
if not exist "docs\USER_GUIDE.md" (type nul > "docs\USER_GUIDE.md" & echo   [+] Documentation target provisioned: USER_GUIDE.md)
if not exist "docs\TECHNICAL_REPORT.md" (type nul > "docs\TECHNICAL_REPORT.md" & echo   [+] Documentation target provisioned: TECHNICAL_REPORT.md)

echo ------------------------------------------------------------------------------
echo [SUCCESS] File architecture system verification and synthesis sequence complete.
echo [CLEANUP] Removing temporary script file...
del "%~f0" & exit
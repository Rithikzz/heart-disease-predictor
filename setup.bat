@echo off
echo Creating frontend directory structure...

mkdir frontend 2>nul
mkdir frontend\public 2>nul
mkdir frontend\src 2>nul

echo Directories created successfully!
echo.
echo Next steps:
echo 1. Run this setup.bat file
echo 2. Then run: python create_frontend_files.py
echo 3. Install Python dependencies: pip install -r requirements.txt
echo 4. Train the model using the Jupyter notebook
echo 5. Start Flask backend: python app.py
echo 6. In another terminal, cd to frontend and run: npm install
echo 7. Start React frontend: npm start
pause

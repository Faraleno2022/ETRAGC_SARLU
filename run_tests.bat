@echo off
echo ========================================
echo EXECUTION DES TESTS DE DEDUCTION
echo ========================================
echo.

python manage.py shell < create_test_data.py

echo.
echo ========================================
echo TESTS TERMINES !
echo ========================================
echo.
echo Appuyez sur une touche pour fermer...
pause > nul

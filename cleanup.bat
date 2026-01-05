@echo off
echo Mowa, cleaning up your project...

if not exist scripts mkdir scripts
if not exist tests mkdir tests

echo Moving scripts...
move add_col.py scripts/
move create_db.py scripts/
move debug_db.py scripts/
move fix_db.py scripts/
move force_reset_db.py scripts/
move mowa_setup.py scripts/
move patch_mowa.py scripts/
move reset_db.py scripts/
move simple_reset.py scripts/
move check_discounts.py scripts/

echo Moving tests...
move test_api.py tests/
move test_conn.py tests/
move verify_6_apis_mowa.py tests/
move verify_discount_fixes.py tests/
move verify_final.py tests/

echo.
echo Cleanup complete mowa! Your project structure is now neat.
echo.
pause

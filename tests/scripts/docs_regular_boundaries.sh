OUT="test_outputs/regular_boundaries"
. tests/scripts/initialize_output_folders.sh $OUT
. tests/scripts/get_plopm.sh
. tests/scripts/get_pytest.sh
WHR="test_outputs/popen-gw2/test_2_generic_deck0/rotate/simulations"
if [ ! -d $WHR ]; then
    pytest --basetemp=$OUT -n 2 tests/test_2_generic_deck.py tests/test_4_site_regional.py
    WHR="$OUT/popen-gw0/test_2_generic_deck0/rotate/simulations"
    WHR1="$OUT/popen-gw1/test_4_site_regional0"
else
    WHR1="test_outputs/popen-gw4/test_4_site_regional0"
fi
plopm -i "$WHR/site_closed/SITE_CLOSED $WHR/expreccs/EXPRECCS $WHR/reference/REFERENCE" -v sgas -s ',,1 ,,1 ,,1' -sg 1,3 -st 0 -cbp 0.2,0.95,0.6,0.02 -fs 24,8 -cbf .1f -fz 20 -xu km -yu km -xf .0f -yf .0f -x '[0,15000]' -y '[0,15000]' -rdl 1 -o $OUT
plopm -i "$WHR1/regional/REGIONAL $WHR1/expreccs/EXPRECCS $WHR1/expreccs_dpincrease/EXPRECCS_DPINCREASE $WHR1/expreccs_perfipnum/EXPRECCS_PERFIPNUM" -v rpr:3 -o $OUT -sp 1

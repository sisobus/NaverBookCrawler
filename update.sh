python down.py
echo "down complete"
python parse.py
echo "parse complete"
python update_db.py
echo "db update complete"
cp info.sqlite /home/hsb/public_html

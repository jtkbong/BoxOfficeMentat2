echo "Creating package for BoxOfficeMentat-Worker..."
mkdir package
cd package

echo "Installing requirements into package..."
pip install Pillow --target .
pip install -r ../requirements.txt --target .
zip -r9 ../boxofficementat-worker.zip .
cd ../

echo "Adding source files to package..."
zip -g boxofficementat-worker.zip main.py
zip -g boxofficementat-worker.zip common/*.py
zip -g boxofficementat-worker.zip scrapetasks/*.py
zip -g boxofficementat-worker.zip config/*

echo "Cleaning up..."
rm -rf package

echo "BoxOfficeMentat-Worker is packaged and good to deploy!"
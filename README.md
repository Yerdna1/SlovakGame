# Remove the virtual environment
rm -rf venv

# Create a new one
python3.10 -m venv venv

# Activate it
source venv/bin/activate

# or at once
pip install -r requirements.txt

# Install packages in the correct order
pip install --upgrade pip
pip install numpy==1.23.5
pip install opencv-python==4.8.0.74



# run app
python main.py


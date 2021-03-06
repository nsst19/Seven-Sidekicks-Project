#!/usr/bin/env bash

# Install apt dependencies
echo "Installing apt dependencies..."
sudo apt-get update 1>/dev/null
sudo apt-get install -y build-essential libqt4-dev libyaml-dev pkg-config libyaml-dev 1>/dev/null

sudo apt-get install -y libfftw3-dev libavcodec-dev libavformat-dev libavutil-dev libavresample-dev 1>/dev/null
sudo apt-get install -y python-dev libsamplerate0-dev libtag1-dev libchromaprint-dev python-six 1>/dev/null
sudo apt-get install -y python3-dev python3-numpy-dev python3-numpy python3-yaml 1>/dev/null

# Install Gaia2 if not already installed
if [ ! -d "/usr/local/include/gaia2" ]; then
    echo "Gaia not installed. Checking for swig..."

    # Install Swig if not already installed
    if [ ! -d "/usr/local/share/swig" ]; then
        echo "Swig not installed. Installing swig..."
        cd $HOME

        wget https://github.com/swig/swig/archive/rel-4.0.0.zip 1>/dev/null
        unzip rel-4.0.0.zip 1>/dev/null
        cd swig-rel-4.0.0

        ./autogen.sh
        ./configure
        make 1>/dev/null
        sudo make install
        cd ..
        rm -rf *rel-4.0.0*
    fi
    
    echo "Swig installed. Installing gaia..."
    cd $HOME

    wget https://github.com/MTG/gaia/archive/v2.4.5.zip 1>/dev/null
    unzip v2.4.5.zip 1>/dev/null
    cd gaia-2.4.5

    python2 ./waf configure --with-python-bindings
    python2 ./waf 1>/dev/null
    sudo python2 ./waf install
    cd ..
    rm -rf *2.4.5

    echo "Gaia installed."
fi

# Install Essentia if not already installed
if [ ! -d "/home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/essentia/" ]; then
    echo "Essentia not installed. Installing Essentia..."
    cd $HOME

    git clone https://github.com/MTG/essentia 1>/dev/null
    cd essentia

    # As of the moment I'm making this commit (25/03/2019), their master doesn't work. This commit works.
    git reset --hard 6b584720c2d0dc0202a9ed5fc4e2121756dadd3a

    ./waf configure --build-static --with-examples --with-python --with-gaia
    ./waf 1>/dev/null
    sudo python3 ./waf install

    python -c 'import essentia'

    cd ..
    rm -rf essentia
    echo "Essentia installed."
fi

echo "All dependencies successfully installed. Going to tests..."

cd $TRAVIS_BUILD_DIR
mv config-travis.yml src/config.yml

cd src
